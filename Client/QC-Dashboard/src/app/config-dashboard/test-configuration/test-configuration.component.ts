import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HierarchyNavigator } from './safe-navigator';

@Component({
  selector: 'app-test-configuration',
  templateUrl: './test-configuration.component.html',
  styleUrls: ['./test-configuration.component.css']
})
export class TestConfigurationComponent implements OnInit {


  public mHierarchy:object;
  public hierarchyOntology:Array<string>;
  public queryableOntology:Array<string>;
  public navlist:object[];
  public safeNav:HierarchyNavigator;
  public testParameters:object;
  public dsID:number;
  public newTests:object[];
  public metadataSource:string;

  constructor(private http:HttpClient) {
    this.mHierarchy = new Object;
    this.navlist = new Array<Object>();
    this.initializeNavigation();
    this.hierarchyOntology = ['SiteNetworks', 'Sites', 'Systems', 'Deployments', 'Datastreams', "tests"];
    this.queryableOntology = ['SiteNetworks', 'Sites', 'Systems', 'Deployments']
    this.safeNav = new HierarchyNavigator(0, 1, this.mHierarchy, this.hierarchyOntology);
    this.navlist = this.safeNav.getCurrent();
    this.newTests = new Array<Object>();
    this.metadataSource = "http://sensor.nevada.edu/Services/nrdc/infrastructure/Services/";
    this.getAllNavLists();

  }

  ngOnInit() {
  }

  initializeNavigation(){
      //this will be replaced with calls to apis
      this.mHierarchy['SiteNetworks'] = {tier: "Network", 1:[{name: "Walker Basin Hydroclimate", id:1}, {name: "Nexus", id:2}]};
      this.mHierarchy['Sites'] = {tier: "Site", 1:[{name:"Rockland Summit", id:1}]}; //organized by the id of the parent
      this.mHierarchy['Systems'] = {tier: "System", 1:[{name:"Meterological", id:1}]};
      this.mHierarchy['Deployments'] = {tier: "Deployment", 1:[{name:"Air temperature (10-meter) monitor", id:1}, {name:"Relative Humidity Monitor", id:2}]};
      this.mHierarchy['Datastreams'] = {tier: "Data Stream",
                                1:[{name:"10 Minute Max", id:66},
                                {name:"10 Minute Min", id:63},
                                {name:"10 Minute Average", id:54}],
                                2:[{name:"1 Minute Max", id:55},
                                {name:"1 Minute Min", id:56},
                                {name:"1 Minute Average", id:57}]};
      this.mHierarchy['tests'] = {Tier:"Test",
       1:[{name:"Bounds Test", id:1},
        {name:"Repeat Value Test", id:2}],
        2:[{name:"Bounds Test", id:4},
        {name:"Repeat Value Test", id:5}],
        4:[{name:"Bounds Test", id:6}],
        5:[{name:"Repeat Value Test", id:6}]};

  }

  renderTest(testParameters:object){
      this.testParameters = testParameters;
      this.safeNav.setTestView();
  }

  getAllNavLists(){
      var fullHTTP;

      fullHTTP = this.metadataSource + "SiteNetworks.svc/Get"
      console.log(fullHTTP)
      this.http.get(fullHTTP).subscribe(
        data => {
          console.log(data);
        }
      )
      //
      // for(let name of this.queryableOntology){
      //     fullHTTP = this.metadataSource + name + ".svc/Get"
      //     console.log(fullHTTP)
      //     this.http.get(fullHTTP).subscribe(
      //       data => {
      //         console.log(data);
      //       }
      //     )
      // }

  }

  getNextNavList(id, name){
        console.log(name);
        this.navlist = this.safeNav.getNext(id, name);

  }

  getTestConfigData(dsID, name){
    var flag:boolean = false;
    var possibleTests:Array<Object> = [{Type:"Bounds", Min: null, Max: null }, {Type:"Repeat Value", RepeatThreshold: null}]; //Oh man makin some may comprimises. . . these should be passed down from original xml test metadata, test ontology?

    this.dsID = dsID;
    this.http.get('https://sensor.nevada.edu/GS/Services/Config/GetTests/'+dsID).subscribe(
      data => {
          console.log(data);
          this.newTests = [];
          this.safeNav.getNext(dsID, name);
          this.navlist = data as Array<object>;
          for(let possibleTest of possibleTests){
              if(! this.navlist.find( existingTest => existingTest['Type'] == possibleTest['Type'])){
                  this.newTests.push(possibleTest);
              }

          }

      });

  }

  //navigates the use rback to the tier they click on
  //in the nav history menu
  onNotify(message:object):void {
      this.navlist = this.safeNav.setViewToSpecificLevel(message['level']);
    }

}
