import React from 'react';
import ReactDOM from 'react-dom';
import { dia, shapes, g, V}  from 'jointjs';
import EntityGraphModel from './EntityGraphModel';

class OutputGraph extends React.Component {

    constructor(props) {
        super(props);
        this.graph = new dia.Graph();
    }

    componentDidMount() {
        this.paper = new dia.Paper({
            el: ReactDOM.findDOMNode(this.refs.placeholder),
            width: 900,
            height: 900,
            model: this.graph,
            gridSize: 1,
            linkPinning: false,
            defaultConnectionPoint: function(line, view) {
                var element = view.model;
                return element.getConnectionPoint(line.start) || element.getBBox().center();
            }
        });

        let graph = this.graph;
        let erd = shapes.erd;

        // Custom highlighter - display an outline around each element that fits its shape.

var highlighter = V('path', {
    'stroke': '#fff',
    'stroke-width': '2px',
    'fill': 'transparent',
    'pointer-events': 'none'
});

// Define a specific highligthing path for every shape.

erd.Attribute.prototype.getHighlighterPath = function(w, h) {

    return ['M', 0, h / 2, 'A', w / 2, h / 2, '0 1,0', w, h / 2, 'A', w / 2, h / 2, '0 1,0', 0, h / 2].join(' ');
};

erd.Entity.prototype.getHighlighterPath = function(w, h) {

    return ['M', w, 0, w, h, 0, h, 0, 0, 'z'].join(' ');
};

erd.Relationship.prototype.getHighlighterPath = function(w, h) {

    return ['M', w / 2, 0, w, w / 2, w / 2, w, 0, w / 2, 'z'].join(' ');
};

erd.ISA.prototype.getHighlighterPath = function(w, h) {

    return ['M', -8, 1, w + 8, 1, w / 2, h + 2, 'z'].join(' ');
};

// Define a specific connection points for every shape

erd.Attribute.prototype.getConnectionPoint = function(referencePoint) {
    // Intersection with an ellipse
    return g.Ellipse.fromRect(this.getBBox()).intersectionWithLineFromCenterToPoint(referencePoint);
};

erd.Entity.prototype.getConnectionPoint = function(referencePoint) {
    // Intersection with a rectangle
    return this.getBBox().intersectionWithLineFromCenterToPoint(referencePoint);
};

erd.Relationship.prototype.getConnectionPoint = function(referencePoint) {
    // Intersection with a rhomb
    var bbox = this.getBBox();
    var line = new g.Line(bbox.center(), referencePoint);
    return (
        line.intersection(new g.Line(bbox.topMiddle(), bbox.leftMiddle())) ||
        line.intersection(new g.Line(bbox.leftMiddle(), bbox.bottomMiddle())) ||
        line.intersection(new g.Line(bbox.bottomMiddle(), bbox.rightMiddle())) ||
        line.intersection(new g.Line(bbox.rightMiddle(), bbox.topMiddle()))
    );
};

erd.ISA.prototype.getConnectionPoint = function(referencePoint) {
    // Intersection with a triangle
    var bbox = this.getBBox();
    var line = new g.Line(bbox.center(), referencePoint);
    return (
        line.intersection(new g.Line(bbox.origin(), bbox.topRight())) ||
        line.intersection(new g.Line(bbox.origin(), bbox.bottomMiddle())) ||
        line.intersection(new g.Line(bbox.topRight(), bbox.bottomMiddle()))
    );
};

const createLink = function(elm1, elm2) {

    var myLink = new erd.Line({
        markup: [
            '<path class="connection" stroke="black" d="M 0 0 0 0"/>',
            '<path class="connection-wrap" d="M 0 0 0 0"/>',
            '<g class="labels"/>',
            '<g class="marker-vertices"/>'
        ].join(''),
        source: { id: elm1.id },
        target: { id: elm2.id }
    });

    return myLink.addTo(graph);
};

const createDashedLink = function(elm1, elm2) {

    let myLink = new erd.Line({
        markup: [
            '<path class="connection" stroke="black" stroke-dasharray="2,5"  d="M 0 0 0 0"/>',
            '<path class="connection-wrap" d="M 0 0 0 0"/>',
            '<g class="labels"/>',
            '<g class="marker-vertices"/>'
            ].join(''),
        source: { id: elm1.id },
        target: { id: elm2.id }
    });

    return myLink.addTo(graph);
};

// create labels for entity to entity multiplicity
var createLabel = function(txt) {
    return {
        labels: [{
            position: -20,
            attrs: {
                text: { dy: -8, text: txt, fill: '#000', fontFamily: 'Roboto' },
                rect: { fill: 'none' }
            }
        }]
    };
};


// Unbind orignal highligting handlers.
this.paper.off('cell:highlight cell:unhighlight');

// Bind custom ones.
this.paper.on('cell:highlight', function(cellView) {

    var padding = 5;
    var bbox = cellView.getBBox({ useModelGeometry: true }).inflate(padding);

    highlighter.translate(bbox.x, bbox.y, { absolute: true });
    highlighter.attr('d', cellView.model.getHighlighterPath(bbox.width, bbox.height));

    V(this.paper.viewport).append(highlighter);
});

this.paper.on('cell:unhighlight', function() {

    highlighter.remove();
});

// Create shapes

let graphModel = new EntityGraphModel(this.props.classes);
let classes = graphModel.classes;
let composedClasses = graphModel.composedClasses;

let entities = {}; //all entity graphable objects  
let relationAttributes = {}; //all relationAttributes
let relationIdentifiers = {}; //all relation indentifiers

let xAdj = 0;
let yAdj = 0;

// parse all entities and render to graph
for(let entity in this.props.classes){

    let name = this.props.classes[entity].name;
    let ent = null;

    if(this.props.classes[entity].isStrong){
        ent = new erd.Entity({ //entity is always the outer object - need to make sure this is a loop and gets all entities

            position: { x: 150 + xAdj, y: 100 + yAdj},
            attrs: {
                text: {
                    fill: '#000',
                    text: name,
                    letterSpacing: 0,
                    style: { textShadow: '1px 0 1px #333333', fontFamily: 'Roboto' },
                    fontSize: 10
                },
                '.outer': {
                    fill: '#fff',
                    stroke: 'none',
                    filter: { name: 'dropShadow',  args: { dx: 0.5, dy: 2, blur: 2, color: '#333333' }}
                }
            }
        });
    }else{
        ent = new erd.WeakEntity({ //entity is always the outer object - need to make sure this is a loop and gets all entities

            position: { x: 150 + xAdj, y: 100 + yAdj},
            attrs: {
                text: {
                    fill: '#000',
                    text: name,
                    letterSpacing: 0,
                    style: { textShadow: '1px 0 1px #333333', fontFamily: 'Roboto'  },
                    fontSize: 10
                },
                        '.inner': {
                             fill: '#fff',
                             stroke: '000',
                             points: '155,5 155,55 5,55 5,5'
                         },
                         '.outer': {
                             fill: '000',
                             stroke: '#fff',
                             points: '160,0 160,60 0,60 0,0',
                             filter: { name: 'dropShadow',  args: { dx: 0.5, dy: 2, blur: 2, color: '#000' }}
                         }
            }
        });
    }
    
    entities[name] = ent;
    graph.addCell(ent);
     xAdj = 300;
     yAdj = -50;

for(let rel in this.props.classes[entity].relationships)
    { 
        if(this.props.classes[entity].relationships[rel].relationAttributes.length > 0 || this.props.classes[entity].relationships[rel].RelationTypeLocal === 'ISA'){

            if(!relationIdentifiers[this.props.classes[entity].name] && !relationIdentifiers[this.props.classes[entity].relationships[rel].Entity]){

            if(this.props.classes[entity].relationships[rel].RelationTypeLocal !== 'ISA')
            {//create the indentifying relation

            relationIdentifiers[this.props.classes[entity].name] =  new erd.Relationship({

                     position: {x: ent.position.x , y: ent.position.y },
                     attrs: {
                         text: {
                             fill: '#ffffff',
                             text: '',
                             letterSpacing: 0,
                             style: { textShadow: '1px 0 1px #333333', fontFamily: 'Roboto'  }
                         },
                         '.outer': {
                             fill: '#fff',
                             stroke: 'none',
                             filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 1, color: '#333333' }}
                         }
                     }
                 });
                 graph.addCell(relationIdentifiers[this.props.classes[entity].name]);
                }else
                {
                    if(!relationIdentifiers[this.props.classes[entity].name] && !relationIdentifiers[this.props.classes[entity].relationships[rel].Entity])
                    {
                        relationIdentifiers[this.props.classes[entity].name] =  new erd.ISA({

                        position: {x: ent.position.x , y: ent.position.y },
                        attrs: {
                                 text: {
                                     text: 'ISA',
                                     fill: '#000',
                                     letterSpacing: 0,
                                     style: { 'text-shadow': '1px 0 1px #333333', fontFamily: 'Roboto'  }
                                 },
                                 polygon: {
                                     fill: '#fff',
                                     stroke: 'none',
                                     filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 1, color: '#333333' }}
                                 }
                             }
                         });

                         graph.addCell(relationIdentifiers[this.props.classes[entity].name]);
                        }
                 }

                 //adds the relation diamond to graoh
                 
                
                }

