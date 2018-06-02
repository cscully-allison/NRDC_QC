import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'test-manager',
  templateUrl: './test-manager.component.html',
  styleUrls: ['./test-manager.component.css']
})
export class TestmanagerComponent implements OnInit {
  @Input() testParameters: Object;
  private arrayParams: Array<Object>;
  testTitle: string;

  constructor() {
      this.arrayParams = new Array<Object>();
  }

  ngOnInit() {

  }

  ngOnChanges(changes: SimpleChanges){
       var tempArray:Object[] = this.objectToArray(this.testParameters);

      for(var indx=0; indx < tempArray.length; indx++){
          if(tempArray[indx]['key'] == 'Type'){
            this.testTitle = tempArray[indx]['value'];
            tempArray.splice(indx, 1);
          }
      }

      this.arrayParams = tempArray;
  }

  objectToArray(object){
      var tempArray:Object[] = new Array<Object>();

      for(let key in object){
        tempArray.push({'key':key,'value':object[key]});
      }

      return tempArray;
  }

}
