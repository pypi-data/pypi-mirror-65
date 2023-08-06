"""
This module maintains a device configuration. It provides a device manager for output and input modules each.
"""
import json
import os
from datetime import datetime
from typing import Optional

import moody

from fpga_device_manager import Pins, Constants
from fpga_device_manager.Devices import Output
from fpga_device_manager.Inputs import Input
from fpga_device_manager.device_manager import DeviceManager
from fpga_device_manager.exceptions import DeviceInvalidError, InvalidConfigError

_output_mgr = DeviceManager(device_class=Output)
_input_mgr = DeviceManager(device_class=Input)


def clear() -> None:
    """Resets the configuration by clearing both device managers."""
    _output_mgr.clear()
    _input_mgr.clear()


def outputs() -> DeviceManager:
    """
    Returns the device manager for output devices.
    :return: Output device manager
    """
    return _output_mgr


def inputs() -> DeviceManager:
    """
    Returns the device manager for input devices.
    :return: Input device manager
    """
    return _input_mgr


def load(cfg_filename: str, max_devices: Optional[int] = None) -> None:
    """
    Loads a device configuration from a specified file.
    :param cfg_filename: Name of the file to load the configuration from.
    :param max_devices: Optionally specifies an upper limit for devices.
    """
    global _output_mgr, _input_mgr

    max_devices = max_devices or Constants.MAX_DEVICES

    _output_mgr = DeviceManager(device_class=Output, max_devices=max_devices)
    _input_mgr = DeviceManager(device_class=Input, max_devices=max_devices)

    with open(cfg_filename, "r") as file:
        device_file_data = json.load(file)

    for mgr, dev_list in ((_output_mgr, device_file_data["devices"]), (_input_mgr, device_file_data["inputs"])):
        mgr.load(dev_list)

        # Re-associate inputs
        for dev_input in _input_mgr.all_devices():
            associated_device_id = device_file_data["inputs"][str(dev_input.dev_id)]["associated_device"]
            if associated_device_id is not None:
                device = _output_mgr.get(associated_device_id)
                dev_input.associate(device)


def save(cfg_filename: str) -> None:
    """
    Saves the current device configuration to a file.
    :param cfg_filename: Name of file to save the configuration to.
    """
    data = {
        "devices": _output_mgr.save(),
        "inputs": _input_mgr.save()
    }

    with open(cfg_filename, "w") as file:
        json.dump(data, file, indent=2)


def check() -> None:
    """
    Performs sanity checks on the current configuration. In particular, this checks all device pins for proper
    assignment and all input/output device associations.

    If all checks pass, returns nothing. Otherwise, an InvalidConfigError is returned, passing all error messages along
    with it.
    """
    errors = []

    for mgr in (_output_mgr, _input_mgr):
        for device in mgr.all_devices():
            try:
                device.check_validity()
            except DeviceInvalidError as e:
                errors.append(str(e))

    if len(errors) > 0:
        raise InvalidConfigError(errors)


def export(out_path: str) -> None:
    """
    Exports the current device configuration to Verilog code.
    :param out_path: Path to write Verilog files to
    """
    # Gather devices
    output_devices = list(_output_mgr.all_devices())
    input_devices = list(_input_mgr.all_devices())
    output_max_id = max([dev.dev_id for dev in output_devices])
    input_max_id = max([dev.dev_id for dev in input_devices])

    # Gather device types
    output_device_types = {dev.dev_id: dev.type for dev in output_devices}
    input_device_types = {dev.dev_id: dev.type for dev in input_devices}

    # Gather input device mappings
    input_assignments = {dev.dev_id: dev.associated_device.dev_id for dev in input_devices}

    # Gather and enumerate used pins
    output_pins = [pin for pin in Pins.all() if pin.is_output()]
    input_pins = [pin for pin in Pins.all() if pin.is_input()]

    # Reverse lookup tables for pin indices
    output_pin_indices = {pin.name: index for index, pin in enumerate(output_pins)}
    input_pin_indices = {pin.name: index for index, pin in enumerate(input_pins)}

    # Gather unused pins
    unused_pins = [pin for pin in Pins.all() if not pin.is_assigned()]

    tpl_loader = moody.make_loader(os.path.join(os.path.dirname(__file__), "res", "vtemplates"))

    out_generator = f"{Constants.APP_NAME} {Constants.APP_VERSION}"
    out_timestamp = datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S")
    exports = {
        "devices_out.v": tpl_loader.render("devices_out.v.tpl",
                                           generator=out_generator,
                                           timestamp=out_timestamp,
                                           devices=output_devices,
                                           pin_ids=output_pin_indices,
                                           unused_pins=unused_pins),
        "devices_in.v": tpl_loader.render("devices_in.v.tpl",
                                          generator=out_generator,
                                          timestamp=out_timestamp,
                                          devices=input_devices,
                                          pin_ids=input_pin_indices,
                                          unused_pins=unused_pins),
        "types.v": tpl_loader.render("types.v.tpl",
                                     generator=out_generator,
                                     timestamp=out_timestamp,
                                     max_output_id=output_max_id,
                                     device_types=output_device_types,
                                     input_types=input_device_types,
                                     max_input_id=input_max_id,
                                     input_assignments=input_assignments),
        "pins_out.v": tpl_loader.render("pins_out.v.tpl",
                                        generator=out_generator,
                                        timestamp=out_timestamp,
                                        device_count=output_max_id + 1,
                                        pins=output_pins),
        "pins_in.v": tpl_loader.render("pins_in.v.tpl",
                                       generator=out_generator,
                                       timestamp=out_timestamp,
                                       device_count=len(input_devices),
                                       pins=input_pins),
        "smarthome.ldf": tpl_loader.render("smarthome.ldf.tpl",
                                           device_types=output_device_types.values(),
                                           input_types=input_device_types.values())
    }

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    for filename, text in exports.items():
        filepath = os.path.join(out_path, filename)
        print(f"Writing to {filepath}...")
        with open(filepath, "w") as file:
            file.write(text)
