import logging
import threading
import urllib.parse

from PySide2 import QtCore
import requests

logger = logging.getLogger(__name__)


class FirmwareFinder(QtCore.QObject):
    completed = QtCore.Signal(object)
    error = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

    def find_firmware(self, build_type, board_info=None, repo=None,
                      branch=None, commit=None):
        keys = []
        # need either board_info or repo, but not both
        if board_info:
            if repo:
                raise ValueError("Cannot specify both board_info and repo")
            else:
                board_name, board_rev = board_info
                keys.append("boardname={}".format(
                    urllib.parse.quote(board_name)))
                keys.append("boardrev={}".format(board_rev))
        else:
            if repo:
                keys.append("repo={}".format(urllib.parse.quote(repo)))
            else:
                raise ValueError("Must specify one of board_info or repo")

        # need at most one of branch and commit
        if commit and branch:
            raise ValueError("Cannot specify both commit and branch")
        elif commit is not None:
            keys.append("hash={}".format(commit))
        elif branch is not None:
            keys.append("branch={}".format(branch))

        base_url = "https://api.suprocktech.com/firmwareinfo/findfirmware"
        url = base_url + "?" + "&".join(keys)

        self.request_thread = threading.Thread(
            target=self.request_thread_run, args=(url, build_type))
        self.request_thread.start()

    def request_thread_run(self, url, build_type):
        try:
            logger.info("Requesting firmware from url %s", url)
            response = requests.get(url)

            if not response.ok:
                logger.error("Error in findfirmware: %s", response.text)
                self.error.emit("Error requesting firmware information!")
                return

            build_urls = response.json()

            if not build_urls:
                logger.error("Empty response to findfirmware!")
                self.error.emit("Error requesting firmware information!")
                return

            if build_type is not None and build_type in build_urls:
                build_urls = {build_type: build_urls[build_type]}

            self.completed.emit(build_urls)
        except Exception:
            logger.exception('Error finding firmware')
            self.error.emit('Unknown error finding firmware!')


class SoftwareFinder(QtCore.QObject):
    completed = QtCore.Signal(object)
    error = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

    def find_software(self, repo, build_key, branch=None, commit=None):
        base_url = "https://api.suprocktech.com/software/findsoftware"
        keys = ["repo={}".format(repo), "key={}".format(build_key)]
        if commit:
            keys.append("hash={}".format(commit))
        if branch:
            keys.append("branch={}".format(branch))

        url = base_url + "?" + "&".join(keys)

        self.request_thread = threading.Thread(
            target=self.request_thread_run, args=(url,))
        self.request_thread.start()

    def request_thread_run(self, url):
        try:
            logger.info("Requesting update from url %s", url)
            response = requests.get(url)

            if not response.ok:
                logger.error("Error in findsoftware: %s", response.text)
                self.error.emit("Error requesting software information!")
                return

            values = response.json()

            if not values or "url" not in values:
                logger.error("Empty response to findsoftware!")
                self.error.emit("Error requesting software information!")
                return

            url = values['url']
            commit = values.get('commit', None)
            state = values.get('state', "SUCCESSFUL")
            ready = (state == "SUCCESSFUL")

            self.completed.emit((url, commit, ready))
        except Exception:
            logger.exception('Error finding software')
            self.error.emit("Unknown error finding software!")


class Downloader(QtCore.QObject):
    completed = QtCore.Signal(object)
    error = QtCore.Signal(object, str)

    def __init__(self):
        super().__init__()

    def start_download(self, url, file, update):
        self.download_thread = threading.Thread(
            target=self.download_thread_run, args=(url, file, update))
        self.download_thread.start()

    def download_thread_run(self, url, file, update):
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_length = r.headers.get('content-length')
                written_bytes = 0
                if total_length:
                    total_length = int(total_length)
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:
                        file.write(chunk)
                        written_bytes += len(chunk)
                        if update and total_length:
                            update(written_bytes, total_length)
                self.completed.emit(file)
        except Exception:
            logger.exception('Error downloading file')
            self.error.emit(file, 'Error downloading file')
