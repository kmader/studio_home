var initSpeed = function(element,points,max,suffix){
	var points = points;
	var parent = $(element).closest('.card-body');
	var totalgraphwidth = parent.width()-24;
	var currentgraphwidth = $(element).width();
	if( currentgraphwidth >= totalgraphwidth){
		points.shift();
	}
	var options = $(element).data();
	options.type = 'bar';
	options.barWidth = 6;
	options.barSpacing = 2;
	options.chartRangeMin = 0;
	options.chartRangeMax = max;
	options.width = currentgraphwidth + 'px';
	options.height = $(element).height() + 'px';
	options.fillColor = false;
	$(element).sparkline(points, options);
	$(element + "-text").text(parseFloat(points[points.length-1]).toFixed(2) + suffix);
};

var initCpuGpuSpeed = function(element,hw_name,points,max,suffix){
	var points = points;
	var parent = $(element).closest('.card-body');
	var totalgraphwidth = parent.width()-24;
	var currentgraphwidth = $(element).width();
	if( currentgraphwidth >= totalgraphwidth){
		points.shift();
	}
	var options = $(element).data();
	options.type = 'bar';
	options.barWidth = 6;
	options.barSpacing = 2;
	options.chartRangeMin = 0;
	options.chartRangeMax = max;
	options.height = $(element).height() + 'px';
	options.fillColor = false;
	$(element).sparkline(points, options);
	$(element + "-text").text(parseFloat(points[points.length-1]).toFixed(2).toString() + suffix);
	$(element + "-hw-name").text(hw_name);
};