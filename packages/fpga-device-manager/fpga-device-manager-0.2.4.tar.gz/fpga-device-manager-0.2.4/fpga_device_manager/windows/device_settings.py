import re

from qtpy.QtCore import Slot
from qtpy.QtWidgets import QFormLayout

from fpga_device_manager import Popup
from fpga_device_manager.device_base import DeviceBaseInstance
from fpga_device_manager.windows.base import BaseDialog


class DeviceSettingsWindow(BaseDialog):
    """A dialog for setting a device's name and parameters."""
    def __init__(self, device: DeviceBaseInstance, *args, **kwargs):
        super(DeviceSettingsWindow, self).__init__("device_settings.ui", *args, **kwargs)
        self.device = device

        proto = device.template
        self.grp_properties.setTitle(proto.name)
        self.lb_description.setText(proto.description)
        self.txt_dev_name.setText(device.name or proto.name)

        self.param_widgets = {}
        self.setup_property_widgets()

    def setup_property_widgets(self):
        """Sets up widgets for all of the device's properties."""
        layout: QFormLayout = self.grp_properties.layout()
        for param_name, param in self.device.parameters.items():
            param_widget = param.create_widget()
            self.param_widgets[param_name] = param_widget
            layout.addRow(param.display_name, param_widget)

    def is_valid_name(self) -> bool:
        """
        Checks whether the chosen name is a valid name for the device.
        A name is valid if it contains between 1 and 60 alphanumeric characters, spaces or underscores.
        :return: True if the chosen name is valid
        """
        return re.search(r"^[a-zA-Z0-9_\- ]{1,60}$", self.txt_dev_name.text()) is not None

    @Slot()
    def accept(self):
        """Handler for pressing OK on the dialog.

        Validates the device's name and parameters.
        """
        # Validate name
        name = self.txt_dev_name.text()
        if not self.is_valid_name():
            Popup.alert(title="Invalid name",
                        message="The name \"%s\" is invalid." % name,
                        additional_text="A device name can only contain up 60 alphanumeric characters, hyphens, "
                                        "underscores and spaces and must not be empty.")
            return

        # Validate and set parameters
        try:
            for param_name, param in self.device.parameters.items():
                param.set_value(param.get_value_from_widget(self.param_widgets[param_name]))
        except Exception as e:
            Popup.alert(title="Invalid parameter", message=str(e))
            return

        # Set name and accept
        self.device.name = name
        super().accept()
