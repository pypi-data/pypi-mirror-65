"""Main executable of the FPGA Device Monitor."""

import argparse
import sys

from qtpy import QtWidgets

from fpga_i2c_bridge import I2CBridge
from fpga_device_monitor.windows.main import MainWindow

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--bus", default="1")
    argparser.add_argument("--addr", default="3E")
    argparser.add_argument("--dummy", action="store_true")
    args = vars(argparser.parse_args())

    i2c_bridge = I2CBridge(i2c_dummy=args['dummy'],
                           i2c_addr=int(args['addr'], base=16),
                           i2c_bus=int(args['bus']))

    if args['dummy']:
        pass

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(i2c_bridge)
    window.show()
    sys.exit(app.exec_())
