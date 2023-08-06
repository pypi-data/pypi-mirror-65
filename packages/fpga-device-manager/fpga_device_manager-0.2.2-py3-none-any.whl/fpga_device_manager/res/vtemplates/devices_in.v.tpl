{% extends "base.tpl" %}
{% block title %}Input device modules file{% endblock %}
{% block body %}
{% for dev in devices %}
/*
    Input {{dev.dev_id}} ({{dev.name}})
    Type: {{dev.type}}
    Pin(s) used: {{", ".join(pin.assigned_pin.name for pin in dev.pins.values())}}
    Associated with output device {{dev.associated_device.dev_id}} ({{dev.associated_device.name}})
*/
{{dev.template.driver}} #(
    .DEV_ADDR(8'd{{dev.dev_id}}){% for param_name, param in dev.parameters.items() %},
    .{{param_name.upper()}}({{param.export()}}){% endfor %}
) input_{{dev.dev_id}} ({% if dev.uses_clk %}
    .clk_i        (clk_i),{% endif %}
    .bus_access_i (bus_access_i[{{dev.dev_id}}]),
    .bus_req_o    (bus_requests_o[{{dev.dev_id}}]),
    .bus_cmd_o    (bus_cmd_o){% for pin_name, pin in dev.pins.items() %},
    .{{pin_name}}_i    ({% if pin.active_low %}~{% endif %}input_signals_i[{{pin_ids[pin.assigned_pin.name]}}]){% endfor %}
);
{% endfor %}
{% if len(devices) < 2 %}
// Fill unused bus request slot
assign bus_requests_o[1] = 1'b0;
{% endif %}
{% endblock %}