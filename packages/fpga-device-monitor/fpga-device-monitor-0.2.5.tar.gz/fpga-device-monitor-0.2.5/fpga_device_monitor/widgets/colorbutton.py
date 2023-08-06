

from qtpy.QtCore import Slot, Signal
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QPushButton, QColorDialog
from typing import Tuple


class ColorButton(QPushButton):
    """A button for selecting a single color.

    The button's color will display the color chosen.  Additionally; the label reflects the hexcode of the color.
    """

    color_chosen = Signal(int, int, int)

    def __init__(self, parent, default_color: Tuple[int, int, int] = (0, 0, 0), *args, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)
        self.color = default_color
        self.clicked.connect(self.show_color_dialog)
        self.refresh()

    def refresh(self):
        """Updates the button's style to reflect the currently chosen color."""
        if self.color == (0, 0, 0):
            self.setText("(off)")
            self.setStyleSheet("")
        else:
            hex_col = ("#%02x%02x%02x" % self.color).upper()
            self.setText(hex_col)
            self.setStyleSheet(f"background-color: {hex_col};")

    def set_color(self, color: Tuple[int, int, int]) -> None:
        """
        Sets the button's current color.
        :param color: Color triplet (Tuple of R, G, B values in the 0..255 range)
        """
        self.color = color
        self.refresh()

    @staticmethod
    def encode_qcolor(color: Tuple[int, int, int]):
        """
        Translates the given color triplet into a QColor.
        :param color: Color triplet (Tuple of R, G, B values ranging from 0 to 255 each)
        :return: QColor corresponding to given color triplet
        """
        return QColor(color[0], color[1], color[2])

    @staticmethod
    def decode_qcolor(color: QColor):
        """
        Translates the given QColor into a RGB color triplet.
        :param color: QColor to translate
        :return: RGB color triplet corresponding to given QColor
        """
        return color.red(), color.green(), color.blue()

    @Slot()
    def show_color_dialog(self):
        """Displays a dialog for choosing a new color."""
        color_dlg = QColorDialog()
        color_dlg.setCurrentColor(self.encode_qcolor(self.color))
        if color_dlg.exec() == color_dlg.Accepted:
            self.color = self.decode_qcolor(color_dlg.currentColor())
            self.refresh()
            self.color_chosen.emit(*self.color)
