import { shapes }  from 'jointjs';

class EntityGraphModel {

    constructor(classes){
        this.uml = shapes.uml;
        this.entityClasses = classes;
        this.classes = {};
        this.composedClasses = {};
        this.erd = shapes.erd;
        this.parseIntoGraphModel(); 
    }

    
   
    parseIntoGraphModel(){
        
        let horAdj = 0;
        let vertAdj = 0;
       for(let index in this.entityClasses){
           for(let attr in this.entityClasses[index].attributes){
            let tempObject = {
                position: { x: 10 + horAdj, y: 150 + vertAdj},
                attrs: {
                    text: {
                        fill: '#000',
                        text: this.entityClasses[index].attributes[attr].attributeName,
                        letterSpacing: 0,
                        style: { textShadow: '1px 0 1px #333333' },
                        fontSize: 10
                    },
                    '.outer': {
                        fill: '#fff',
                        stroke: '#fff',
                        filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 2, color: '#222138' }}
                    }
                }
            };
            if(this.entityClasses[index].attributes[attr].isIdentifier){                                           //check to see if foreign key or not
                this.classes[this.entityClasses[index].attributes[attr].attributeName] = new this.erd.Key(tempObject);
            }
            else{
                this.classes[this.entityClasses[index].attributes[attr].attributeName] = new this.erd.Normal(tempObject);
            }
            horAdj+=100;
            vertAdj+=35;

            if(this.entityClasses[index].attributes[attr].composedOf.length > 0){
                this.composedClasses[this.entityClasses[index].attributes[attr].attributeName] = this.entityClasses[index].attributes[attr].composedOf;
            }
           }
        
       }
}

}

export default EntityGraphModel;