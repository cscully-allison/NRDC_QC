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
  private passedData = {};
  private dataHolder = [];

  constructor(private route:ActivatedRoute, private http:HttpClient) { }

  ngOnInit() {
    //required safegards for
    if(true){
      this.sub = this.route.params.subscribe( passedData => {
        this.passedData = passedData;
      });
    }

    this.http.get('https://sensor.nevada.edu/GS/Services/DataVis/Measurements/' + this.passedData["streamID"] + '/1000').subscribe(
       data => {
           console.log(data)
           for(let measurement in data["Measurements"]){
              var measurementRef =  data["Measurements"][measurement];
           }
    })
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
