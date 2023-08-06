"""Utility base classes for Qt widgets."""

from qtpy import QtWidgets, uic
from os import path


class BaseWindow(QtWidgets.QMainWindow):
    """Base class for Qt MainWindow widgets. Automatically creates a MainWindow widget based on the supplied UI file,
    and assigns all child widgets as attributes to itself."""
    def __init__(self, ui_file, *args, **kwargs):
        super(BaseWindow, self).__init__(*args, **kwargs)
        uic.loadUi(path.join(path.dirname(__file__), "..", "res", "ui", ui_file), self)

        for child in self.findChildren(QtWidgets.QWidget):
            name = child.objectName()
            setattr(self, name, child)


class BaseWidget(QtWidgets.QWidget):
    """Base class for generic Qt widgets. Automatically creates a Qt widget based on the supplied UI file,
    and assigns all child widgets as attributes to itself."""
    def __init__(self, ui_file, *args, **kwargs):
        super(BaseWidget, self).__init__(*args, **kwargs)
        uic.loadUi(path.join(path.dirname(__file__), "..", "res", "ui", ui_file), self)

        for child in self.findChildren(QtWidgets.QWidget):
            name = child.objectName()
            setattr(self, name, child)