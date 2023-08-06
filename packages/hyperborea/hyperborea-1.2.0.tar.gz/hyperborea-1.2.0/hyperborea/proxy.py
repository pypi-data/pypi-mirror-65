import itertools
import logging.handlers
import multiprocessing
import os
import queue
import signal
import sys
import threading

import psutil
from PySide2 import QtCore

logger = logging.getLogger(__name__)


TIMEOUT = 0.1  # 100 milliseconds

# globals
local_cleanup = []  # list of (func, [args], {kwargs})
got_local_exit = False
device_lock = None
proxy_ids = {}
device_identifiers = {}  # key deivce, value: identifier


def noop_function(device=None):
    return None


def _simple_access(device, function_name, *args, **kwargs):
    func = getattr(device, function_name)
    result = func(*args, **kwargs)
    return result


class DeviceOperation(QtCore.QObject):
    """
    This class represents an operation on the hardware (e.g. set_leds).
    """

    completed = QtCore.Signal(object)
    error = QtCore.Signal()  # no message; that's handled by the proxy's error

    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function  # function to be called in the remote process
        self.args = args  # args to pass to the function
        self.kwargs = kwargs  # kwargs to pass to the function


class SimpleDeviceOperation(DeviceOperation):
    def __init__(self, function_name, *args, **kwargs):
        super().__init__(_simple_access, function_name, *args, **kwargs)


class OptionalDeviceStringFilter:
    # creates a record.optdevice string created via fmt % record.device
    # but replaces it with fallback if record.device does not exist
    def __init__(self, fmt, fallback):
        self.fmt = fmt
        self.fallback = fallback

    def filter(self, record):
        try:
            record.optdevice = self.fmt % record.device
        except AttributeError:
            record.optdevice = self.fallback
        return True


class DeviceLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, device_id):
        super().__init__(logger, {'device': device_id})


def get_device_logger(logger, device):
    identifier = device_identifiers.get(device, "unknown")
    return DeviceLoggerAdapter(logger, identifier)


def setup_remote_logging(log_queue):
    handler = logging.handlers.QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)
    # remove pyusb's logging info
    pyusb_logger = logging.getLogger("usb")
    pyusb_logger.propagate = False


def register_local_cleanup(cleanup_func, *args, **kwargs):
    global local_cleanup
    local_cleanup.append((cleanup_func, args, kwargs))


def unregister_local_cleanup(cleanup_func, *args, **kwargs):
    global local_cleanup
    local_cleanup.remove((cleanup_func, args, kwargs))


def local_exit():
    global got_local_exit
    got_local_exit = True


def proxy_process(log_queue, incoming, outgoing, identifier,
                  find_func, ffargs, ffkwargs):
    global local_cleanup
    global device_lock

    # fix a bug with stderr and stdout being None
    sys.stdout = open(os.devnull)
    sys.stderr = open(os.devnull)

    setup_remote_logging(log_queue)

    device = None
    device_lock = threading.Lock()

    # create a logger using the device specific identifier
    device_logger = DeviceLoggerAdapter(logger, identifier)

    # ctrl+c handling: want to let the main process send the exit command
    if sys.platform == "win32":
        # the best way on windows? since we can't create a new process group
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    else:
        # move to a new process group (won't be signalled with ctrl+c)
        os.setpgrp()

    device_logger.debug("Proxy process starting")
    me = psutil.Process(os.getpid())
    try:
        try:
            device = find_func(*ffargs, **ffkwargs)
            outgoing.put(True)  # signals success
        except Exception as e:
            device_logger.exception("Exception")
            outgoing.put(e)
        if device:
            proxy_ids[None] = device
            device_identifiers[device] = identifier
            while me.parent() is not None:
                try:
                    if got_local_exit:
                        break
                    job = incoming.get(True, TIMEOUT)
                    if job is None:  # check for sentinel value
                        break
                    job_id, proxy_id, function, args, kwargs = job
                    device_logger.debug("got: {}".format(job))
                    try:
                        with device_lock:
                            proxy_device = proxy_ids[proxy_id]
                            result = function(proxy_device, *args, **kwargs)
                        outgoing.put((job_id, result))
                        device_logger.debug(
                            "finished: {} => {}".format(job, result))
                    except Exception as e:
                        device_logger.exception("Exception")
                        outgoing.put(e)
                except queue.Empty:
                    pass

        # finished with the outgoing queue
        outgoing.put(None)  # sentinel value
        outgoing.close()

        if device:
            # make a copy of the list in case it gets modified in the loop
            for cleanup in local_cleanup[:]:
                try:
                    with device_lock:
                        func, args, kwargs = cleanup
                        func(*args, **kwargs)
                except Exception as e:
                    device_logger.exception("Exception during cleanup")
    except:
        device_logger.exception("Uncaught Exception in Remote Process")
        raise
    finally:
        if device:
            device.close()
    device_logger.debug("Proxy process ending")


