//draw button event
function requestDraw(){
	graph = $("#graph").val();
	hours = $("#hours").val();
	if(graph && hours)
		socket.send(`{ "action": "history",
					   "graph" : "${graph}", 
					   "hours" : ${hours} }`);
}

//change button event
function requestRateChange(){
	new_rate = $("#new_rate").val();
	if(new_rate)
		socket.send(`{ "action": "rate",
						"rate" : "${new_rate}"}`);
}


//connect button event
//attempts to connect to web socket with provided token 
function attemptConnect(event){
	event.preventDefault();
	token = $("input[name='token']").val();
	$(this).trigger("reset");

	try{
		newMessage();
		socket = new WebSocket('wss://tx3bpj2xt4.execute-api.eu-central-1.amazonaws.com/dev?authorizationToken=' + token);
		setOnOpen();
		setOnClose();
		setOnError();
		setOnMessage();
	}
	catch(error){
		newMessage("danger", error);
	}

}