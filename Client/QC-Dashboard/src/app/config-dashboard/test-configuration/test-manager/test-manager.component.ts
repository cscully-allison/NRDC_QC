import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'test-manager',
  templateUrl: './test-manager.component.html',
  styleUrls: ['./test-manager.component.css']
})
export class TestmanagerComponent implements OnInit {
  @Input() testParameters: Object;
  private arrayParams: Array<Object>;
  formModified:boolean;
  testTitle: string;

  constructor() {
      this.arrayParams = new Array<Object>();
  }

  ngOnInit() {

  }

  undoChanges(){
    for(var param of this.arrayParams){
      param['newValue'] = null;
    }

    this.formModified = false;
  }

  updateNewValue(param:Object, event:any){
      param['newValue'] = event.target.value;
      this.formModified = true;

      console.log(param)
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
        tempArray.push({'key':key,'value':object[key], 'displaykey':this.formatForDisplay(key)});
      }

      return tempArray;
  }

  formatForDisplay(keyString:string):string{
    var temp:string = "";

    //check first letter
    for(var letter = 0; letter < keyString.length; letter++){

      if(letter == 0){
          temp += keyString[letter].toUpperCase();
      }
      else if(keyString[letter].toUpperCase() != keyString[letter]){
          temp += keyString[letter];
      }
      else if(keyString[letter].toUpperCase() == keyString[letter]){
          temp += " "+ keyString[letter];
      }

    }

    return temp;
  }

}
