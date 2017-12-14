import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-demo',
  templateUrl: './demo.component.html',
  styleUrls: ['./demo.component.css']
})
export class DemoComponent implements OnInit {

  public loading = true;

  constructor(private http: HttpClient) { }

  ngOnInit() {
      this.http.get('http://sensor.nevada.edu/GS/Services/Demo/').subscribe(
        data => {
            console.log(data);
        })
  }

}
