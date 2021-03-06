import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-datavis-dashboard',
  templateUrl: './datavis-dashboard.component.html',
  styleUrls: ['./datavis-dashboard.component.css']
})

export class DatavisDashboardComponent implements OnInit {

  private sub = null;
  public test = "test";
  public passedData = {};
  public dataHolder = [];

  constructor(private route:ActivatedRoute, private http:HttpClient) { }

  ngOnInit() {
    //required safegards for
    if(true){
      this.sub = this.route.params.subscribe( passedData => {
        this.passedData = passedData;
      });
    }

    this.http.get('https://sensor.nevada.edu/GS/Services/DataVis/Measurements/' + this.passedData["streamID"] + '/50').subscribe(
       data => {
           var tempHolder = [];
           var flagNames = ["Repeat Value","Out of Bounds","Missing Value","OK"];

           for(let measurement in data["Measurements"]){
              var measurementRef =  data["Measurements"][measurement];
              measurementRef["Flag Name"] = flagNames[measurementRef["Flag Type"]-1];
              tempHolder.push(measurementRef);
           }

           this.dataHolder = tempHolder;

    })
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
