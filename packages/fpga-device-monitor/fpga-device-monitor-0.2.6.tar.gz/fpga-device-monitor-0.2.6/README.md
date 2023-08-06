# fpga_device_monitor
A GUI for remotely controlling a Smart Home FPGA solution that was created as part of a Bachelor's thesis.

## Installation
```
pip install fpga-device-monitor
```

## Usage
To run the monitor on a device with I2C support and a connected Smart Home FPGA:
```
python -m fpga_device_monitor
```

To run with simulated dummy devices, run instead:
```
python -m fpga_device_monitor --dummy
```

Use `--bus` and `--addr` to adjust I2C bus number and FPGA device address, respectively. See `--help`.

## Related projects

- [fpga-i2c-bridge](https://pypi.org/project/fpga-i2c-bridge/): Smart Home FPGA API and I2C shell
- [fpga-device-manager](https://pypi.org/project/fpga-device-manager/): Smart Home FPGA device manager