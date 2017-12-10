import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Router} from '@angular/router';

@Component({
  selector: 'app-flag-dashboard',
  templateUrl: './flag-dashboard.component.html',
  styleUrls: ['./flag-dashboard.component.css']
})



export class FlagDashboardComponent implements OnInit {

  // Doughnut
  public doughnutChartLabels:string[] = ['Repeat Value Flag', 'Out Of Bounds Flag', 'Missing Value Flag'];
  public flagIds:number[] = [1,2,3];
  public doughnutChartData:number[] = [0,0,210];
  public doughnutChartType:string = 'doughnut';

  public flagData:object

  // events
  public chartClicked(e:any):void {
    var flagid = this.flagIds[e.active[0]._index];

    this.router.navigateByUrl("/flag/" + flagid);


  }

  public chartHovered(e:any):void {
    console.log(e);
  }

  constructor(private http: HttpClient, private router:Router) {

  }

  ngOnInit() {
        this.http.get('https://sensor.nevada.edu/GS/Services/Flag/L1/').subscribe(
          data => {
              this.doughnutChartData = this.retrieveDataValues(data);
          })
          // this.http.get('http://sensor.nevada.edu/GS/Services/DataVis/Measurements/66').subscribe(
          //   data => {
          //       console.log(data)
          //   })

  }

   public retrieveDataValues(flagData:object):number[]{
      var values = new Array();

      for(let flag in flagData){
        values.push(flagData[flag]["Total Amount"]);
      }

      values.push(210);

      return values;
   }

}
