"""The main application window of the monitoring application."""


from datetime import datetime
from typing import Any

from qtpy.QtCore import Slot
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem

from fpga_i2c_bridge import I2CBridge
from fpga_i2c_bridge.appliance import I2CAppliance
from fpga_i2c_bridge.sensor import I2CPassthroughSensor, I2CShutterControlSensor, I2CSensor, I2CBinarySensor

from fpga_device_monitor.widgets.device import DeviceWidget
from fpga_device_monitor.windows.base import BaseWindow


class MainWindow(BaseWindow):
    def __init__(self, i2c_bridge: I2CBridge, *args, **kwargs):
        super(MainWindow, self).__init__("main.ui", *args, **kwargs)

        self.i2c = i2c_bridge
        self.device_widgets = {}  # type: dict[int, DeviceWidget]
        self.add_devices()

        self.init_log_table()

        @self.i2c.register_update()
        def on_update(device):
            """Handler for incoming Update events. Inserts a new log entry and updates the widget corresponding
            to the device that reported an update."""
            self.log_update(device, device.state)
            self.device_widgets[device.device_id].control_widget.update_state(new_state=device.state)

        for sensor_id, sensor_dev in self.i2c.sensors.items():
            if isinstance(sensor_dev, I2CShutterControlSensor):
                @sensor_dev.register_full_down_handler()
                def handler():
                    self.log_sensor(sensor_dev, "Full down press")

                @sensor_dev.register_full_up_handler()
                def handler():
                    self.log_sensor(sensor_dev, "Full up press")

                @sensor_dev.register_short_down_handler()
                def handler():
                    self.log_sensor(sensor_dev, "Short down press")

                @sensor_dev.register_short_up_handler()
                def handler():
                    self.log_sensor(sensor_dev, "Short up press")

            elif isinstance(sensor_dev, I2CBinarySensor):
                @sensor_dev.register_event_handler()
                def handler(event_data: int):
                    self.log_sensor(sensor_dev, f"Received state: {event_data}")

    def add_devices(self) -> None:
        """Adds widgets for the found devices."""
        for device in self.i2c.appliances.values():
            widget = DeviceWidget(device)
            self.lyo_devices.addWidget(widget)
            self.device_widgets[device.device_id] = widget

    def init_log_table(self) -> None:
        """Initializes the log view by formatting the widget."""
        self.tbl_log: QTableWidget
        self.tbl_log.setHorizontalHeaderLabels(["Time", "Type", "Event data"])
        self.tbl_log.setColumnWidth(0, 60)
        self.tbl_log.setColumnWidth(1, 50)

    def insert_log(self, log_type: str, log_text: str) -> None:
        """
        Inserts a new log entry into the log view.
        :param log_type: Type of log entry, either "Update" or "Input"
        :param log_text: Text of log entry
        """
        self.tbl_log: QTableWidget
        cell_time = QTableWidgetItem(datetime.strftime(datetime.now(), "%H:%M:%S"))
        cell_type = QTableWidgetItem(log_type)
        cell_log = QTableWidgetItem(log_text)

        row_count = self.tbl_log.rowCount()
        self.tbl_log.setRowCount(row_count + 1)
        self.tbl_log.setItem(row_count, 0, cell_time)
        self.tbl_log.setItem(row_count, 1, cell_type)
        self.tbl_log.setItem(row_count, 2, cell_log)

        self.tbl_log.scrollToBottom()

    def log_update(self, device: I2CAppliance, new_state: Any) -> None:
        """Inserts a new Update event log entry."""
        self.insert_log("Update", "[%s] New state: %s (0x%06x)" % (device, new_state, device._encode_state(new_state)))

    def log_sensor(self, sensor: I2CSensor, event_text: str) -> None:
        """Inserts a new Input event log entry."""
        self.insert_log("Input", "[Input %s] %s" % (sensor, event_text))

    @Slot()
    def on_btn_poll_clicked(self):
        """Handler for clicking the Poll button. Performs a single poll instruction."""
        self.i2c.poll()

    @Slot()
    def on_btn_reset_clicked(self):
        """Handler for clicking the Reset button. This causes the bridge to perform a reset command.
        All device widgets will be removed and then read again from the bridge."""
        for widget in self.device_widgets.values():
            widget.close()

        self.device_widgets.clear()
        self.i2c.reset()
        self.add_devices()

    @Slot()
    def on_btn_quit_clicked(self):
        """Handler for clicking the Quit button. Exits the application."""
        self.close()

    @Slot(int)
    def on_chk_polling_stateChanged(self, state: int):
        """Handler for (un)checking the auto-polling checkbox. Toggles auto-polling on and off."""
        if state == 0:
            self.i2c.stop_polling()
        else:
            self.i2c.start_polling()