from abc import ABC
from typing import Any

from qtpy.QtCore import Signal

from fpga_device_monitor import Popup
from fpga_device_monitor.windows.base import BaseWidget


class DeviceControlWidget(BaseWidget):
    """Abstract base class for a device control widget. Provides an interface for translating the widget's state to a
    device state and vice versa."""

    external_update = Signal()

    def __init__(self, parent: 'DeviceWidget', ui_file: str, *args, **kwargs):
        super(DeviceControlWidget, self).__init__(ui_file, *args, **kwargs)
        self.parent = parent
        self.state = parent.device.state
        self.external_update.connect(self.update_widget)
        self.update_widget()

    def update_state(self, new_state: Any) -> None:
        """
        Updates the widget's state, based on the supplied device state.
        This method should be called when a device updates its state externally; i.e. on its own.
        :param new_state: The device's new state. This must be a valid state for the device this widget is based on.
        """
        self.state = new_state
        self.external_update.emit()

    def send_device_state(self) -> None:
        """
        Updates the associated device with the widget's current state.
        This method should be called after the widget's state has been changed by the user.
        """
        try:
            self.parent.device.set_state(self.get_state_from_widget())
        except Exception as e:
            Popup.error(title="Exception", ex=e)

    def get_state_from_widget(self) -> Any:
        """Translates the widget's state to the corresponding device state."""
        raise NotImplementedError()

    def update_widget(self) -> None:
        """Updates the widget. This method will be called whenever the device's state updates externally,
        and should update the widget's state accordingly."""
        raise NotImplementedError()

