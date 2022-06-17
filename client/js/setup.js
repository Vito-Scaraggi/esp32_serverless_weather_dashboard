/// onload instructions

$(document).ready( function(){
	window.socket = null;
	window.timer_event = null;
	
	window.units = {
		"temp" : "°C",
		"humid" : "%",
		"lum" : "",
		"rate" : "mins"
	}

	window.vartype = {
		"temp" : "S",
		"humid" : "S",
		"lum" : "N",
		"rate" : "N",
		"timestamp" : "N"
	}

	window.alias = {
		"temp" : "Temperature",
		"humid" : "Humidity",
		"lum" : "Brightness",
		"rate" : "Measurement rate",
		"timestamp" : "Time"
	}
	window.timer_event = null;
	window.ping_event = null;

	$("#connected").hide();
	$("#toconnect").show();
	$("#attemptconnect").on("submit", attemptConnect);
});