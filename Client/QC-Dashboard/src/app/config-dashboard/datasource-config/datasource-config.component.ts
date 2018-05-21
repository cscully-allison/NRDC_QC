import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-datasource-config',
  templateUrl: './datasource-config.component.html',
  styleUrls: ['./datasource-config.component.css']
})
export class DatasourceConfigComponent implements OnInit {

  public SetupOptions = ['API', 'Database Connection', 'Flat File']

  constructor() { }

  ngOnInit() {
  }

}
