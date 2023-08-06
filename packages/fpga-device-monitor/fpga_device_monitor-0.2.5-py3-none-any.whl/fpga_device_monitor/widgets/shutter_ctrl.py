import os
from typing import Any

from PySide2.QtGui import QIcon
from qtpy.QtCore import Slot, Signal
from qtpy.QtWidgets import QPushButton

from fpga_i2c_bridge.appliance import I2CShutter
from fpga_device_monitor.widgets.device_ctrl import DeviceControlWidget


def get_icon_path(icon: str) -> str:
    return os.path.join(__file__, '..', '..', 'res', 'icons', icon)


class ShutterControlWidget(DeviceControlWidget):
    """A widget for controlling a FPGA Shutter. This widget provides buttons for moving the Shutter up and down,
    either fully or by a single unit of movement; as well as stopping it."""
    def __init__(self, *args, **kwargs):
        super(ShutterControlWidget, self).__init__(ui_file="out_shutter.ui", *args, **kwargs)

        self.btn_up_full.setIcon(QIcon(get_icon_path('up_full.png')))
        self.btn_up.setIcon(QIcon(get_icon_path('up.png')))
        self.btn_down.setIcon(QIcon(get_icon_path('down.png')))
        self.btn_down_full.setIcon(QIcon(get_icon_path('down_full.png')))

    def update_widget(self) -> None:
        """Updates the widget by pushing the appropriate button corresponding to the current state of the Shutter."""
        if self.state == I2CShutter.State.UP_FULL:
            widget = self.btn_up_full
        elif self.state == I2CShutter.State.UP_ONCE:
            widget = self.btn_up
        elif self.state == I2CShutter.State.IDLE:
            widget = self.btn_stop
        elif self.state == I2CShutter.State.DOWN_ONCE:
            widget = self.btn_down
        else:
            widget = self.btn_down_full

        widget.setChecked(True)
        self.deactivate_except(widget)

    def get_state_from_widget(self) -> Any:
        """Returns the device state corresponding to the button of the widget that is currently pressed.

        :return Shutter state"""
        return (self.btn_up_full.isChecked() and I2CShutter.State.UP_FULL or
                self.btn_up.isChecked() and I2CShutter.State.UP_ONCE or
                self.btn_stop.isChecked() and I2CShutter.State.IDLE or
                self.btn_down.isChecked() and I2CShutter.State.DOWN_ONCE or
                I2CShutter.State.DOWN_FULL)

    def deactivate_except(self, except_btn: QPushButton) -> None:
        """Activates the supplied button and deactivates all other buttons.

        :param except_btn: Button that should be pressed"""
        for btn in (self.btn_up_full, self.btn_up, self.btn_stop, self.btn_down, self.btn_down_full):
            if btn == except_btn:
                continue
            btn.setChecked(False)


    @Slot()
    def on_btn_up_full_clicked(self):
        """Handler for pressing the 'Move Shutter up fully' button."""
        self.deactivate_except(self.btn_up_full)
        self.send_device_state()

    @Slot()
    def on_btn_up_clicked(self):
        """Handler for pressing the 'Move Shutter up once' button."""
        self.deactivate_except(self.btn_up)
        self.send_device_state()

    @Slot()
    def on_btn_stop_clicked(self):
        """Handler for pressing the 'Stop Shutter' button."""
        self.deactivate_except(self.btn_stop)
        self.send_device_state()

    @Slot()
    def on_btn_down_clicked(self):
        """Handler for pressing the 'Move Shutter down once' button."""
        self.deactivate_except(self.btn_down)
        self.send_device_state()

    @Slot()
    def on_btn_down_full_clicked(self):
        """Handler for pressing the 'Move Shutter down fully' button."""
        self.deactivate_except(self.btn_down_full)
        self.send_device_state()
