import { shapes }  from 'jointjs';

class RelationGraphModel {

    constructor(classes){
        this.uml = shapes.uml;
        this.relationClasses = classes;
        this.classes = {};
        this.parseIntoGraphModel();
    }

    
   
    parseIntoGraphModel(){
        let heightAdjust = 50 ;
        let widthAdjust = 100 ;
        for(let index in this.relationClasses){
            
            
            let attributeArray = []; //need to turn attributes into correct format name : dataType
            for(let attribute in this.relationClasses[index].attributes){
                let convertedAttribute = '';
                if(this.relationClasses[index].attributes[attribute].attributeName === 'self'){ 
                    // do nothing
                }
                else{
                    if(this.relationClasses[index].attributes[attribute].isPathFunctionalDependency){
                        convertedAttribute = '{'+ this.relationClasses[index].attributes[attribute].attributeName + " : "+ this.relationClasses[index].attributes[attribute].dataType+'} -> self';
                    }
                    else{
                        convertedAttribute = this.relationClasses[index].attributes[attribute].attributeName + " : "+ this.relationClasses[index].attributes[attribute].dataType;
                    }
                    attributeArray.push(convertedAttribute); 
                }
            }

            let tempObject = {
                position: { x: widthAdjust  , y: heightAdjust }, // adjust height
                size: { width: 260, height: (attributeArray.length * 25) + 25 },           // standard width and height variabled by number of attributes
                name: this.relationClasses[index].name,
                attributes: ['*Self'],                      // we want to structure arm so thta self appears in the standard attributes section of an uml
                methods: attributeArray,
                attrs: {
                    '.uml-class-name-rect': {
                        fill: '#fff',
                        stroke: '#000',
                        'stroke-width': 0.5
                    },
                    '.uml-class-attrs-rect': {
                        fill: '#fff',
                        stroke: '#000',
                        'stroke-width': 0.5
                    },
                    '.uml-class-methods-rect': {
                        fill: '#fff',
                        stroke: '#000',
                        'stroke-width': 0.5
                    },
                    '.uml-class-methods-text, .uml-class-attrs-text': {
                        fill: '#fff'
                    }
                }
            };
            this.classes[tempObject.name] = new this.uml.Class(tempObject); // assign key value pair - class name to class object
            
            heightAdjust += 150;
            widthAdjust += 100;
            
            
        }
    }
}

export default RelationGraphModel;