            //create the relationship attributes
            for(let relation in this.props.classes[entity].relationships[rel].relationAttributes)
            {
                if(!relationAttributes[relation]) //only if it doesnt already exist
               {
                   relationAttributes[relation] = new erd.Normal({
                position: { x: ent.position.x  , y: ent.position.y },
                attrs: {
                    text: {
                        fill: '#000',
                        text: this.props.classes[entity].relationships[rel].relationAttributes[relation],
                        letterSpacing: 0,
                        style: { textShadow: '1px 0 1px #333333', fontFamily: 'Roboto'  },
                        fontSize: 10
                    },
                    '.outer': {
                        fill: '#fff',
                        stroke: '#fff',
                        filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 2, color: '#222138' }}
                    }
                }
            });

            //add the relationship attributes to the graph
            graph.addCell(relationAttributes[relation]);
            createDashedLink(relationIdentifiers[this.props.classes[entity].name],relationAttributes[relation]); 

         }
        }

     }
    }
}

let tempArray = [];

//dictionary into array
for(let key in classes){
    tempArray.push(classes[key]);   
}

// create a dictionary e.g. customerAddress: [object, object, object]
let composedDictionary = {};
for(let key in composedClasses){
    composedDictionary[key] = [];
    for(let comp in composedClasses[key]){
            for(let normalKey in classes){
                if(composedClasses[key][comp] === normalKey){
                    classes[normalKey].attributes.position = {x: classes[normalKey].attributes.position.x ,y: classes[normalKey].attributes.position.y + 100};
                    composedDictionary[key].push(classes[normalKey]);
                    delete classes[normalKey];
            }
        }
    }
}

