import { Component, OnInit, Input, OnChanges } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'line-graph',
  templateUrl: './line-graph.component.html',
  styleUrls: ['./line-graph.component.css']
})
export class LineGraphComponent implements OnInit, OnChanges {

  @Input() chartData:object[];

  constructor() { }

  ngOnInit() {
      //build our grpah the first time
      //var el: HTMLElement = document.getElementById("graph-container");
      //this.buildGraph(el);
      //scope.$watch('chartData.data', updateChart);
  }

  ngOnChanges(changes) {
    console.log(changes);
    if(this.chartData.length > 2){
      var el: HTMLElement = document.getElementById("graph-container");
      this.buildGraph(el, this.chartData);
    }
  }




        //look for any changes to data or element & adjust accordingly

        //angular.element($window).on('resize', updateChart);



        /**
          * Principle function to call on change of data that comprises chart.
          * Called from scope.$watch(<data>)
          *
          *
          */
        // private updateChart() {
        //
        //     //variables shared by buld graph and update graph
        //     var containerWidth = elem.parent()[0].offsetWidth;
        //     var containerHeight = elem.parent()[0].offsetHeight;
        //
        //     var margin = { top: 20, right: 20, bottom: 30, left: 30 },
        //     width = containerWidth - margin.left - margin.right,
        //     height = containerHeight - margin.top - margin.bottom;
        //
        //     d3.selectAll('svg')
        //         .attr("width", width + margin.left + margin.right)
        //         .attr("height", height + margin.top + margin.bottom)
        //         .append("g")
        //         .attr("transform",
        //         "translate(" + margin.left + "," + margin.top + ")");
        //
        //     //parse our time values
        //     var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S");
        //
        //     //for each is a javascript function
        //     //does something to each item in calling array
        //     //this is being used to format the data
        //     scope.chartData.data.forEach(function (d) {
        //         d.ParsedTimeStamp = parseTime(d["Time Stamp"]);
        //         d["Value"] = +d["Value"];
        //     });
        //
        //     //set ranges for our graph
        //     // we will use this with the line definition
        //     var x = d3.scaleTime().range([0, width]);
        //     var y = d3.scaleLinear().range([height, 0]);
        //     var xAxis = d3.axisBottom(x).ticks(10);
        //     var yAxis = d3.axisLeft(y);
        //
        //     var valueline = d3.line()
        //     .curve(d3.curveMonotoneX)
        //     .x(function (d) { return x(d.ParsedTimeStamp); })
        //     .y(function (d) { return y(d["Value"]); });
        //
        //     // Scale the range of the data again
        //     x.domain(d3.extent(scope.chartData.data, function (d) { return d.ParsedTimeStamp; }));
        //     y.domain([d3.min(scope.chartData.data, function (d) { return d["Value"]; }) - 5, d3.max(scope.chartData.data, function (d) { return d["Value"]; })]);
        //
        //     // Select the section we want to apply our changes to
        //     var svg = d3.select(elem.parent()[0]).transition();
        //
        //     // Make the changes
        //     svg.select(".line")   // change the line
        //         .duration(750)
        //         .attr("d", valueline(scope.chartData.data));
        //     svg.select(".x.axis") // change the x axis
        //         .duration(750)
        //         .call(xAxis);
        //     svg.select(".y.axis") // change the y axis
        //         .duration(750)
        //         .call(yAxis);
        // }


        /**
          * Local Function used to build our graph the first time using bound data.
          * This will have to be expanded I think to be inclusive of more data sets at one time.
          * Also requires the ability to plot two data scales.
          */

        public buildGraph(elem:HTMLElement, chartData:object[]) {
            var containerWidth = elem.offsetWidth;
            var containerHeight = elem.offsetHeight;

            var margin = { top: 20, right: 20, bottom: 30, left: 30 },
            width = containerWidth - margin.left - margin.right,
            height = containerHeight - margin.top - margin.bottom;

            var svg = d3.select(elem).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

            //parse our time values
            var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S");


            //set ranges for our graph
            // we will use this with the line definition
            var x = d3.scaleTime().range([0, width]);
            var y = d3.scaleLinear().range([height, 0]);


            var valueLine = d3.line()
                    .curve(d3.curveMonotoneX)
                    .x(d => { return x(d["Time Stamp"]); })
                    .y(d => { return y(d["Value"]); });


            var data = chartData;

            //for each is a javascript function
            //does something to each item in calling array
            //this is being used to format the data
            data.forEach(function (d) {
                d["Time Stamp"] = new Date(d["Time Stamp"]);
                if(d["Value"] != "None"){
                    d["Value"] = +d["Value"];
                }else{
                    d["Value"] = 0;
                }
            });

            console.log(data);


            //this holds the actual ramges of our dataset
            //domain expects a two value array [min,max] (extent returns that array)
            x.domain(d3.extent(data, function (d) { return d["Time Stamp"]; }));
            y.domain([d3.min(data, function (d) { return d["Value"]; }), d3.max(data, function (d) { return d["Value"]; })]);

            // Add the valueline path
            // attr "d" automgically calls valueline to
            // setup our line using x,y values in data
            //d3.select("path").remove();


            svg.append("path")
               .data([data])
               .attr("class", "line")
               .attr("d", valueLine)
               .on("mouseover", function(d){
                        console.log( x.invert( d3.mouse(elem)[0]), y.invert(d3.mouse(elem)[0]) )
                   });

            // Add the X Axis
            svg.append("g")
               .attr("transform", "translate(0," + height + ")")
                .attr("class", "x axis")
               .call(d3.axisBottom(x).ticks(10));

            // Add the Y Axis
            svg.append("g")
                .attr("class", "y axis")
                .call(d3.axisLeft(y));
        }


}
