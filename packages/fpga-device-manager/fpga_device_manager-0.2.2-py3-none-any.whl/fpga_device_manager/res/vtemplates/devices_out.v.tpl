{% extends "base.tpl" %}
{% block title %}Output device modules file{% endblock %}
{% block body %}

{% for i, dev in enumerate(devices) %}
/*
    Output device {{dev.dev_id}} ({{dev.name}})
    Type: {{dev.type}}
    Pin(s) used: {{", ".join(pin.assigned_pin.name for pin in dev.pins.values())}}
*/
// Device outputs{% for pin_name, pin in dev.pins.items() %}
wire dev_{{ dev.dev_id }}_{{ pin_name }}_o;
assign pin_signals_o[{{pin_ids[pin.assigned_pin.name]}}] = {% if pin.active_low %}~{% endif %}dev_{{ dev.dev_id }}_{{ pin_name }}_o;{% endfor %}

// Device driver
{{dev.template.driver}} #(
    .DEV_ADDR(8'd{{dev.dev_id}}){% for param_name, param in dev.parameters.items() %},
    .{{param_name.upper()}}({{param.export()}}){% endfor %}
) output_{{dev.dev_id}} ({% if dev.uses_clk %}
    .clk_i        (clk_i),{% endif %}{% if dev.uses_bus %}
    .bus_access_i (bus_access_i[{{i}}]),
    .bus_req_o    (bus_requests_o[{{i}}]),
    .bus_cmd_o    (bus_cmd_o),{% endif %}
    .state_i      (device_states_i[{{dev.dev_id * 24 + 23}}:{{dev.dev_id * 24}}]){% for pin_name, pin in dev.pins.items() %},
    .{{pin_name}}_o(dev_{{dev.dev_id}}_{{pin_name}}_o){% endfor %}
);
{% endfor %}
{% endblock %}