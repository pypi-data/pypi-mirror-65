{% extends "base.tpl" %}
{% block title %}Device type file{% endblock %}
{% block body %}
localparam device_types = {
    {{", ".join(str(x) for x in reversed(device_types))}}
};

// Input -> Output device map
localparam io_map = {
    {{", ".join(str(x) for x in reversed(io_map))}}
};{% endblock %}
