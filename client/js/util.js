//some util functions

//convert date to GMT+0200
function timeZoned(timestamp){
	return new Date(timestamp).toLocaleString('it-IT', {timeZone: 'Europe/Rome'});
}

function dateMake(datestr){
	arr = datestr.split(', ');
	dmy = arr[0].split('/');
	hms = arr[1].split(':')
	return new Date(dmy[2], dmy[1], dmy[0], hms[0], hms[1], hms[2]);
}

//show a new message
function newMessage(type=null, message='', class_div = ".message"){
	$(class_div).removeClass("text-danger text-success text-warning");
	if(type) $(class_div).addClass("text-"+type);
	$(class_div).html("<h3>" + message + "</h3>");
}