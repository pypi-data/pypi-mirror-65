from __future__ import annotations
from abc import ABC
from typing import Any, Tuple

from qtpy.QtWidgets import QWidget, QSpinBox, QSizePolicy
from qtpy.QtCore import Qt

from fpga_device_manager.widgets.colorbutton import ColorButton
from fpga_device_manager.widgets.percent_slider import PercentSlider
from fpga_device_manager.widgets.state_spinbox import StateSpinBox


class DeviceParameter(ABC):
    """Base class for device parameters."""
    def __init__(self, name, display_name=None, description="", value=None, default=None):
        self.name = name
        self.display_name = display_name or name
        self.description = description
        self.default = default
        self.value = value or default or 0

    @staticmethod
    def load(name: str, data: dict) -> DeviceParameter:
        """
        Factory for creating a new device parameter object from JSON data.
        Throws an Exception if the specified parameter type is unknown.
        :param name: Name of parameter
        :param data: JSON data
        :return: Parameter object
        """
        if data["type"] == "int":
            return IntParameter(name=name,
                                description=data.get("description", None),
                                display_name=data.get("name", None),
                                default=data.get("default", None),
                                v_min=data.get("min", 0),
                                v_max=data.get("max", 65535),)
        elif data["type"] == "percent":
            return PercentParameter(name=name,
                                    description=data.get("description", None),
                                    display_name=data.get("name", None),
                                    default=data.get("default", None))
        elif data["type"] == "state":
            return StateParameter(name=name,
                                  description=data.get("description", None),
                                  display_name=data.get("name", None),
                                  default=data.get("default", None))
        elif data["type"] == "color":
            return ColorParameter(name=name,
                                  description=data.get("description", None),
                                  display_name=data.get("name", None),
                                  default=data.get("default", None))
        raise Exception("Unknown parameter type %s" % data["type"])

    def copy(self) -> DeviceParameter:
        """
        Creates a copy of itself.
        :return: Copy parameter
        """
        raise NotImplementedError

    def create_widget(self) -> QWidget:
        """
        Creates a widget used for setting this parameter's value.
        :return: Parameter widget
        """
        widget = self._base_widget()
        widget.setToolTip(self.description)
        widget.sizePolicy().setHorizontalPolicy(QSizePolicy.Maximum)
        return widget

    def _base_widget(self) -> QWidget:
        """Returns the base widget for this parameter."""
        raise NotImplementedError

    def set_value(self, value: Any) -> None:
        """
        Assigns a new value to this parameter. If the value isn't found to be valid, this throws an Exception.
        :param value: The new value for this parameter
        """
        if not self.is_valid(value):
            raise Exception("%s is not a valid value for %s" % (value, self))

        self.value = value

    def get_value_from_widget(self, widget: QWidget) -> Any:
        """
        Extracts the current value from the parameter widget.
        :param widget: Widget to get value from
        """
        raise NotImplementedError

    def is_valid(self, value: Any) -> bool:
        """
        Verifies the validity of the given parameter value.
        :param value: Value to verify
        :return: True if value is valid, False otherwise
        """
        raise NotImplementedError

    def export(self) -> str:
        """Exports a string representation of the parameter's value."""
        raise NotImplementedError

    def __str__(self):
        return f"Parameter {self.name}"


