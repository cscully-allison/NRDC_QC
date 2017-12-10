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

  constructor(private aroute:ActivatedRoute, private http:HttpClient) {

  }

  ngOnInit() {
    this.sub = this.aroute.params.subscribe(params => this.id = params["id"]);
    this.http.get('http://sensor.nevada.edu/GS/Services/Flag/L1/'+this.id).subscribe(
     data => {
         console.log(data)
     })
  }

  ngOnDestroy() {
   this.sub.unsubscribe();
 }

}
