function pie(element, title, subtitle, content) {
 return new d3pie(element, {
    "header": {
      "title": {
        "text": title,
        "fontSize": 23,
        "font": "verdana"
      },
      "subtitle": {
        "text": subtitle,
        "color": "#999999",
        "fontSize": 12,
        "font": "verdana"
      },
      "titleSubtitlePadding": 12
    },
    "footer": {
      "color": "#999999",
      "fontSize": 11,
      "font": "open sans",
      "location": "bottom-center"
    },
    "size": {
      "canvasHeight": 350,
      "canvasWidth": 400,
      "pieOuterRadius": "88%"
    },
    "data": {
      "sortOrder": "value-desc",
      "smallSegmentGrouping": {
          "enabled": true,
          "value": 4,
          "label": "Outros"
      },
      "content": content
    },
    "labels": {
      "outer": {
        "format": "label-percentage2",
        "pieDistance": 32
      },
      "inner": {
        "format": "value"
      },
      "mainLabel": {
        "font": "verdana",
        "fontSize": 14
      },
      "percentage": {
        "color": "#bc6666",
        "font": "verdana",
        "fontSize": 12,
        "decimalPlaces": 0
      },
      "value": {
        "color": "#fcfcfc",
        "font": "verdana",
        "fontSize": 12,
      },
      "lines": {
        "enabled": true,
        "color": "#cccccc"
      },
      "truncation": {
        "enabled": true
      }
    },
    "effects": {
      "load": {
        "speed": 500
      },
      "pullOutSegmentOnClick": {
        "effect": "linear",
        "speed": 400,
        "size": 8
      }
    }
  });
}

function simpleBarChart(element, data, title, titleX, titleY, width2, height2) {
// nv.addGraph(function() {
//   var chart = nv.models.discreteBarChart()
//       .x(function(d) { return d.label })    //Specify the data accessors.
//       .y(function(d) { return d.value })
//       .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
//       .tooltips(false)        //Don't show tooltips
//       .showValues(true)       //...instead, show the bar value right on top of each bar.
//       .transitionDuration(350)
//       ;

//   d3.select('#chart svg')
//       .datum(data) //.datum(exampleData())
//       .call(chart);

//   nv.utils.windowResize(chart.update);

//   return chart;
// });

  var margin = {top: 20, right: 20, bottom: 100, left: 100}; //margin = {top: 20, right: 20, bottom: 30, left: 40};
  // if (title.length>0) {
  //   margin.top = margin.top+30
  // }
  var width = width2 - margin.left - margin.right,
      height = height2 - margin.top - margin.bottom;

  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], 0.1);

  var y = d3.scale.linear()
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      ;

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      //.ticks(10, "%")
      ;

  var svg = d3.select(element).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  // if (title.length>0) {
  //   svg
  //     .append("text")
  //       .attr("y", width/2)
  //       .attr("dy", ".71em")
  //       .style("text-anchor", "middle")
  //       .text(title);
  // }
  // svg
  //     .append("g")
  //       .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  data.forEach(function(d) {
    d.value = +d.value;
  });

  x.domain(data.map(function(d) { return d.x; }));
  var ymin = d3.min(data, function(d) { return d.value; });
  var ymax = d3.max(data, function(d) { return d.value; });
  if ((ymin>=0) && (ymax>=0)) {
    ymin = 0;
  }
  y.domain([ymin, ymax]);//y.domain([0, d3.max(data, function(d) { return d.value; })]);

  svg
    .append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" )
      //.text(titleX)
      ;

  svg
    .append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 4)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text(titleY)
      ;

  svg
    .selectAll(".bar")
      .data(data)
    .enter().append("rect")
      //.style("fill", "steelblue")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.x); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.value); })
      .attr("height", function(d) { return height - y(d.value); });

  return svg;
}


/* Inspired by Lee Byron's test data generator. */
function stream_layers(n, m, o) {
  if (arguments.length < 3) o = 0;
  function bump(a) {
    var x = 1 / (0.1 + Math.random()),
        y = 2 * Math.random() - 0.5,
        z = 10 / (0.1 + Math.random());
    for (var i = 0; i < m; i++) {
      var w = (i / m - y) * z;
      a[i] += x * Math.exp(-w * w);
    }
  }
  return d3.range(n).map(function() {
      var a = [], i;
      for (i = 0; i < m; i++) a[i] = o + o * Math.random();
      for (i = 0; i < 5; i++) bump(a);
      return a.map(stream_index);
    });
}

/* Another layer generator using gamma distributions. */
function stream_waves(n, m) {
  return d3.range(n).map(function(i) {
    return d3.range(m).map(function(j) {
        var x = 20 * j / m - i / 3;
        return 2 * x * Math.exp(-0.5 * x);
      }).map(stream_index);
    });
}

function stream_index(d, i) {
  return {x: i, y: Math.max(0, d)};
}

// Set locale
var pt_BR = {
              "decimal": ",",
              "thousands": ".",
              "grouping": [3],
              "currency": ["R$ ", ""],
              "dateTime": "%d/%m/%Y H:%M:%S",
              "date": "%d/%m/%Y",
              "time": "%H:%M",
              "periods": ["", ""],
              "days": ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
              "shortDays": ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
              "months": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
              "shortMonths": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
            };
var locale = d3.locale(pt_BR);

function complexBarChart(element, data, title, titleX, titleY, width2, height2) {
  if (1 == 1) {
    nv.addGraph(function () {

      var margin = {top: 20, right: 20, bottom: 100, left: 100}; //margin = {top: 20, right: 20, bottom: 30, left: 40};

      var chart = nv.models.multiBarChart()
        //.transitionDuration(350)  // deprecated => .duration()
        .duration(350)
        .reduceXTicks(true)   //If 'false', every single x-axis tick label will be rendered.
        .rotateLabels(-90)      //Angle to rotate x-axis labels.
        .showControls(true)   //Allow user to switch between 'Grouped' and 'Stacked' mode.
        .groupSpacing(0.1)    //Distance between each group of bars.
      ;

      //chart.legend.margin({top: 5, right: 100, bottom: 50, left: 100});
      //chart.legend.margin().bottom = 50;
      //chart.margin( {top: 30, right: 20, bottom: 50, left: 60} );
      chart.margin().left = 110;


      chart.xAxis
      //.tickFormat(d3.format(',f'))
      //.tickPadding(25)
      ;

      chart.yAxis
        //.tickPadding(25)
        .tickFormat(locale.numberFormat('$,.2f')); //.tickFormat(d3.format(',.2f')); locale.numberFormat(

      //console.log(console, data);

      d3.select(element)
        .datum(data)
        //.datum(exampleData())
        .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
  }

    //Generate some nice data.
  //   function exampleData() {
  //     return stream_layers(3,10+Math.random()*100,0.1).map(function(data, i) {
  //       return {
  //         key: 'Stream #' + i,
  //         values: data
  //       };
  //     });
  //   }
  // }

  if (1 === 0) {
    nv.addGraph(function() {
      var chart = nv.models.discreteBarChart()
          .x(function(d) { return d.label })    //Specify the data accessors.
          .y(function(d) { return d.value })
          .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
          //.tooltips(false)        //Don't show tooltips
          .showValues(true)       //...instead, show the bar value right on top of each bar.
          //.transitionDuration(350)
          .duration(350)
          ;

      d3.select(element)
          .datum(data) //.datum(exampleData())
          .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
  }
}

