import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-flags-by-datastream',
  templateUrl: './flags-by-datastream.component.html',
  styleUrls: ['./flags-by-datastream.component.css']
})
export class FlagsByDatastreamComponent implements OnInit {

  id = -1;
  sub = null;
  flagData = {};

  constructor(private aroute:ActivatedRoute, private http:HttpClient) {

  }

  ngOnInit() {
    this.sub = this.aroute.params.subscribe(params => this.id = params["id"]);
    this.http.get('http://sensor.nevada.edu/GS/Services/Flag/L1/'+this.id).subscribe(
     data => {
         console.log(data)
         this.flagData = data;

         this.getFlagCounts(data);
     })
  }

  ngOnDestroy() {
   this.sub.unsubscribe();
  }

  getFlagCounts(returnedFlags:object):object{
      var countsObject = {};

      for(let dsid in returnedFlags){
          if(!Number.isNaN(+dsid)){
              countsObject[dsid] = {};
              countsObject[dsid]["Deployment Name"] =  returnedFlags[dsid]["Deployment Name"];
              countsObject[dsid]["flagCount"] = returnedFlags[dsid]["Measurements"].length;
          }
      }

      console.log(countsObject);
      return countsObject;
  }

}
