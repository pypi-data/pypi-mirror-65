{% extends "base.tpl" %}
{% block title %}Output pin assignment file{% endblock %}
{% block body %}
// Number of device IDs (including unused)
`define NUM_OUTPUTS {{device_count}}

// Number of input pins
`define NUM_OUTPUT_PINS {{len(pins)}}

// Pin list
`define OUTPUT_PINS {{", ".join("pin_%s" % pin.name for pin in pins)}}

// Pin to Signal map
`define OUTPUT_ASSIGNMENTS{% for pin_id, pin in enumerate(pins) %} \
    assign pin_{{pin.name}} = output_signals[{{pin_id}}];{% endfor %}
{% endblock %}