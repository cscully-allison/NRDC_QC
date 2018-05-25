export class HierarchyNavigator{
    private level:number;
    private id:number;
    private hierarchy:string[];
    private metadata:object;
    private navHistory:object[];

    constructor(level, id, metadata){
        this.level = level;
        this.id = id;
        this.hierarchy = ["networks","sites","systems","deployments","datastreams","tests"];
        this.metadata = metadata;
        this.navHistory = new Array<Object>();
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

    getNext(id, name){
        if(this.level+1 < this.hierarchy.length){
          this.storeHistory(id, name);
          this.incrementLevel();
          this.id = id;
          return this.getCurrent();
        } else {
          return this.getCurrent();
        }
    }

    private storeHistory(id,name){
        if(this.level+1 < this.hierarchy.length){
          this.navHistory.push({id:id, name:name})
          console.log(this.navHistory)
        }
    }

    getPrior(){

    }

    private incrementLevel(){
      if(this.level+1 < this.hierarchy.length){
          this.level++;
      }else{
        //do nothing
      }
    }

}
