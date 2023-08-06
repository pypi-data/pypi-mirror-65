# fpga_device_manager
A GUI for managing device configurations for a FPGA Smart Home project that was created as part of a Bachelor's thesis on the subject.

Generates Verilog code for use with the Smart Home FPGA.

A more comprehensive description will follow shortly.

## Installation
```
pip install fpga-device-manager
```

## Usage
```
python -m fpga_device_manager
```

Generated Verilog code as well as the Lattice `.ldf` file will be exported to the `generated` directory and will have to be copied to the Lattice project manually (for now.)