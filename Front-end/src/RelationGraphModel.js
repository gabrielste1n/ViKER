import { shapes }  from 'jointjs';

class RelationGraphModel {

    constructor(classes){
        this.uml = shapes.uml;
        this.relationClasses = classes;
        this.classes = {};
        this.parseIntoGraphModel();
    }

       // parses the initial object into  an object that can be used to render the relation graph
    parseIntoGraphModel(){

        let heightAdjust = 50 ;
        let widthAdjust = 100 ;
        let pathAttrs = [];
        let pathFD = 'pathFD(';

        for(let index in this.relationClasses){
            
            
            let attributeArray = []; //need to turn attributes into correct format name : dataType
            for(let attribute in this.relationClasses[index].attributes){
                let convertedAttribute = '';
                
                if(this.relationClasses[index].attributes[attribute].attributeName === 'self'){ 
                    // do nothing
                }
                else{
                    let name = this.relationClasses[index].attributes[attribute].attributeName;
                    let type = this.relationClasses[index].attributes[attribute].dataType;

                    if(this.relationClasses[index].attributes[attribute].isFK){ //checking to see if it is a foreign key
                        name = name + '*';
                    }

                    if(this.relationClasses[index].attributes[attribute].isPathFunctionalDependency ){ //if in first table
                        pathAttrs.push(name);
                    }
                     // normal attribute
                    convertedAttribute = name + " : "+ type;
                    attributeArray.push(convertedAttribute); 
                }
            }
        
            //creating object to store graph info
            let tempObject = {
                position: { x: widthAdjust  , y: heightAdjust }, // adjust height
                size: { width: (pathAttrs.length * 80) + 150, height: (attributeArray.length * 25) + 25 },           // standard width and height variabled by number of attributes
                name: this.relationClasses[index].name,
                attributes: [(pathFD + pathAttrs.join(',')+ ') -> self')],                      // we want to structure arm so that self appears in the standard attributes section of an uml
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
                    },
                    text:{
                        style: { fontFamily: 'Roboto'  },
                    }
                }
            };
            this.classes[tempObject.name] = new this.uml.Class(tempObject); // assign key value pair - class name to class object
            
            heightAdjust += 150; //adjust the position of object
            widthAdjust += 100;
            
            pathAttrs = []; //reset path functional entities

        }
    }
}

export default RelationGraphModel;