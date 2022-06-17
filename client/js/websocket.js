//ping to api default endpoint after a while
function ping(){
	socket.send(`{"action" : "default"}`);
}

//set websocket open connection event
function setOnOpen(){
	
	socket.addEventListener('open', function (event) {
		$("#connected").show();
		$("#toconnect").hide();
		$("#draw").click(requestDraw);
		$("#change").click(requestRateChange);
		draw();
		newMessage("success", "Connected");
		timer_event = setInterval( loopTime, 1000);
		ping_event = setInterval(ping, 2 * 60 * 1000);
		socket.send(`{"action" : "now"}`);
	});

}

//set websocket close connection event
function setOnClose(){
	socket.addEventListener('close', function (event) {
		$("#connected").hide();
		$("#toconnect").show();
		newMessage("danger", "Disconnected");
		clearInterval(timer_event);
		clearInterval(ping_event);
	});
}

//set websocket error event
function setOnError(){
	socket.addEventListener('error', function (event) {
		$("#connected").hide();
		$("#toconnect").show();
		newMessage("danger", event.data);
	});
}

//set websocket message event
function setOnMessage(){
	
	socket.addEventListener('message', function (event) {
		responseJSON = JSON.parse(event.data);

		if('action' in responseJSON){
			action = responseJSON['action'];
			delete responseJSON['action'];
		}
		else action = null;

		if('message' in responseJSON){
			mex = responseJSON['message'];
			style = mex.toLowerCase().includes("error") ? "danger" : ( mex.toLowerCase().includes("waiting") ? "warning" : "success" );
			newMessage( style , mex, '.log');
			setTimeout(function(){
				$(".log").empty();
			}, 3000);
		}


		switch(action){
			case 'now':
				updateDashboard(responseJSON);
			break;
			case 'history':
				updateGraph(responseJSON);
			break;
			case 'ack':
				$("#rate").html("<h3>" + responseJSON['rate'] + " mins</h3>");
		}
		
	});
}