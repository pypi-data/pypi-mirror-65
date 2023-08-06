from typing import Any

from qtpy.QtCore import Slot, Signal

from fpga_device_monitor.widgets.device_ctrl import DeviceControlWidget
from fpga_device_monitor.widgets.percent_slider import PercentSlider
from fpga_device_monitor.windows.base import BaseWidget


class DimmerControlWidget(DeviceControlWidget, BaseWidget):
    """Control widget for a FPGA Dimmer. Provides a slider that is used to change the Dimmer's brightness."""

    def __init__(self, *args, **kwargs):
        super(DimmerControlWidget, self).__init__(ui_file="out_dimmer.ui", *args, **kwargs)

        self.sld_brightness.slider.valueChanged.connect(self.send_device_state)

    def update_widget(self) -> None:
        """Updates the widget by setting the slider's value to the Dimmer's reported brightness."""
        self.sld_brightness: PercentSlider
        self.sld_brightness.slider.setValue(self.state * 100)

    def get_state_from_widget(self) -> float:
        """Translates the slider's value (0..100) to the Dimmer device state (0..1).

        :return Dimmer brightness value calculated from slider's value"""
        return self.sld_brightness.value / 100
