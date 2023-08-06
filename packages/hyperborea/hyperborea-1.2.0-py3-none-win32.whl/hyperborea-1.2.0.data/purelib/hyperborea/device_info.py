import logging
import math

import asphodel
import hyperborea.proxy

logger = logging.getLogger(__name__)


def get_reconnect_info(device):
    info = {}

    device_logger = hyperborea.proxy.get_device_logger(logger, device)

    try:
        # LEDs
        leds = device.get_led_count()
        info['led_settings'] = [device.get_led_value(i) for i in range(leds)]
        rgbs = device.get_rgb_count()
        info['rgb_settings'] = [device.get_rgb_values(i) for i in range(rgbs)]

        # ctrl variables
        ctrl_vars = device.get_ctrl_var_count()
        ctrl_var_settings = [device.get_ctrl_var(i) for i in range(ctrl_vars)]
        info['ctrl_var_settings'] = ctrl_var_settings

        if device.supports_rf_power_commands():
            info['rf_power_status'] = device.get_rf_power_status()

        # device mode (if supported)
        try:
            info['device_mode'] = device.get_device_mode()
            info['supports_device_mode'] = True
        except asphodel.AsphodelError as e:
            if e.args[1] == "ERROR_CODE_UNIMPLEMENTED_COMMAND":
                info['supports_device_mode'] = False
            else:
                raise
    except Exception:
        device_logger.exception("Unhandled exception in get_reconnect_info()")
        return {}

    return info


