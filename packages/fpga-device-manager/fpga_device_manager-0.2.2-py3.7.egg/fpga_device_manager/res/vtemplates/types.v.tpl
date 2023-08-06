{% extends "base.tpl" %}
{% block title %}Device type file{% endblock %}
{% block body %}

function [7:0] get_device_type(input reg [7:0] device_id);
	case (device_id){% for dev_id, dev_type in device_types.items() %}
		8'd{{dev_id}}: get_device_type = 8'd{{dev_type}};{% endfor %}
		default: get_device_type = 8'd0;
	endcase
endfunction

function [7:0] get_input_type(input reg [7:0] input_id);
	case (input_id){% for input_id, input_type in input_types.items() %}
		8'd{{input_id}}: get_input_type = 8'd{{input_type}};{% endfor %}
		default: get_input_type = 8'd0;
	endcase
endfunction

function [7:0] get_io_target(input reg [7:0] input_id);
	case (input_id){% for input_id, input_target in input_assignments.items() %}
		8'd{{input_id}}: get_io_target = 8'd{{input_target}};{% endfor %}
		default: get_io_target = 8'h00;
	endcase
endfunction
{% endblock %}
