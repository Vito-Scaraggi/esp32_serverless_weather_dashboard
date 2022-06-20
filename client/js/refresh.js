function updateDashboard(responseJSON){
	for (property in responseJSON){
		if(property == "timestamp"){
			timestamp = parseInt(responseJSON[property][vartype[property]]) * 1000;
			content = timeZoned(timestamp);
		}
		else{
			data = responseJSON[property][vartype[property]];
			
			if(data == "Fail to read")
				content = data
			else 
				content = (property == "temp"? parseFloat(data).toFixed(2) : data) + " " + units[property];
		}
		$("#"+property).html("<h3>" + content + "</h3>");
	}
}

function loopTime(){
	
	$.ajax(
		{
			url : "https://worldtimeapi.org/api/ip",
			type : "GET",
			dataType: "json",
			success : function(result){
				let data = new Date(result.datetime);
				//console.log(result.timezone);
				$("#time").html(data.toLocaleString('it-IT',{timeZone: result.timezone}));
			},
			error : function(xhr){
				console.log("Fatal error: " + xhr.status + " " + xhr.statusText);
			}
		}
	);
}
