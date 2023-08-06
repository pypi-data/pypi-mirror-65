from qtpy.QtCore import Slot
from qtpy.QtWidgets import QSlider

from fpga_device_monitor.windows.base import BaseWidget


class PercentSlider(BaseWidget):
    """A combination of a slider and a label for selecting a percentage value.

    The label automatically updates to display the slider's state.
    """
    def __init__(self, parent, default: int = 0, v_min: int = 0, v_max: int = 100, *args, **kwargs):
        super(PercentSlider, self).__init__("label_slider.ui", *args, **kwargs)
        self.slider: QSlider
        self.value = default

        self.slider.setMinimum(v_min)
        self.slider.setMaximum(v_max)
        self.slider.setValue(default)
        self.refresh()

    def refresh(self) -> None:
        """Updates the label to reflect the currently chosen value."""
        self.label.setText(f"{self.value} %")

    @Slot(int)
    def on_slider_valueChanged(self, new_value: int):
        """Handler for choosing a new value on the slider.

        :param new_value: New value
        """
        self.value = new_value
        self.refresh()
