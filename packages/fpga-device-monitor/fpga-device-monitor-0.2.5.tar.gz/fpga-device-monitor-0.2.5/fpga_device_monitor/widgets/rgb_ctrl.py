from typing import Any

from qtpy.QtCore import Slot, Signal

from fpga_device_monitor.widgets.colorbutton import ColorButton
from fpga_device_monitor.widgets.device_ctrl import DeviceControlWidget
from fpga_device_monitor.windows.base import BaseWidget


class RGBControlWidget(DeviceControlWidget, BaseWidget):
    """A widget for controlling a FPGA RGB Dimmer. Provides a color button that can be used to change the RGB Dimmer's
    RGB color value."""
    def __init__(self, *args, **kwargs):
        super(RGBControlWidget, self).__init__(ui_file="out_rgb.ui", *args, **kwargs)

        self.btn_color.color_chosen.connect(self.send_device_state)
        self.update_widget()

    def update_widget(self) -> None:
        """Updates the widget's style to reflect the RGB Dimmer's current color."""
        self.btn_color: ColorButton
        self.btn_color.set_color(self.state)

    def get_state_from_widget(self) -> Any:
        """Translates the widget's color state into the state value for the RGB device.

        :return RGB color triplet as floats from (0..1)
        """
        return tuple(color / 255 for color in self.btn_color.color)

