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
  public lineChartOptions:any = {responsive: true};
  public lineChartLegend:boolean = true;
  public lineChartType:string = 'line';
  public loadingDone:boolean = false;
  public reviewFlags:boolean = false;
  public flagMappings = {1:"Repeat Value",2:"Out of Bounds",3:"Missing Value", 4:"OK"};

  updateChart(){
      this.data = this.data.slice()
  }

  //function
  public renderFlags = function(event, active){
                          if(active[0] != null){
                              //console.log(event,active,this.flags[active[0]._index]);
                              //active[0]._view.backgroundColor = "rgba(0,0,0,1)";
                              //this.updateChart();
                          }
                      };


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

             for(let measurement in data["Measurements"]){
                this.data.push(data["Measurements"][measurement]['Value']);
                this.labels.push(data["Measurements"][measurement]['Time Stamp']);
                this.flags.push(this.flagMappings[data["Measurements"][measurement]['Flag Type']]);

                this.dataHolder.push(data["Measurements"][measurement]);
             }


             this.lineChartOptions['hover'] = { onHover: (event, active) => { this.renderFlags(event, active) } };

             this.loadingDone = true;

      })
  }

  showAdvData($event, active){
    console.log($event, active);
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  listFlags(){
    this.reviewFlags = true;
  }

  returnToChart(){
    this.reviewFlags = false;
  }

}
