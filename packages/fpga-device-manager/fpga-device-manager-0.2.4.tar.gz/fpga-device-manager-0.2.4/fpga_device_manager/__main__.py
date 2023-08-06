import os
import sys

from qtpy import QtWidgets

from fpga_device_manager import Devices, Inputs, Pins
from fpga_device_manager.windows.main_window import MainWindow

if __name__ == '__main__':
    base_data_path = os.path.join(os.path.dirname(__file__), "res", "data")

    Devices.init(os.path.join(base_data_path, "device_types.json"))
    Inputs.init(os.path.join(base_data_path, "input_types.json"))
    Pins.init(os.path.join(base_data_path, "pins.json"))

    # Create some directories if possible
    for dirname in ("configurations", "generated"):
        try:
            os.mkdir(dirname)
        except FileExistsError:
            pass

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
