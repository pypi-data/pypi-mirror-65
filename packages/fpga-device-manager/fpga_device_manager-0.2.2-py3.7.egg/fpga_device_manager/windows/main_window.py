from functools import partial

from qtpy.QtCore import Slot
from qtpy.QtWidgets import QMenu, QFileDialog

from fpga_device_manager import Devices, Pins, Popup, Inputs, Config, Constants
from fpga_device_manager.Devices import Output
from fpga_device_manager.Inputs import Input
from fpga_device_manager.device_base import DeviceBaseTemplate, DeviceBaseInstance
from fpga_device_manager.exceptions import InvalidConfigError
from fpga_device_manager.widgets.device_widget import OutputWidget, InputWidget
from fpga_device_manager.windows.base import BaseWindow
from fpga_device_manager.windows.device_settings import DeviceSettingsWindow


class MainWindow(BaseWindow):
    """The application's main window."""
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__("main.ui", *args, **kwargs)

        self.dirty = False
        self.device_widgets = {}

        self.init_btn_menu()
        self.init_colors()

        self.refresh()

    def set_dirty(self) -> None:
        """Sets the dirty flag, which prompts to save on several actions that would otherwise lose data."""
        self.dirty = True
        self.update_title()

    def clear_dirty(self) -> None:
        """Clears the dirty flag."""
        self.dirty = False
        self.update_title()

    def init_btn_menu(self) -> None:
        """Initializes the buttons for adding devices."""
        dev_menu = QMenu()
        input_menu = QMenu()

        for tpl_id, tpl in Devices.list_templates():
            dev_menu.addAction(f"Add {tpl.name}").triggered.connect(
                partial(self.add_device_template, tpl)
            )

        for tpl_id, tpl in Inputs.list_templates():
            input_menu.addAction("Add %s" % tpl.name).triggered.connect(
                partial(self.add_device_template, tpl, True)
            )

        self.btn_add_device.setMenu(dev_menu)
        self.btn_add_input.setMenu(input_menu)

        print(self.btn_add_device.menu())
        print(self.btn_add_input.menu())

    def init_colors(self) -> None:
        """Initializes the preview key colors."""
        for frame, color_type in {
            self.fr_reserved: Pins.PIN_RESERVED,
            self.fr_inputs: Pins.PIN_OCCUPIED_INPUT,
            self.fr_devices: Pins.PIN_OCCUPIED_DEVICE,
            self.fr_available: Pins.PIN_AVAILABLE,
            self.fr_available_pwm: Pins.PIN_AVAILABLE_PWM
        }.items():
            frame.setStyleSheet("background-color: rgb(%d, %d, %d);" % Pins.color(color_type)[0:3])

    def refresh(self) -> None:
        """Updates all widgets."""
        self.update_labels()
        self.update_buttons()
        self.update_preview()
        self.update_widgets()
        self.update_title()

    def update_labels(self) -> None:
        """Updates the window's labels."""
        self.tabs.setTabText(0, "Appliances (%d)" % (len(Config.outputs().devices)))
        self.tabs.setTabText(1, "Sensors (%d)" % (len(Config.inputs().devices)))

        self.lb_pins_used.setText(str(sum(pin.is_output() for pin in Pins.all())))
        self.lb_pins_input.setText(str(sum(pin.is_input() for pin in Pins.all())))
        self.lb_pins_free.setText(str(sum(not pin.is_assigned() and not pin.supports_pwm for pin in Pins.all())))
        self.lb_pins_free_pwm.setText(str(sum(not pin.is_assigned() and pin.supports_pwm for pin in Pins.all())))

    def update_buttons(self) -> None:
        """Updates the window's buttons."""
        self.btn_save.setEnabled(Config.outputs().has_devices() or Config.inputs().has_devices())
        self.btn_export.setEnabled(Config.outputs().has_devices() and Config.inputs().has_devices())
        self.btn_clear.setEnabled(Config.outputs().has_devices() or Config.inputs().has_devices())
        self.btn_add_device.setEnabled(not Config.outputs().has_max_devices())
        self.btn_add_input.setEnabled(not Config.inputs().has_max_devices())

    def update_widgets(self) -> None:
        """Updates all device widgets."""
        for widget in self.device_widgets.values():
            widget.refresh()

    def update_preview(self) -> None:
        """Updates the pin preview."""
        self.img_pins.update()

    def update_title(self) -> None:
        """Updates the window's title."""
        dirty = self.dirty and "*" or ""
        self.setWindowTitle(f"{Constants.APP_NAME} {Constants.APP_VERSION}{dirty}")

    def load(self, filename: str) -> None:
        """
        Loads a device configuration.
        :param filename: Name of configuration file to load
        """
        try:
            self.reset()
            Config.load(filename)

            self.add_all_widgets()
            self.clear_dirty()
            self.update_title()

        except Exception as e:
            Popup.alert(title=f"Failed to load {filename}",
                        message=str(e))
            raise

    def save(self, filename: str) -> None:
        """
        Saves the current device configuration.
        :param filename: Name of file to save to
        """
        try:
            Config.save(filename)
            self.clear_dirty()

        except Exception as e:
            Popup.error(title=f"Failed to save {filename}", ex=e)

    def export(self, path: str) -> None:
        """
        Exports the current device configuration to Verilog code.
        :param path: Path to output Verilog files to
        """
        try:
            Config.export(path)
            Popup.info(title="Successfully exported",
                       message=f"Verilog code has been successfully written to {path}.")

        except InvalidConfigError as e:
            Popup.alert(title=f"Failed to export",
                        message=str(e))

    def reset(self) -> None:
        """Resets the configuration and window."""
        Config.clear()
        self.remove_all_widgets()
        self.clear_dirty()

    def closeEvent(self, event) -> None:
        """
        Handler that gets executed when the window is about to close. If the dirty flag is set, this will prompt the
        user to save.
        :param event: Qt close event
        """
        if self.dirty:
            Popup.confirm(title="You have unsaved changes",
                          message="Are you sure you want to quit?",
                          additional_text="You will lose all unsaved changes.",
                          on_yes=lambda: event.accept(),
                          on_no=lambda: event.ignore())

    def add_device_template(self, tpl: DeviceBaseTemplate, is_input: bool = False) -> None:
        """
        Adds a new device, based on the supplied device template.
        :param tpl: The device template to base the new device off of
        :param is_input: Whether this is an input device or not
        """
        if is_input:
            dev_class = Input
            manager = Config.inputs()
            add_widget_call = self.add_input_widget
        else:
            dev_class = Output
            manager = Config.outputs()
            add_widget_call = self.add_output_widget

        try:
            device = dev_class.create_from_template(dev_name=tpl.name, dev_type=tpl.type)
            window = DeviceSettingsWindow(device)
            if window.exec_() == window.Accepted:
                for pin in device.pins.values():
                    try:
                        Pins.assign(Pins.get_next_available_pin(pin).name, pin)
                    except Exception as e:
                        print("could not assign pin %s: %s" % (pin.name, e))

                    if is_input:
                        try:
                            device.associate(next(Config.outputs().filter(device.template.compatible_devices)))
                        except StopIteration:
                            print("could not associate device: no compatible devices")
                manager.add_device(device)
                add_widget_call(device)
        except Exception as e:
            Popup.error(title=f"Failed to add device", ex=e)

    def add_output_widget(self, device: Output, refresh: bool = True) -> None:
        """
        Adds a widget for the specified output device.
        :param device: Output device to add widget for
        :param refresh: Whether the window should refresh after adding
        """
        widget = OutputWidget(device, main_window=self)
        self.device_widgets[device] = widget
        self.tab_devices.device_list.layout().addWidget(widget)
        if refresh:
            self.refresh()

    def add_input_widget(self, input_device: Input, refresh: bool = True) -> None:
        """
        Adds a widget for the specified input device.
        :param input_device: Input device to add widget for
        :param refresh: Whether the window should refresh after adding
        """
        widget = InputWidget(input_device, main_window=self)
        self.device_widgets[input_device] = widget
        self.tab_inputs.device_list.layout().addWidget(widget)
        if refresh:
            self.refresh()

    def add_all_widgets(self) -> None:
        """Adds widgets for all devices, based on the current configuration."""
        for mgr, call in ((Config.outputs(), self.add_output_widget), (Config.inputs(), self.add_input_widget)):
            for device in mgr.all_devices():
                call(device, refresh=False)

        self.refresh()

    def remove_widget(self, device: DeviceBaseInstance, refresh: bool = True) -> None:
        """
        Removes a widget belonging to a device. This is usually done to remove a device from the configuration.
        :param device: Device widget to remove
        :param refresh: Whether the window should refresh after removing
        """
        try:
            self.device_widgets[device].close()
            del self.device_widgets[device]
            if refresh:
                self.refresh()
        except KeyError:
            print(f"attempted to close nonexistent widget for device {device}")

    def remove_all_widgets(self) -> None:
        """Removes all device widgets."""
        for device in self.device_widgets.copy().keys():
            self.remove_widget(device, refresh=False)

        self.refresh()

    @Slot()
    def on_btn_clear_clicked(self):
        """Handler for clicking the Clear button. This prompts the user whether all devices should be removed."""
        Popup.confirm(title="Clear all devices",
                      message="Are you sure you wish to remove all devices and inputs?",
                      on_yes=self.reset)

    @Slot()
    def on_btn_load_clicked(self):
        """Handler for clicking the Load button. This opens a file selection dialog for loading a configuration."""
        filename = QFileDialog.getOpenFileName(parent=self,
                                               caption="Load device data",
                                               dir="./configurations",
                                               filter="JSON device data (*.json)")[0]

        # Cancelling results in filename being ''
        if filename != '':
            self.load(filename)

    @Slot()
    def on_btn_save_clicked(self):
        """Handler for clicking the Save button. This opens a file selection dialog for saving a configuration."""
        filename = QFileDialog.getSaveFileName(parent=self,
                                               caption="Load device data",
                                               dir="./configurations",
                                               filter="JSON device data (*.json)")[0]

        # Cancelling results in filename being ''
        if filename != '':
            self.save(filename)

    @Slot()
    def on_btn_export_clicked(self):
        """Handler for clicking the Export button. This performs some sanity checks on the current configuration,
        and if passed opens a directory selection dialog for exporting Verilog code.
        """
        # Verify device settings
        try:
            Config.check()
            path = QFileDialog.getExistingDirectory(parent=self,
                                                    caption="Export verilog code",
                                                    dir="./generated")

            if path != '':
                self.export(path)

        except InvalidConfigError as e:
            Popup.alert(title="Export failed",
                        message="\n".join(e.errors),
                        additional_text="Please check your configuration and try again.")
            return
