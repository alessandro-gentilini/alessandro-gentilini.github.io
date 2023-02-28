// Simple model of water waves using circular motion of the particles.
// Hastily written by Mark McClure
// September 23/24, 2019.
//
// Based on work by Dan Russell:
// https://www.acs.psu.edu/drussell/Demos/waves/wavemotion.html


svg = d3.select('body').append('svg');
function setup_pic() {
	width = window.innerWidth;
	height = window.innerHeight;
	svg
		.selectAll('*').remove()
	svg
		.attr('width', width)
		.attr('height', height)

	xmin = -10, xmax = 10, dx = 1;
	ymin = -6, ymax = 8, dy = 1;
	xScale = d3.scaleLinear()
	  .domain([xmin, xmax])
	  .range([0, width]);
	rScale = d3.scaleLinear()
	  .domain([0,xmax-xmin])
	  .range([0, width]);
	yScale = d3.scaleLinear()
	  .domain([ymin,ymax])
	  .range([height, 0]);
	pts_to_path = d3.line()
	  .x(function(d) { return xScale(d[0]); })
	  .y(function(d) { return yScale(d[1]); })

	grid = d3.range(ymin,dy,dy)
		.map(y => (d3.range(xmin-dx,xmax + 2*dx,dx).map(x => [x,y])));
	grid = grid.reduce(
	  function(accumulated, currentValue) {
	    return accumulated.concat(currentValue);
	  },
	  []
	);

	A0 = 0.7, alpha0 = 0.6, beta = 3, t0 = 0;
	A = A0, alpha = alpha0;
	pts = grid.map(xy => p(A,alpha,beta,xy[0],xy[1],t0));
	outline = pts.slice((pts.length - (xmax-xmin+3)));
	outline.push([xmax,ymin]);
	outline.push([xmin,ymin]);

	svg
		.append("path")
    .attr('d', pts_to_path(outline))
		.attr('fill', 'lightblue')
		.attr('stroke', 'blue')
		.attr('stroke-width', '2px');
  circles = svg
    .selectAll("circle")
    .data(pts)
    .enter().append("circle")
    .attr('class', 'water')
    .attr("cx", function(d) { return xScale(d[0])})
    .attr("cy", function(d) {return yScale(d[1])})
    .attr("r", 3)
    .attr("fill", "black")
    .attr("stroke", "black")
    .attr("stroke-width", 1);
	to_highlight = circles
		.filter(function(d,i) {
			i1 = (Math.round(pts.length - (xmax-xmin+3)/2));
			i2 = (3*Math.round(pts.length/4 - (xmax-xmin+3)/2));
			return i == i1 || i == i2
		})
		.attr('class', 'highlight')
}
setup_pic()

function start(t) {
	pts = grid.map(xy => p(A,alpha,beta,xy[0],xy[1],t/1000));
	outline = pts.slice(grid.length - (xmax-xmin+3));
	outline.push([xmax,ymin]);
	outline.push([xmin,ymin]);
	svg
		.selectAll("path")
    .transition().duration(0)
    .attr('d', pts_to_path(outline));
  svg
    .selectAll("circle")
    .data(pts)
    .transition().duration(0)
    .attr("cx", function(d) { return xScale(d[0])})
    .attr("cy", function(d) {return yScale(d[1])})
}
timer = d3.timer(start);

x_to_alpha = d3.scaleLinear()
	.domain([0,width])
	.range([0.1,1]);
y_to_A = d3.scaleLinear()
	.domain([height,0])
	.range([0.1, 1]);

function update(xy) {
	x = xy[0];
	alpha_in = x_to_alpha(x);
	y = xy[1];
	A_in = y_to_A(y);
	rate = 0.9;
	one_minus_rate = 1-rate;
	alpha = rate*alpha + one_minus_rate*alpha_in;
	A = rate*A + one_minus_rate*A_in;
}

highlighted = 'off'
d3.select('body')
	.on("mousemove", function() {
		update(d3.mouse(this))
	})
	.on("mouseleave", function() {
		trans_timer = d3.timer(trans_back);
	})
	.on("mouseenter", function() {
		if(window.trans_timer && trans_timer.stop) {
			trans_timer.stop()
		}
	})
	.on('touchmove', function() {
		update(d3.touches(this)[0])
	})
	.on("touchend", function() {
		trans_timer = d3.timer(trans_back);
	})
	.on("touchstart", function() {
		if(window.trans_timer && trans_timer.stop) {
			trans_timer.stop()
		}
		if(highlighted == 'off') {
			d3.selectAll('circle.highlight')
				.attr('r',5)
				.attr('fill', 'yellow');
			highlighted = 'on'
		}
		else {
			d3.selectAll('circle.highlight')
				.attr('r',3)
				.attr('fill', 'black');
			highlighted = 'off'
		}
	})
	.on('click', function() {
		if(highlighted == 'off') {
			d3.selectAll('circle.highlight')
				.attr('r',8)
				.attr('fill', 'yellow');
			highlighted = 'on'
		}
		else {
			d3.selectAll('circle.highlight')
				.attr('r',3)
				.attr('fill', 'black');
			highlighted = 'off'
		}
	})

function trans_back() {
	rate = 0.9;
	one_minus_rate = 1-rate;
	alpha = rate*alpha + one_minus_rate*alpha0;
	A = rate*A + one_minus_rate*A0;
	if(Math.abs(alpha) + Math.abs(A-1)<0.01) {
		trans_timer.stop()
		return false
	}
	else {
		return true
	}
}

function p(A,alpha,beta,x0,y0,t) {
	r = A*Math.exp(alpha*y0);
	arg = alpha*x0-beta*t;
	x = x0 + r*Math.cos(arg);
	y = y0 + r*Math.sin(arg);
	return [x,y]
}

window.addEventListener("resize", setup_pic);
