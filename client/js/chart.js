//build dataPoints array for the requested graphic
function updateGraph(responseJSON){
	
	chart.destroy();
	dataPoints = [];
	graph = responseJSON['graph'];
	hours = responseJSON['hours'];

	dataPoints.push({
		x : timeZoned(Date.now() - parseInt(hours) * 60 * 60 * 1000),
		y : null
	});

	for(key in responseJSON['data']){
			
			varx = timeZoned(parseInt(responseJSON['data'][key]['timestamp'][vartype['timestamp']]) * 1000);
			tmp = responseJSON['data'][key][graph][vartype[graph]];
			vary = tmp != "Fail to read"? parseFloat(tmp) : null;
			dataPoints.push({
				x : varx,
				y : vary
			});
	}

	if(vartype[graph] == 'N')
		draw(`${alias[graph]} in the last ${hours} hours`, dataPoints, graph, "0");
	else
		draw(`${alias[graph]} in the last ${hours} hours`, dataPoints, graph);
}

//draw the requested graphic
function draw(title_text = "Empty graph", dataPoints = [], graph = null, yformat = "0.0#"){
	
	dataPoints.push({
		x : timeZoned(Date.now()),
		y : null
	});

	window.chart = new CanvasJS.Chart("chartContainer",
	{		
	
			theme : "dark2",
			title: {
				text: title_text,
				margin: 10,
				padding: 10     
			},

			axisX:{      
				valueFormatString: "H:mm",
				labelAngle: -50,
				title: "time",
				time: {
					unit: 'minute',
				},
				margin: 5,
				labelFontColor: "#adb5bd",
				lineColor: "#1a1a1a",
				tickColor: "#1a1a1a",
				interlacedColor: "#3c434a",
			},

			axisY: {
				valueFormatString: yformat,
				title: units[graph],
				margin: 5,
				labelFontColor: "#adb5bd",
				lineColor: "#1a1a1a",
				tickColor: "#1a1a1a",
				gridColor: "#1a1a1a"
			},
			
			data : [{
				type : "spline",
				xValueType: "dateTime",
				color: "#ec1525",
				markerColor : "#fff",
				markerBorderColor : "#171a1c",
				markerBorderThickness : 2,
				dataPoints : dataPoints
			}]
		}
	
	);

	chart.render();
}