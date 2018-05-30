import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { HierarchyNavigator } from './safe-navigator';

@Component({
  selector: 'app-test-configuration',
  templateUrl: './test-configuration.component.html',
  styleUrls: ['./test-configuration.component.css']
})
export class TestConfigurationComponent implements OnInit {


  public mHierarchy:object;
  public navlist:object[];
  public safeNav:HierarchyNavigator;

  constructor(private http:HttpClient) {
    this.mHierarchy = new Object;
    this.navlist = new Array<Object>();
    this.initializeNavigation();
    this.safeNav = new HierarchyNavigator(0, 1, this.mHierarchy);
    this.navlist = this.safeNav.getCurrent();
  }

  ngOnInit() {
  }

  initializeNavigation(){
      //this will be replaced with calls to apis
      this.mHierarchy['networks'] = {tier: "Network", 1:[{name: "Walker Basin Hydroclimate", id:1}, {name: "Nexus", id:2}]};
      this.mHierarchy['sites'] = {tier: "Site", 1:[{name:"Rockland Summit", id:1}]}; //organized by the id of the parent
      this.mHierarchy['systems'] = {tier: "System", 1:[{name:"Meterological", id:1}]};
      this.mHierarchy['deployments'] = {tier: "Deployment", 1:[{name:"Air temperature (10-meter) monitor", id:1}, {name:"Air temperature (2-meter) monitor", id:2}]};
      this.mHierarchy['datastreams'] = {tier: "Data Stream",
                                1:[{name:"10 Minute Max", id:1},
                                {name:"10 Minute Min", id:2},
                                {name:"10 Minute Average", id:3}],
                                2:[{name:"1 Minute Max", id:4},
                                {name:"1 Minute Min", id:5},
                                {name:"1 Minute Average", id:6}]};
      this.mHierarchy['tests'] = {Tier:"Test",
       1:[{name:"Bounds Test", id:1},
        {name:"Repeat Value Test", id:2}],
        2:[{name:"Bounds Test", id:4},
        {name:"Repeat Value Test", id:5}],
        4:[{name:"Bounds Test", id:6}],
        5:[{name:"Repeat Value Test", id:6}]};

  }

  getNextNavList(id, name){
        console.log(name);
        this.navlist = this.safeNav.getNext(id, name);

  }

  getTestConfigData(dsID){
    this.http.get('https://sensor.nevada.edu/GS/Services/Config/GetTests/dsID').subscribe(
      data => {
          console.log(data);
      })

  }

  //navigates the use rback to the tier they click on
  //in the nav history menu
  onNotify(message:object):void {
      this.navlist = this.safeNav.setViewToSpecificLevel(message['level'], message['id']);
    }

}