//add attributes to graph
graph.addCells(tempArray);

// create links to relationship types
for(let entity in this.props.classes){
    if(this.props.classes[entity].relationships){   //look for relation types
        for(let rel in this.props.classes[entity].relationships)
    { 
        if(this.props.classes[entity].relationships[rel].relationAttributes.length > 0 || this.props.classes[entity].relationships[rel].RelationTypeLocal === 'ISA' 
        || relationIdentifiers[this.props.classes[entity].name]){ //if there are relation attributes or ISA
            
            if(relationIdentifiers[this.props.classes[entity].name]){ //if i exist in the relation array - create link to diamond
                let textRel = '';
                switch(this.props.classes[entity].relationships[rel].RelationTypeLocal){
                    case 'ExactlyOne':
                        textRel = '1';
                        break;
                    case 'ZeroOrMany':
                        textRel = '0...N';
                        break;
                    case 'ISA':
                        textRel = '1';
                        break;
                    default:
                        break;
                }
                createLink(relationIdentifiers[this.props.classes[entity].name],entities[this.props.classes[entity].name]).set(createLabel(textRel))
            }
            else{
                let textRel = '';
                switch(this.props.classes[entity].relationships[rel].RelationTypeLocal){
                    case 'ExactlyOne':
                        textRel = '1';
                        break;
                    case 'ZeroOrMany':
                        textRel = '0...N';
                        break;
                    case 'ISA':
                        textRel = '1';
                        break;
                    default:
                        break;
                }
                createLink(relationIdentifiers[this.props.classes[entity].relationships[rel].Entity], entities[this.props.classes[entity].name]).set(createLabel(textRel));
            }
        }else
        {
            for(let relationship in this.props.classes[entity].relationships){
            if(entities[this.props.classes[entity].relationships[relationship].Entity]){
                if(!relationIdentifiers[this.props.classes[entity].name] && ( !relationIdentifiers[this.props.classes[entity].relationships[relationship].Entity] || !this.props.classes[entity].relationships[relationship].relationAttributes.length >0 )){
                    let textRel = '';
                switch(this.props.classes[entity].relationships[relationship].RelationTypeLocal){
                    case 'ExactlyOne':
                        textRel = '1';
                        break;
                    case 'ZeroOrMany':
                        textRel = '0...N';
                        break;
                    case 'ISA':
                        textRel = '1';
                        break;
                    default:
                        break;
                }
                   
                    createLink(entities[this.props.classes[entity].relationships[relationship].Entity], entities[this.props.classes[entity].name]).set(createLabel(textRel)); //create all the entity to entity links
                }
            }
        }
    }
        
    }
}
    else
    {
        for(let relationship in this.props.classes[entity].relationships){
        if(entities[this.props.classes[entity].relationships[relationship].Entity]){
            if(!relationIdentifiers[this.props.classes[entity].name]){
                let textRel = '';
                switch(this.props.classes[entity].relationships[relationship].RelationTypeLocal){
                    case 'ExactlyOne':
                        textRel = '1';
                        break;
                    case 'ZeroOrMany':
                        textRel = '0...N';
                        break;
                    case 'ISA':
                        textRel = '1';
                        break;
                    default:
                        break;
                }
                
                createLink(entities[this.props.classes[entity].name],entities[this.props.classes[entity].relationships[relationship].Entity]).set(createLabel(textRel)); //create all the entity to entity links
            }
        }
    }
}
}
//create links betweeen entities and their attributes
for(let key in classes){
    for(let entity in this.props.classes){
        for(let attribute in this.props.classes[entity].attributes){
            
            if(this.props.classes[entity].attributes[attribute].attributeName === key){
                for(let entityKey in entities){
                        if(entityKey === this.props.classes[entity].name){
                            createLink(entities[entityKey],classes[key]);
                        }
                }
                 //create all the normal links to entity
            }
        }
    }
}

//create links for composed attributes
for(let key in composedDictionary){
    for(let comp in classes){
        if(key === comp){
            for(let compA in composedDictionary[key]){
                createLink(classes[comp],composedDictionary[key][compA]); //create composed links
            }
        }
    }
     //create all the links
}

}

    render() {
        return <div ref="placeholder"></div>;
    }
}

export default OutputGraph;