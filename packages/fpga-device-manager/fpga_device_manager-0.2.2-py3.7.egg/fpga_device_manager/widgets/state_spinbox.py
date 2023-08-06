from qtpy.QtWidgets import QSpinBox


class StateSpinBox(QSpinBox):
    """
    A QSpinBox that displays 24-bit hexadecimal values.
    """
    def __init__(self, *args, **kwargs):
        super(StateSpinBox, self).__init__(*args, **kwargs)
        self.setStyleSheet("QSpinBox {  font-family: monospace }")

    def textFromValue(self, v: int) -> str:
        """
        Converts a value into its text representation.
        :param v: Value to convert
        :return: Converted text
        """
        return ("%06x" % v).upper()