class IntParameter(DeviceParameter):
    """An integer parameter."""
    def __init__(self, v_min, v_max, word_size=16, *args, **kwargs):
        super(IntParameter, self).__init__(*args, **kwargs)
        self.min = v_min
        self.max = v_max
        self.word_size = word_size

    def copy(self) -> IntParameter:
        """
        Creates a copy of itself.
        :return: Copy
        """
        return IntParameter(name=self.name,
                            display_name=self.display_name,
                            description=self.description,
                            v_min=self.min,
                            v_max=self.max,
                            default=self.default,
                            word_size=self.word_size,
                            value=self.value)

    def _base_widget(self) -> QSpinBox:
        """
        Returns a SpinBox with the parameter's settings.
        :return: SpinBox for this parameter
        """
        widget = QSpinBox()
        widget.setToolTip(self.description)
        widget.setMinimum(self.min)
        widget.setMaximum(self.max)
        widget.setAlignment(Qt.AlignRight)
        widget.setValue(self.value)
        return widget

    def get_value_from_widget(self, widget: QSpinBox) -> int:
        """
        Gets the integer value from the specified widget.
        :param widget: SpinBox to extract value from
        :return: Integer value
        """
        return widget.value()

    def is_valid(self, value: int) -> bool:
        """
        Verifies whether the value is valid for this parameter.
        :param value: Value to verify
        :return: True if value is valid, False otherwise
        """
        return self.min <= value <= self.max

    def export(self) -> str:
        """
        Exports the Verilog string representation of this parameter's value.
        :return: String representation
        """
        return f"{self.word_size}'d{self.value}"


class PercentParameter(IntParameter):
    """A parameter that can be set from 0 to 100%."""
    def __init__(self, *args, **kwargs):
        super(PercentParameter, self).__init__(v_min=0, v_max=100, word_size=8, *args, **kwargs)

    def copy(self) -> PercentParameter:
        """
        Creates a copy of itself.
        :return: Copy
        """
        return PercentParameter(name=self.name,
                                display_name=self.display_name,
                                description=self.description,
                                default=self.default,
                                value=self.value)

    def _base_widget(self) -> PercentSlider:
        """
        Creates a PercentSlider for this parameter.
        :return: PercentSlider widget
        """
        widget = PercentSlider(default=self.default)
        return widget

    def get_value_from_widget(self, widget: PercentSlider) -> int:
        """
        Extracts the value from the PercentSlider widget.
        :param widget: PercentSlider widget to extract value from
        :return: Extracted value
        """
        return widget.value


class StateParameter(IntParameter):
    """A parameter representing a raw FPGA device 24-bit state."""
    def __init__(self, *args, **kwargs):
        super(StateParameter,  self).__init__(v_min=0, v_max=0xFFFFFF, word_size=24, *args, **kwargs)

    def copy(self) -> StateParameter:
        """
        Creates a copy of itself.
        :return: Copy
        """
        return StateParameter(name=self.name,
                              display_name=self.display_name,
                              description=self.description,
                              default=self.default,
                              value=self.value)

    def _base_widget(self) -> StateSpinBox:
        """
        Creates a StateSpinBox for this parameter.
        :return: StateSpinBox widget
        """
        widget = StateSpinBox()
        widget.setMinimum(self.min)
        widget.setMaximum(self.max)
        widget.setAlignment(Qt.AlignRight)
        widget.setDisplayIntegerBase(16)
        widget.setPrefix("0x")
        widget.setValue(self.value)
        return widget

    def export(self) -> str:
        """
        Exports the parameter's value to its Verilog string representation.
        :return: Verilog string representation of value
        """
        return "24'h%06x" % self.value


class ColorParameter(StateParameter):
    """A parameter that represents a 24-bit hexadecimal color."""
    def __init__(self, *args, **kwargs):
        super(ColorParameter, self).__init__(*args, **kwargs)

    def copy(self) -> ColorParameter:
        """
        Creates a copy of itself.
        :return: Copy
        """
        return ColorParameter(name=self.name,
                              display_name=self.display_name,
                              description=self.description,
                              default=self.default,
                              value=self.value)

    def _base_widget(self) -> ColorButton:
        """
        Creates a ColorButton for this parameter.
        :return: ColorButton widget
        """
        col_tuple = (self.value >> 16, (self.value >> 8) % 256, self.value % 256)
        widget = ColorButton(default_color=col_tuple)
        return widget

    def get_value_from_widget(self, widget: ColorButton) -> Tuple[int, int, int]:
        """
        Extracts the value from the ColorButton widget.
        :param widget: ColorButton to extract value from
        :return: RGB color triplet
        """
        return (widget.color[0] << 16) + (widget.color[1] << 8) + widget.color[2]
