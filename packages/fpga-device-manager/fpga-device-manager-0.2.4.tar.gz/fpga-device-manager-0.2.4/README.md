# FPGA Device Manager
A GUI for managing device configurations for a Smart Home FPGA solution that was created as part of a Bachelor's thesis.

This application aids you in creating a device configuration for a Smart Home FPGA and automatically generates the corresponding Verilog code.

## Installation
```
pip install fpga-device-manager
```

## Usage
To launch the GUI, execute:
```
python -m fpga_device_manager
```

- The generated Verilog `.v` files will have to be copied manually to the `smarthome/source/generated` folder of the Lattice Diamond project.
- The generated `smarthome.ldf` file has to be copied manually to the root folder of the Lattice Diamond project.

### Command-line generation
Verilog code can be generated from the command line like this:
```
python -m fpga_device_manager.generator --output=./generated configuration.json
```

## Valid configurations
A valid configuration needs:

- at least one appliance
- at least one sensor
- every sensor to be associated with an appliance