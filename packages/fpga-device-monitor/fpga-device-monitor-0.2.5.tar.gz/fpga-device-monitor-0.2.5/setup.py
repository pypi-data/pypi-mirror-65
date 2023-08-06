import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='fpga-device-monitor',
    version='0.2.5',
    packages=setuptools.find_packages(),
    url='',
    license='MIT',
    author='Hannes Preiss',
    author_email='sophie@sophieware.net',
    description='A GUI for remotely controlling FPGA devices, serving as an example on how to use the FPGA Bridge API.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=['qtpy', 'PySide2', 'fpga_i2c_bridge'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
