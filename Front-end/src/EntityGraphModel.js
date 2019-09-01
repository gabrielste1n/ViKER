import { shapes }  from 'jointjs';

class EntityGraphModel {

    constructor(classes){
        this.uml = shapes.uml;
        this.entityClasses = classes;
        this.classes = {};
        this.parseIntoGraphModel();
    }

    
   
    parseIntoGraphModel(){
        let heightAdjust = 50 ;
        let widthAdjust = 100 ;
        for(let index in this.entityClasses){
            
            
            let attributeArray = [];  
            // for(let attribute in this.relationClasses[index].attributes){
            //     let convertedAttribute = this.relationClasses[index].attributes[attribute].attributeName + ": "+ this.relationClasses[index].attributes[attribute].dataType;
            //     if(this.relationClasses[index].attributes[attribute].attributeName !== 'self'){ attributeArray.push(convertedAttribute)};
            // }

            let tempObject = {
                position: { x: 175, y: 300 },
                attrs: {
                    text: {
                        fill: '#000',
                        text: 'CustomerPostalCode',
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
            this.classes[tempObject.name] = new this.uml.Class(tempObject); // assign key value pair - class name to class object
            
            heightAdjust += 150;
            widthAdjust += 100;
            
            
        }
    }
}

export default EntityGraphModel;