class DeviceProxy(QtCore.QObject):
    """
    This class represents a Device being handled in a different process.
    """

    connected = QtCore.Signal()
    disconnected = QtCore.Signal()
    error = QtCore.Signal(str)

    def __init__(self, log_queue, identifier, find_func, *args, **kwargs):
        super().__init__()
        self.identifier = identifier
        self.log_queue = log_queue

        self.logger = DeviceLoggerAdapter(logger, identifier)

        self.toProcess = multiprocessing.Queue()
        self.fromProcess = multiprocessing.Queue()

        self.process = multiprocessing.Process(target=proxy_process,
                                               args=(self.log_queue,
                                                     self.toProcess,
                                                     self.fromProcess,
                                                     identifier,
                                                     find_func, args, kwargs))
        self.process.daemon = True

        self.monitor_thread = threading.Thread(target=self.monitor)
        self.started = False

        self.jobs = {}
        self.next_job_index = 0

        self.proxy_id_counter = itertools.count()

    def handle_reply(self, reply):
        try:
            if reply is True:  # connection success
                self.connected.emit()
            elif isinstance(reply, Exception):
                import traceback
                message = traceback.format_exception_only(type(reply), reply)
                message = "".join(message)
                if message[-1:] == "\n":
                    message = message[:-1]
                self.logger.error(message)
                self.error.emit(message)
                self.close_connection()
            else:
                job_id, result = reply
                if result is None:  # NOTE: emitting None will crash pyside
                    result = type(None)  # send builtins.NoneType instead
                self.jobs[job_id].completed.emit(result)
                del self.jobs[job_id]
        except:
            self.logger.exception("Unhandled Exception in Monitor Thread")

    def monitor(self):
        """
        thread target to monitor the responses from the remote process
        """
        self.logger.debug("Monitor thread starting")
        self.started = True
        normal_exit = False
        while self.process.is_alive():  # check that process is still running
            try:
                reply = self.fromProcess.get(True, TIMEOUT)
                if reply is None:  # check for sentinel value
                    normal_exit = True
                    break
                self.handle_reply(reply)
            except queue.Empty:
                pass
        # might still be entries in the queue
        while True:
            try:
                reply = self.fromProcess.get(False)
                if reply is None:
                    normal_exit = True
                    continue
                self.handle_reply(reply)
            except queue.Empty:
                break
        for operation in list(self.jobs.values()):
            operation.error.emit()
        self.jobs = {}  # empty out the jobs
        self.logger.debug("Monitor thread finished")
        if not normal_exit:
            message = "Device Process Closed Prematurely!"
            self.logger.error(message)
            self.error.emit(message)
        self.disconnected.emit()
        self.process.join()
        self.logger.debug("Monitor thread closing")

    @QtCore.Slot()
    def open_connection(self):
        if self.monitor_thread.is_alive() or self.process.is_alive():
            raise Exception("Proxy already opened!")
        self.process.start()
        self.monitor_thread.start()
        # NOTE: connected is emitted when the device connection is established

    @QtCore.Slot()
    def close_connection(self):
        self.toProcess.put(None)  # send sentinel value to remote process
        # NOTE: monitor waits for process to finish then emits disconnected

    def send_job(self, operation, *args, proxy_id=None, **kwargs):
        job_index = self.next_job_index
        self.next_job_index = (self.next_job_index + 1) & 0xFFFFFFFF
        self.jobs[job_index] = operation

        new_kwargs = dict(list(operation.kwargs.items()) +
                          list(kwargs.items()))
        new_args = operation.args + args

        self.toProcess.put((job_index, proxy_id, operation.function,
                            new_args, new_kwargs))

    def wait_for_close(self):
        if self.monitor_thread.is_alive():
            self.close_connection()
            self.monitor_thread.join()

    def is_finished(self):
        if self.started:
            return not self.monitor_thread.is_alive()
        else:
            return False

    def create_subproxy(self, func, *args, **kwargs):
        proxy_id = next(self.proxy_id_counter)
        op = DeviceOperation(create_subproxy_util, func, proxy_id,
                             self.identifier, *args, **kwargs)
        subproxy = DeviceSubProxy(self, proxy_id, op)
        return subproxy


