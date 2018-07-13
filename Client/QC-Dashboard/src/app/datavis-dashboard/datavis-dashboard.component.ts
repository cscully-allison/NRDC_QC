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
  public data:Array<any> = [];
  public labels:Array<number[]> = [];
  public flags:Array<any> = [];
  public lineChartOptions:any = {
    responsive: true,
  };
  public lineChartLegend:boolean = true;
  public lineChartType:string = 'line';
  public loadingDone:boolean = false;

  //function
  public renderFlags = function(event, active){ if(active[0] != null){ console.log(event,active,this.flags[active[0]._index]) } };


  constructor(private route:ActivatedRoute, private http:HttpClient) { }

  ngOnInit() {
      //required safegards for
      if(true){
        this.sub = this.route.params.subscribe( passedData => {
          this.passedData = passedData;
        });
      }

      this.http.get('https://sensor.nevada.edu/GS/Services/DataVis/Measurements/' + this.passedData["streamID"] + '/150').subscribe(
         data => {
             var tempHolder = [];
             var flagMappings = {1:"Repeat Value",2:"Out of Bounds",3:"Missing Value", 4:"OK"};

             for(let measurement in data["Measurements"]){
                this.data.push(data["Measurements"][measurement]['Value']);
                this.labels.push(data["Measurements"][measurement]['Time Stamp']);
                this.flags.push(flagMappings[data["Measurements"][measurement]['Flag Type']]);

                // var measurementRef =  data["Measurements"][measurement];
                // measurementRef["Flag Name"] = flagNames[measurementRef["Flag Type"]-1];
                // tempHolder.push(measurementRef);

             }


             this.lineChartOptions['hover'] = {onHover: (event, active) => { this.renderFlags(event, active) }};

             this.loadingDone = true;

             // this.dataHolder = tempHolder;

      })
  }

  showAdvData($event, active){
    console.log($event, active);
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

}
