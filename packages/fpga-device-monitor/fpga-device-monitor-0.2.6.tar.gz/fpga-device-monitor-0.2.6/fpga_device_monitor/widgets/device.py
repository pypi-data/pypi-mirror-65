from fpga_i2c_bridge.appliance import I2CAppliance, I2CGenericBinary, I2CDimmer, I2CRGBDimmer, I2CShutter
from fpga_device_monitor.widgets.dimmer_ctrl import DimmerControlWidget
from fpga_device_monitor.widgets.rgb_ctrl import RGBControlWidget
from fpga_device_monitor.widgets.shutter_ctrl import ShutterControlWidget
from fpga_device_monitor.widgets.switch_ctrl import SwitchControlWidget
from fpga_device_monitor.windows.base import BaseWidget


class DeviceWidget(BaseWidget):
    """Widget representing a single FPGA output device."""

    def __init__(self, device: I2CAppliance, *args, **kwargs):
        super(DeviceWidget, self).__init__("device.ui", *args, **kwargs)

        self.device = device
        self.control_widget = None
        self.init_ui()

    def init_ui(self) -> None:
        """Factory method that initializes the control widget, based on the type of device it was instantiated with."""
        self.group.setTitle(str(self.device))

        # Create control widget
        if isinstance(self.device, I2CGenericBinary):
            widget_class = SwitchControlWidget
        elif isinstance(self.device, I2CDimmer):
            widget_class = DimmerControlWidget
        elif isinstance(self.device, I2CRGBDimmer):
            widget_class = RGBControlWidget
        elif isinstance(self.device, I2CShutter):
            widget_class = ShutterControlWidget
        else:
            raise Exception("Unknown device: %s" % str(self.device))

        self.control_widget = widget_class(parent=self)
        self.group.layout().addWidget(self.control_widget)
