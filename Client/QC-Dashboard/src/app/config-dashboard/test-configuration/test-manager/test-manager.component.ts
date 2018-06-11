import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Component({
  selector: 'test-manager',
  templateUrl: './test-manager.component.html',
  styleUrls: ['./test-manager.component.css']
})
export class TestmanagerComponent implements OnInit {
  @Input() testParameters: Object;
  @Input() dsID:number;
  private arrayParams: Array<Object>;
  formModified:boolean;
  testTitle: string;
  editable: boolean;

  constructor(private http:HttpClient) {
      this.arrayParams = new Array<Object>();
      this.editable = false;
  }

  ngOnInit() {

  }

  toggleEditing(){
    this.editable = !(this.editable);
  }

  saveChanges(){
    var modifiedParams:Object = new Object();

    this.applyArrayToObject(this.arrayParams);

    modifiedParams[this.dsID] = this.testParameters;

    this.http.post('https://sensor.nevada.edu/GS/Services/Config/ModifyTests/', modifiedParams).subscribe(
      data => {
        console.log(data);
      }
    )

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


  applyArrayToObject(arrayParams){

      for(var i = 0; i < arrayParams.length; i++){
          console.log(arrayParams[i]['newValue'])
          if(arrayParams[i]['newValue'] != null){
            this.testParameters[arrayParams[i]['key']] = arrayParams[i]['newValue'];
          }
      }

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
