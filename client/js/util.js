//some util functions

//convert date from GMT-0400 to GMT+0200
function timeZoned(timestamp){
	return new Date(new Date(timestamp + 6 * 60 * 60 * 1000).toString());
}

//show a new message
function newMessage(type=null, message='', class_div = ".message"){
	$(class_div).removeClass("text-danger text-success text-warning");
	if(type) $(class_div).addClass("text-"+type);
	$(class_div).html("<h3>" + message + "</h3>");
}