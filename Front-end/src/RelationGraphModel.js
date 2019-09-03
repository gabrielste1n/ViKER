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
        let innerPFDCounter = 0;
        let outerPFDCounter = 0; //counts how many path funcitonal dependencies there are
        let self = '} -> self';
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

                    if(this.relationClasses[index].attributes[attribute].isPathFunctionalDependency && outerPFDCounter === 0 ){ //if in first table
                        convertedAttribute = '{'+ name + " : "+ type + self;
                        outerPFDCounter++;
                    }
                    else{
                        
                        if(this.relationClasses[index].attributes[attribute].isPathFunctionalDependency && innerPFDCounter === 0){ //first pfd in 2nd table
                            console.log('gets hit');
                            convertedAttribute = '{'+ name + " : "+ type;
                            innerPFDCounter++;
                        }else{
                            if(this.relationClasses[index].attributes[attribute].isPathFunctionalDependency && innerPFDCounter > 0){ //not the first pfd in 2nd table
                                convertedAttribute = name + " : "+ type;
                                innerPFDCounter++;
                            }
                        }
                        if(this.relationClasses[index].attributes[attribute].isPathFunctionalDependency && innerPFDCounter === 0 && type === 'OID'){ //last pfd in 2nd table
                            convertedAttribute = '{'+ name + " : "+ type + self;
                            innerPFDCounter++;
                        }
                        if(this.relationClasses[index].attributes[attribute].isPathFunctionalDependency && innerPFDCounter > 0 && type === 'OID'){ //last pfd in 2nd table
                            convertedAttribute = name + " : "+ type + self;
                            innerPFDCounter++;
                        }
                        if(!this.relationClasses[index].attributes[attribute].isPathFunctionalDependency){ // normal attribute
                            convertedAttribute = name + " : "+ type;
                        }
                    }
                    
                    attributeArray.push(convertedAttribute); 
                }
            }
        
            //creating object to store graph info
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