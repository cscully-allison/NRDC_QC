import { HttpClient } from '@angular/common/http';


export class HierarchyNavigator{
    private level:number;
    private id:number;
    private hierarchyOntology:string[];
    private metadata:object;
    private navHistory:object[];
    public isNavView:Boolean;

    constructor(level, id, metadata, hierarchyOntology){
        this.isNavView = true;
        this.level = level;
        this.id = id;
        this.hierarchyOntology = hierarchyOntology;
        this.metadata = metadata;
        this.navHistory = new Array<Object>();
    }


    //getters
    getCurrentLevel(){
        return this.level;
    }

    getCurrentId(){
        return this.id;
    }

    getCurrentLevelName(){
        return this.hierarchyOntology[this.level];
    }

    getNavHistory(){
      return this.navHistory;
    }

    getCurrentLevelTitle(){
       var title:string = this.hierarchyOntology[this.level];
       title = title.slice(0, -1); //remove
       title = title[0].toUpperCase() + title.slice(1,); //make first letter uppercase
       return title;
    }

    getCurrent(){
      return this.metadata[this.hierarchyOntology[this.level]][this.id];
    }

    peekNext(id, name){
      //this retirves the information related to a hovered item, filters it according to the actual item being hovered over, and sends back only the additional metadata about the item
      return this.metadata[this.hierarchyOntology[this.level]][this.id].filter(object => object['name'] == name)[0]['otherdata'];
    }


    //Forward navigation
    getNext(id, name){
        if(this.level+1 < this.hierarchyOntology.length){
          this.storeHistory(id, name, this.getCurrentLevelTitle());
          this.incrementLevel();
          this.id = id;
          return this.getCurrent();
        }
        else {
          return this.getCurrent();
        }
    }

    setTestView(){
        this.isNavView = false;
    }

    setNavView(){
      this.isNavView = true;
    }

    private storeHistory(id, name, title){
        if(this.level+1 < this.hierarchyOntology.length){
          this.navHistory.push({id:id, level:this.level, name:name, levelTitle:title})
          console.log(this.navHistory)
        }
    }

    //---- Navigation from side menu ---//

    //function to set view to a specific level
    // when we click on the history element
    setViewToSpecificLevel(level){
        this.isNavView = true;
        this.modifyHistory(this.level, level);

        //account for error where initial site network list is id'd as 1
        this.level = level;
        if(level == 0){
          this.id = 1;
        }
        //all other attempts to navigate back to other levels
        // get's the id of the prior clicked item as stored in history
        else {
          this.id = this.navHistory[this.navHistory.length-1]['id'];
        }

        return this.getCurrent();
    }

    //adjusts the history to get us back to the original level
    modifyHistory(currentLevel, newLevel){
        for(var i = 0; i < currentLevel - newLevel; i++){
            this.navHistory.pop();
        }
    }


    //increments our level safely
    private incrementLevel(){
      if(this.level+1 < this.hierarchyOntology.length){
          this.level++;
      }else{
        //do nothing
      }
    }




}
