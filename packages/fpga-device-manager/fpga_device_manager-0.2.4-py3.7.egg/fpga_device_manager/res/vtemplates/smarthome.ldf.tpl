<?xml version="1.0" encoding="UTF-8"?>
<BaliProject version="3.2" title="smarthome" device="LCMXO2-7000HE-5TG144C" default_implementation="smarthome">
    <Options/>
    <Implementation title="smarthome" dir="smarthome" description="smarthome" synthesis="synplify" default_strategy="Strategy1">
        <Options def_top="main"/>
        <Source name="smarthome/source/main.v" type="Verilog" type_short="Verilog">
            <Options top_module="main"/>
        </Source>
        <Source name="smarthome/source/device_controller.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/i2c_controller.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/output_manager.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/input_manager.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/i2c_h.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/i2c_opcodes_h.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/efb.ipx" type="IPX_Module" type_short="IPX">
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/output/out_binary.v" type="Verilog" type_short="Verilog"{% if 1 not in device_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/output/out_pwm.v" type="Verilog" type_short="Verilog"{% if 2 not in device_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/output/out_rgb.v" type="Verilog" type_short="Verilog"{% if 3 not in device_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/output/out_shutter.v" type="Verilog" type_short="Verilog"{% if 4 not in device_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/input/in_button.v" type="Verilog" type_short="Verilog"{% if 1 not in input_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/input/in_toggle.v" type="Verilog" type_short="Verilog"{% if 2 not in input_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/input/in_cycle_dimmer.v" type="Verilog" type_short="Verilog"{% if 3 not in input_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/input/in_cycle_rgb.v" type="Verilog" type_short="Verilog"{% if 4 not in input_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/input/in_shutter.v" type="Verilog" type_short="Verilog"{% if 5 not in input_types %} excluded="TRUE"{% endif %}>
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/bus_arbiter.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/debounce.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/edge_detect.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/pwm.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/modules/timer.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/generated/pins_in.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/generated/pins_out.v" type="Verilog" type_short="Verilog">
            <Options/>
        </Source>
        <Source name="smarthome/source/generated/devices_in.v" type="Verilog" type_short="Verilog" excluded="TRUE">
            <Options/>
        </Source>
        <Source name="smarthome/source/generated/devices_out.v" type="Verilog" type_short="Verilog" excluded="TRUE">
            <Options/>
        </Source>
        <Source name="smarthome/source/generated/types.v" type="Verilog" type_short="Verilog" excluded="TRUE">
            <Options/>
        </Source>
        <Source name="efb_sim/efb_sim.spf" type="Simulation Project File" type_short="SPF">
            <Options/>
        </Source>
        <Source name="smarthome.lpf" type="Logic Preference" type_short="LPF">
            <Options/>
        </Source>
        <Source name="smarthome/smarthome.xcf" type="Programming Project File" type_short="Programming">
            <Options/>
        </Source>
    </Implementation>
    <Strategy name="Strategy1" file="smarthome1.sty"/>
</BaliProject>
