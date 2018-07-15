import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import * as d3 from 'd3';

@Component({
  selector: 'app-flags-by-datastream',
  templateUrl: './flags-by-datastream.component.html',
  styleUrls: ['./flags-by-datastream.component.css']
})
export class FlagsByDatastreamComponent implements OnInit {

  id = -1;
  sub = null;
  flagData = {};
  flagDataArr = [];
  labels = [];
  viewport_width = 1600;
  viewport_height = 600;

  constructor(private aroute:ActivatedRoute, private http:HttpClient, private router:Router) {

  }

  ngOnInit() {


      this.sub = this.aroute.params.subscribe(params => this.id = params["id"]);
      this.http.get('http://sensor.nevada.edu/GS/Services/Flag/L1/'+this.id).subscribe(
        data => {
          this.flagData = data;
          this.flagDataArr = this.formatFlagObjects(data);
          this.labels = this.extractLabels(this.flagDataArr);


          var svgContainer = d3.select("#flag-bundles-container").append("svg")
                              .attr("width", this.viewport_width)
                              .attr("height", this.viewport_height);



          var circles = svgContainer.selectAll("circle")
                              .data(this.flagDataArr)
                              .enter()
                              .append("circle");

          var circleAttributes = circles
                                 .attr("cx", function(d){return d.xoffset;})
                                 .attr("cy", function(d){return d.yoffset;})
                                 .attr("r", function(d){return d.radius})
                                 .style("fill", function(d){return d.color;})
                                 .style("cursor", "pointer")
                                 .on("click", function(d){ d.classContext.forwardToMeasurements(d, d.classContext) })
                                 //.on("mouseover", function(d){console.log("mouseover", this); d3.select(this).style("fill", "rgb(250,170,104, .9)");  })
                                 //.on("mouseout", function(){d3.select(this).style("fill", "#027878") })



          //set the center text of each sphere object
          svgContainer
                  .selectAll("text.flagData")
                  .data(this.flagDataArr)
                  .enter()
                  .append("text")
                  .style("fill", "rgba(255,255,255,0.9)")
                  .style("text-anchor", "middle")
                  .style("cursor", "pointer")
                  .attr("x", function(d){return d.xoffset;} )
                  .attr("y", function(d){return d.yoffset + 20;} )
                  .attr("font-size", "4em")
                  .text( function(d){return d.flagCount;} )
                  .on("click", function(d){ d.classContext.forwardToMeasurements(d, d.classContext) })
                  .on("mouseover", function(d){console.log("mouseover", this); d3.select(this).style("fill", "rgba(0,0,0,.7)");  })
                  .on("mouseout", function(){d3.select(this).style("fill", "rgba(255,255,255,.9)") })


          svgContainer
                  .selectAll("text.labels")
                  .data(this.flagDataArr)
                  .enter()
                  .append("text")
                  .style("fill", "rgba(0,0,0,0.9)")
                  .style("text-anchor", "middle")
                  .attr("x", function(d){return d.xoffset;} )
                  .attr("y", function(d){return d.yoffset-120;} )
                  .attr("font-size", "1.1em")
                  .text( function(d){ return d["Deployment Name"]; } );

          svgContainer
                  .selectAll("text.streams")
                  .data(this.flagDataArr)
                  .enter()
                  .append("text")
                  .style("fill", "rgba(0,0,0,0.9)")
                  .style("text-anchor", "middle")
                  .attr("x", function(d){return d.xoffset;} )
                  .attr("y", function(d){return d.yoffset-150;} )
                  .attr("font-size", "1.5em")
                  .text( function(d){ return "Stream: " + d["streamID"] ; } );

          console.log(this.flagDataArr);


        })



  }

  ngOnDestroy() {
      this.sub.unsubscribe();
  }

  formatFlagObjects(returnedFlags:object):object[]{
      var objectsArr = [];

      for(let dsid in returnedFlags){
          if(!Number.isNaN(+dsid)){
              returnedFlags[dsid]["streamID"] = dsid;
              returnedFlags[dsid]["flagCount"] = returnedFlags[dsid]["Measurements"].length;

              //this binds the class context to this object
              //necessary for evoking class level functions
              returnedFlags[dsid]["classContext"] = this;

              objectsArr.push(returnedFlags[dsid]);
          }
      }

      //sort each stream by size in descending order
      objectsArr = objectsArr.sort( (fo1,fo2)  => {
          if(fo1["flagCount"] < fo2["flagCount"]){
            return 1;
          }
          if(fo1["flagCount"] > fo2["flagCount"]){
            return -1
          }
          return 0;
      });

      objectsArr = this.assignVisualData(objectsArr);

      return objectsArr;
  }

  //assign some visual data to each flag bundle object that will be
  // displayed as a circle
  assignVisualData(flagBundles:object[]):object[]{
      var xoffset = 400, yoffset = 200;
      var color = "rgb(250,170,104, .9)";
      var radius = 100;
      var localXOffset = 400;
      var localYOffset = 320;

      for(var i=0; i< flagBundles.length; i++ ){
          if(localXOffset*(i+1) < this.viewport_width - 100){
            flagBundles[i]["xoffset"] = localXOffset*(i+1);
            flagBundles[i]["yoffset"] = yoffset;
          } else {
            localXOffset = 400;
            localYOffset += yoffset;
            this.viewport_height += yoffset;

            flagBundles[i]["xoffset"] = localXOffset;
            flagBundles[i]["yoffset"] = localYOffset;
          }
          flagBundles[i]["color"] = color;
          flagBundles[i]["radius"] = radius;
      }


      return flagBundles;
  }

  forwardToMeasurements(passedFlaggedData:object, context){
      var flagDataBundle = {};

      //flagDataBundle["Measurements"] = passedFlaggedData["Measurements"];
      flagDataBundle["streamID"] = passedFlaggedData["streamID"];
      flagDataBundle["Deployment Name"] = passedFlaggedData["Deployment Name"];
      flagDataBundle["Deployment ID"] = passedFlaggedData["Deployment ID"];

      context.router.navigate(["/datavis/", flagDataBundle] );
  }

  extractLabels(organizedData:object[]):object[]{
      var labels = [];

      for(var i=0; i < organizedData.length; i++){
          labels.push(organizedData[i]["Deployment Name"] + " : Stream " + organizedData[i]["streamID"]);
      }

      return labels;
  }



}