def create_subproxy_util(device, func, proxy_id, identifier, *args, **kwargs):
    """ called from create_subproxy() to handle registration """
    try:
        subproxy_device = func(device, *args, **kwargs)
        proxy_ids[proxy_id] = subproxy_device

        subproxy_sn = subproxy_device.get_serial_number()
        subproxy_identifier = "{}->{}".format(identifier, subproxy_sn)
        device_identifiers[subproxy_device] = subproxy_identifier

        return True
    except Exception:
        message = "[{}] Unhandled exception in create_subproxy_util()"
        logger.exception(message.format(identifier))
        return False


class DeviceSubProxy(QtCore.QObject):

    connected = QtCore.Signal()
    disconnected = QtCore.Signal()
    error = QtCore.Signal(str)

    def __init__(self, proxy, proxy_id, start_op):
        super().__init__()

        self.proxy = proxy
        self.proxy_id = proxy_id
        self.start_op = start_op

        self.opened = False

        # connect signals from the parent into this instance
        self.proxy.disconnected.connect(self.disconnected)
        self.proxy.error.connect(self.error)

        self.close_job = DeviceOperation(noop_function)
        self.close_job.completed.connect(self.close_completed)

    @QtCore.Slot()
    def open_connection(self):
        self.start_op.completed.connect(self.connected_cb)
        self.proxy.send_job(self.start_op)
        # NOTE: connected is emitted when the device connection is established

    @QtCore.Slot()
    def close_connection(self):
        if self.opened:
            self.proxy.send_job(self.close_job, proxy_id=self.proxy_id)
            self.opened = False

    def close_completed(self):
        self.proxy.disconnected.disconnect(self.disconnected)
        self.proxy.error.disconnect(self.error)
        self.disconnected.emit()

    def connected_cb(self, success):
        if success:
            self.opened = True
            self.connected.emit()
        else:
            self.error.emit("Subproxy Creation Failed")
            self.proxy.disconnected.disconnect(self.disconnected)
            self.proxy.error.disconnect(self.error)
            self.disconnected.emit()

    def wait_for_close(self):
        pass

    def send_job(self, operation, *args, **kwargs):
        if self.opened:
            self.proxy.send_job(operation, *args, proxy_id=self.proxy_id,
                                **kwargs)


class RemoteToLocalLogHandler(logging.Handler):
    def __init__(self, logger_name):
        super().__init__()
        self.logger = logging.getLogger(logger_name)

    def emit(self, record):
        self.logger.handle(record)


class DeviceProxyManager:
    def __init__(self):
        self.setup_logging()
        self.proxies = []

    def setup_logging(self):
        # setup the directory
        logdir = QtCore.QStandardPaths.writableLocation(
            QtCore.QStandardPaths.DataLocation)
        logfile = os.path.join(logdir, "usb.log")
        os.makedirs(logdir, exist_ok=True)  # make sure the directory exists

        file_handler = logging.handlers.RotatingFileHandler(logfile,
                                                            maxBytes=10e6,
                                                            backupCount=9)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s"
                                      " -%(optdevice)s %(message)s")
        file_handler.setFormatter(formatter)
        optdevice_filter = OptionalDeviceStringFilter(" [%s]", "")
        file_handler.addFilter(optdevice_filter)

        local_handler = RemoteToLocalLogHandler(__name__ + ".remote")

        handlers = [file_handler, local_handler]

        self.logQueue = multiprocessing.Queue()
        self.logListener = logging.handlers.QueueListener(self.logQueue,
                                                          *handlers)
        self.logListener.start()

    def stop(self):
        for proxy in self.proxies:
            proxy.wait_for_close()
        self.logListener.stop()

    def clear_finished_proxies(self):
        original_proxies = self.proxies
        for proxy in original_proxies:
            if proxy.is_finished():
                self.proxies.remove(proxy)

    def new_proxy(self, identifier, find_func, *args, **kwargs):
        # clear finished proxies first
        self.clear_finished_proxies()

        proxy = DeviceProxy(self.logQueue, identifier, find_func,
                            *args, **kwargs)
        self.proxies.append(proxy)
        return proxy
