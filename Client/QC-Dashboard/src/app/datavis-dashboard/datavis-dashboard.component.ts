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

  public lineChartData:Array<any> = [
   {data: [], label: 'Series A'}
  ];

  public lineChartLabels:Array<any> = [];

  public lineChartOptions:any = {
   responsive: true,
   scales: {
           xAxes: [{
               type:"time",
               time: {
                  unit: 'month'
              }
          }]
       }
  };

  public lineChartColors:Array<any> = [
   { // grey
     backgroundColor: 'rgba(148,159,177,0.2)',
     borderColor: 'rgba(148,159,177,1)',
     pointBackgroundColor: 'rgba(148,159,177,1)',
     pointBorderColor: '#fff',
     pointHoverBackgroundColor: '#fff',
     pointHoverBorderColor: 'rgba(148,159,177,0.8)'
   },
   { // grey
     backgroundColor: 'rgba(148,159,177,0.2)',
     borderColor: 'rgba(148,159,177,1)',
     pointBackgroundColor: 'rgba(148,159,177,1)',
     pointBorderColor: '#fff',
     pointHoverBackgroundColor: '#fff',
     pointHoverBorderColor: 'rgba(148,159,177,0.8)'
   }
  ];

  public lineChartLegend:boolean = true;
  public lineChartType:string = 'line';

  public randomize():void {
   let _lineChartData:Array<any> = new Array(this.lineChartData.length);
   for (let i = 0; i < this.lineChartData.length; i++) {
     _lineChartData[i] = {data: new Array(this.lineChartData[i].data.length), label: this.lineChartData[i].label};
     for (let j = 0; j < this.lineChartData[i].data.length; j++) {
       _lineChartData[i].data[j] = Math.floor((Math.random() * 100) + 1);
     }
   }
   this.lineChartData = _lineChartData;
  }

  // events
  public chartClicked(e:any):void {
   console.log(e);
  }

  public chartHovered(e:any):void {
   console.log(e);
  }


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
              var date = new Date(measurementRef["Time Stamp"]);
              this.lineChartLabels.push(date);
              this.lineChartData[0].data.push(+measurementRef["Value"]);

           }

           console.log(this.dataHolder);

           console.log(this.lineChartData[0]);
    })
}

ngOnDestroy() {
    this.sub.unsubscribe();
}

}