def get_initial_info(device, progress_pipe=None):
    info = {}
    device_logger = hyperborea.proxy.get_device_logger(logger, device)

    total_commands = 10 + 13 + 3 + 1
    finished_commands = 0

    def increment_and_report(increment, section):
        if progress_pipe:
            nonlocal finished_commands
            finished_commands += increment
            progress_pipe.send((finished_commands, total_commands, section))

    try:
        # (10 commands)
        # do the count commands first, so we can try to figure out how many
        # command exchanges will need to happen
        custom_enum_counts = device.get_custom_enum_counts()
        custom_enum_commands = sum(custom_enum_counts)
        total_commands += custom_enum_commands

        setting_category_count = device.get_setting_category_count()
        setting_caterogy_commands = 2 * setting_category_count
        total_commands += setting_caterogy_commands

        leds = device.get_led_count()
        rgbs = device.get_rgb_count()
        total_commands += leds + rgbs

        stream_count, filler_bits, id_bits = device.get_stream_count()
        stream_commands = 4 * stream_count
        total_commands += stream_commands

        channel_count = device.get_channel_count()
        channel_commands = 4 * channel_count
        total_commands += channel_commands

        supply_count = device.get_supply_count()
        supply_commands = 2 * supply_count
        total_commands += supply_commands

        ctrl_var_count = device.get_ctrl_var_count()
        ctrl_var_commands = 3 * ctrl_var_count
        total_commands += ctrl_var_commands

        setting_count = device.get_setting_count()
        setting_commands = 3 * setting_count
        total_commands += setting_commands

        nvm_size = device.get_nvm_size()
        nvm_bpc = (device.get_max_incoming_param_length() // 4) * 4
        nvm_commands = math.ceil(nvm_size / nvm_bpc)
        total_commands += nvm_commands

        increment_and_report(10, "counts")

        # misc info (13 commands)
        info['serial_number'] = device.get_serial_number()
        info['location_string'] = device.get_location_string()
        info['protocol_version'] = device.get_protocol_version_string()
        info['board_info'] = device.get_board_info()
        info['build_info'] = device.get_build_info()
        info['build_date'] = device.get_build_date()
        info['chip_family'] = device.get_chip_family()
        info['chip_model'] = device.get_chip_model()
        info['chip_id'] = device.get_chip_id()
        info['bootloader_info'] = device.get_bootloader_info()
        info['library_protocol_version'] = asphodel.protocol_version_string
        info['library_build_info'] = asphodel.build_info
        info['library_build_date'] = asphodel.build_date
        increment_and_report(13, "strings")

        # nvm
        nvm_bytes = device.read_nvm_section(0, nvm_size)
        info['nvm'] = nvm_bytes
        increment_and_report(nvm_commands, "nvm")

        # user tags (~3 commands)
        info['tag_locations'] = device.get_user_tag_locations()
        try:
            tag_1_loc = info['tag_locations'][0]
            info['user_tag_1'] = device.read_user_tag_string(*tag_1_loc)
        except UnicodeDecodeError:
            info['user_tag_1'] = None
        try:
            tag_2_loc = info['tag_locations'][1]
            info['user_tag_2'] = device.read_user_tag_string(*tag_2_loc)
        except UnicodeDecodeError:
            info['user_tag_2'] = None
        increment_and_report(3, "tags")

        # custom enums (1 each)
        custom_enums = {}
        for i, count in enumerate(custom_enum_counts):
            custom_enums[i] = [device.get_custom_enum_value_name(i, v)
                               for v in range(count)]
            increment_and_report(count, "custom enum {}".format(i))
        info['custom_enums'] = custom_enums

        # setting categories (2 each)
        setting_categories = []
        for i in range(setting_category_count):
            name = device.get_setting_category_name(i)
            settings = device.get_setting_category_settings(i)
            setting_categories.append((name, settings))
            increment_and_report(2, "setting category {}".format(i))
        info['setting_categories'] = setting_categories

        # packet sizes (0 commands)
        info["max_incoming_param_length"] = \
            device.get_max_incoming_param_length()
        info["max_outgoing_param_length"] = \
            device.get_max_outgoing_param_length()
        info["stream_packet_length"] = device.get_stream_packet_length()

        # LEDs (1 each for LED and RGB)
        info['led_settings'] = [device.get_led_value(i) for i in range(leds)]
        increment_and_report(leds, "LEDs")
        info['rgb_settings'] = [device.get_rgb_values(i) for i in range(rgbs)]
        increment_and_report(rgbs, "RGBs")

        # streams (4 commands each)
        streams = []
        stream_rate_info = []
        for i in range(stream_count):
            streams.append(device.get_stream(i))
            stream_rate_info.append(device.get_stream_rate_info(i))
            device.enable_stream(i, False)  # stop the stream
            increment_and_report(4, "stream {}".format(i))
        info['streams'] = streams
        info['stream_filler_bits'] = filler_bits
        info['stream_id_bits'] = id_bits
        info['stream_rate_info'] = stream_rate_info

        # channels (~4 commands each)
        channels = []
        channel_calibration = []
        supports_calibration = True
        for i in range(channel_count):
            channels.append(device.get_channel(i))
            if supports_calibration:
                try:
                    channel_calibration.append(
                        device.get_channel_calibration(i))
                except asphodel.AsphodelError as e:
                    if e.args[1] == "ERROR_CODE_UNIMPLEMENTED_COMMAND":
                        supports_calibration = False
                        channel_calibration.append(None)
                    else:
                        raise
            else:
                channel_calibration.append(None)
            increment_and_report(4, "channel {}".format(i))
        info['channels'] = channels
        info['channel_calibration'] = channel_calibration

        # supplies (2 commands each)
        supplies = []
        for i in range(supply_count):
            supply_name = device.get_supply_name(i)
            supply_info = device.get_supply_info(i)
            supplies.append((supply_name, supply_info))
            increment_and_report(2, "supply {}".format(i))
        info['supplies'] = supplies

        # ctrl variables (3 commands each)
        ctrl_vars = []
        for i in range(ctrl_var_count):
            ctrl_var_name = device.get_ctrl_var_name(i)
            ctrl_var_info = device.get_ctrl_var_info(i)
            setting = device.get_ctrl_var(i)
            ctrl_vars.append((ctrl_var_name, ctrl_var_info, setting))
            increment_and_report(3, "ctrl var {}".format(i))
        info['ctrl_vars'] = ctrl_vars

        # settings (3 commands each)
        settings = []
        for i in range(setting_count):
            settings.append(device.get_setting(i))
            increment_and_report(3, "setting {}".format(i))
        info['settings'] = settings

        # device mode (1 command)
        try:
            info['device_mode'] = device.get_device_mode()
            info['supports_device_mode'] = True
        except asphodel.AsphodelError as e:
            if e.args[1] == "ERROR_CODE_UNIMPLEMENTED_COMMAND":
                info['supports_device_mode'] = False
            else:
                raise
        increment_and_report(1, "device mode")

        # Extended device types (~0 commands)
        info['supports_rf_power'] = device.supports_rf_power_commands()
        if info['supports_rf_power']:
            info['rf_power_status'] = device.get_rf_power_status()
            info['rf_power_ctrl_vars'] = device.get_rf_power_ctrl_vars()
        info['supports_radio'] = device.supports_radio_commands()
        if info['supports_radio']:
            try:
                device.get_radio_scan_power([0])
                info['radio_scan_power'] = True
            except:
                info['radio_scan_power'] = False
            device.stop_radio()
            info['radio_ctrl_vars'] = device.get_radio_ctrl_vars()
            info['radio_default_serial'] = device.get_radio_default_serial()
        info['supports_remote'] = device.supports_remote_commands()
        info['supports_bootloader'] = device.supports_bootloader_commands()
    except Exception:
        device_logger.exception("Unhandled exception in get_initial_info()")
        return {}
    finally:
        if progress_pipe:
            progress_pipe.close()

    return info
