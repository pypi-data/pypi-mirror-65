import os
import sys

from PyQt5.QtWidgets import QApplication, QGraphicsView

from fpga_device_manager import Pins
from fpga_device_manager.widgets.preview import FPGAPreview

if __name__ == '__main__':
    app = QApplication(sys.argv)

    base_data_path = os.path.join(os.path.dirname(__file__), "res", "data")
    Pins.init(os.path.join(base_data_path, "pins.json"))

    image = FPGAPreview()
    image.show()

    sys.exit(app.exec())
