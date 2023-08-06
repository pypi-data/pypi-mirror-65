from typing import Union

from qtpy.QtCore import Slot
from qtpy.QtWidgets import QComboBox, QVBoxLayout

from fpga_device_manager import Config
from fpga_device_manager.device_base import DeviceBaseInstance
from fpga_device_manager.device_manager import DeviceManager
from fpga_device_manager.exceptions import DeviceInvalidError
from fpga_device_manager.widgets.device_assoc import DeviceAssociationWidget
from fpga_device_manager.widgets.device_pin import DevicePinWidget
from fpga_device_manager.windows.base import BaseWidget
from fpga_device_manager.windows.device_settings import DeviceSettingsWindow


class DeviceBaseWidget(BaseWidget):
    """A widget representing a device and its state, including several children widgets."""
    def __init__(self, device: Union['Device', 'Output'], main_window: 'MainWindow', manager: DeviceManager,
                 *args, **kwargs):
        super(DeviceBaseWidget, self).__init__("device.ui", *args, **kwargs)

        self.device = device
        self.main_window = main_window
        self.manager = manager

        self.setup_pin_widgets()
        self.refresh()

    def setup_pin_widgets(self) -> None:
        """Sets up widgets for the device's pins."""
        for pin in self.device.pins.values():
            self.lyo_pins.addWidget(DevicePinWidget(device_widget=self, device_pin=pin))

    def refresh(self) -> None:
        """Updates the widget and its children to reflect its current state."""
        self.group.setTitle(self.device.name)

        self.combo_ids: QComboBox
        self.combo_ids.clear()
        self.combo_ids.addItem(str(self.device.dev_id))
        self.combo_ids.addItems(str(i) for i in Config.outputs().available_ids)

        try:
            self.device.check_validity()
            self.group.setStyleSheet("")
        except DeviceInvalidError:
            self.group.setStyleSheet("QGroupBox::title {font-weight: bold; color: red;}")

        self.lyo_pins: QVBoxLayout

        # Refresh children
        for i in range(self.lyo_pins.count()):
            self.lyo_pins.itemAt(i).widget().refresh()

    @Slot()
    def on_btn_rename_clicked(self):
        """Handler for clicking the Rename button."""
        window = DeviceSettingsWindow(self.device)
        window.exec()
        self.refresh()

    @Slot()
    def on_btn_delete_clicked(self):
        """Handler for clicking the Delete button."""
        self.manager.remove_device(self.device.dev_id)
        self.main_window.remove_widget(self.device)

    @Slot(str)
    def on_combo_ids_currentTextChanged(self, new_id: str):
        """
        Handler for changing the device ID combo box.
        :param new_id: Selected device ID
        """
        if new_id != '' and int(new_id) != self.device.dev_id:
            self.manager.move_device(self.device.dev_id, int(new_id))
            self.main_window.refresh()


class OutputWidget(DeviceBaseWidget):
    """A widget representing an output device."""
    def __init__(self, *args, **kwargs):
        super(OutputWidget, self).__init__(manager=Config.outputs(), *args, **kwargs)

    @Slot()
    def on_btn_delete_clicked(self):
        """Handler for clicking the Delete button."""
        self.device.remove_associations()
        super(OutputWidget, self).on_btn_delete_clicked()


class InputWidget(DeviceBaseWidget):
    """A widget representing an input device."""
    def __init__(self, *args, **kwargs):
        super(InputWidget, self).__init__(manager=Config.inputs(), *args, **kwargs)

    def setup_pin_widgets(self) -> None:
        """Sets up widgets for the device's pins and output association."""
        self.lyo_pins.addWidget(DeviceAssociationWidget(device_widget=self))
        super(InputWidget, self).setup_pin_widgets()
