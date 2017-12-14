import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-demo',
  templateUrl: './demo.component.html',
  styleUrls: ['./demo.component.css']
})
export class DemoComponent implements OnInit {

  public loading = false;
  public done = false;
  public data = {};

  constructor(private http: HttpClient) { }

  ngOnInit() {

  }

  demo(){
      this.loading = true;
      this.http.get('https://sensor.nevada.edu/GS/Services/Demo/Config/', { headers: new HttpHeaders({ timeout: `${60000}` }) })
      .subscribe(
        data => { this.loading = false;
                  this.http.get('https://sensor.nevada.edu/GS/Services/Demo/Run/')
                  .subscribe(data => {this.data = data; console.log(data); this.done = true;})
                },
        err => {
                this.loading = false;
                this.http.get('https://sensor.nevada.edu/GS/Services/Demo/Run/')
                .subscribe(data => {this.data = data; console.log(data); this.done = true;})
                }
     )
  }

}
