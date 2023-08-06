{% extends "base.tpl" %}
{% block title %}Input pin assignment file{% endblock %}
{% block body %}
{% if pins %}
// Number of device IDs
// ATTN: Has to be at least 2 for all components to work.
//       If less or no devices are present, dummy devices will be used instead.
`define NUM_INPUTS {{max(2, device_count)}}

// Number of input pins
`define NUM_INPUT_PINS {{len(pins)}}

// Pin list
`define INPUT_PINS {{", ".join("pin_%s" % pin.name for pin in pins)}}

// Pin to Signal map
`define INPUT_ASSIGNMENTS{% for pin_id, pin in enumerate(pins) %} \
    assign input_signals[{{pin_id}}] = pin_{{pin.name}};{% endfor %}
{% endif %}
{% endblock %}