export class HierarchyNavigator{
    private level:number;
    private id:number;
    private hierarchy:string[];
    private metadata:object;
    private navHistory:object[];
    public isNavView:Boolean;

    constructor(level, id, metadata){
        this.isNavView = true;
        this.level = level;
        this.id = id;
        this.hierarchy = ["networks","sites","systems","deployments","datastreams","tests"];
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
        return this.hierarchy[this.level];
    }

    getCurrentLevelTitle(){
       var title:string = this.hierarchy[this.level];
       title = title.slice(0, -1); //remove
       title = title[0].toUpperCase() + title.slice(1,); //make first letter uppercase
       return title;
    }

    getCurrent(){
      return this.metadata[this.hierarchy[this.level]][this.id];
    }


    //Forward navigation
    getNext(id, name){
        if(this.level+1 < this.hierarchy.length){
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

    private storeHistory(id, name, title){
        if(this.level+1 < this.hierarchy.length){
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
      if(this.level+1 < this.hierarchy.length){
          this.level++;
      }else{
        //do nothing
      }
    }




}