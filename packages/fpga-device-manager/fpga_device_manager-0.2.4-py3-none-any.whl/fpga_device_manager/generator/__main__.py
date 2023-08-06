import argparse
import os
import sys

from fpga_device_manager import Devices, Inputs, Pins, Config
from fpga_device_manager.exceptions import InvalidConfigError, DeviceLoadError


def fail(err_msg: str = ""):
    if err_msg:
        sys.stderr.write(err_msg + "\n")
    sys.exit(1)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--output",
                           default="./generated",
                           help="Path where the generated files should be output to.")
    argparser.add_argument("config_file",
                           help="File containing device configuration.")

    args = vars(argparser.parse_args())

    base_data_path = os.path.join(os.path.dirname(__file__), "..", "res", "data")

    Devices.init(os.path.join(base_data_path, "device_types.json"))
    Inputs.init(os.path.join(base_data_path, "input_types.json"))
    Pins.init(os.path.join(base_data_path, "pins.json"))

    try:
        Config.load(args['config_file'])
    except DeviceLoadError as e:
        fail(f"An error occurred while loading the configuration: {e}")

    try:
        Config.check()
        Config.export(args['output'])

    except InvalidConfigError as e:
        error_str = ""
        for error in e.errors:
            error_str += f"\n - {error}"

        fail(f"The configuration is not valid: {error_str}")

    except Exception as e:
        fail(f"An error occurred: {e}")

    print(f"Successfully exported Verilog code to {os.path.abspath(args['output'])}")
