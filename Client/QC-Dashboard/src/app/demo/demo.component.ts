import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {
  trigger,
  state,
  style,
  animate,
  transition
} from '@angular/animations';

@Component({
  selector: 'app-demo',
  templateUrl: './demo.component.html',
  styleUrls: ['./demo.component.css'],
  animations: [
  trigger('activity', [
    state('inactive', style({
      visibility: 'none',
      backgroundColor: '#eee',
      transform: 'scale(1)'
    })),
    state('active',   style({
      backgroundColor: '#cfd8dc',
      transform: 'scale(1.1)'
    })),
    transition('inactive => active', animate('100ms ease-in')),
    transition('active => inactive', animate('100ms ease-out'))
  ])
]
})
export class DemoComponent implements OnInit {

  public loading = false;
  public done = false;
  public numtests = 0;
  public data = {};

  constructor(private http: HttpClient) { }

  ngOnInit() {

  }

  demo(){
      this.loading = true;
      this.http.get('https://sensor.nevada.edu/GS/Services/Demo/Config/', { headers: new HttpHeaders({ timeout: `${60000}` }) })
      .subscribe(
        data => { this.http.get('https://sensor.nevada.edu/GS/Services/Demo/Run/')
                  .subscribe(data => {
                      this.loading = false;
                      this.data = data;
                      console.log(data);
                      this.done = true;
                      this.numtests = 0;
                      for(let stream in this.data["Measurements"]){
                          this.numtests += this.data["Measurements"][stream] * 3;
                      }
                  })
                },
        err => {
                this.http.get('https://sensor.nevada.edu/GS/Services/Demo/Run/')
                .subscribe(data => {
                        this.loading = false;
                        this.data = data;
                        console.log(data);
                        this.done = true;
                        this.numtests = 0;
                        for(let stream in this.data["Measurements"]){
                            this.numtests += this.data["Measurements"][stream] * 3;
                        }
                })
        }
     )
  }

}
