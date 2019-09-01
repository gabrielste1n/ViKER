import React from 'react';
import ReactDOM from 'react-dom';
import { dia, shapes, g, V}  from 'jointjs';

class OutputGraph extends React.Component {

    constructor(props) {
        super(props);
        this.graph = new dia.Graph();
    }

    componentDidMount() {
        this.paper = new dia.Paper({
            el: ReactDOM.findDOMNode(this.refs.placeholder),
            width: 720,
            height: 500,
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

var Customer = new erd.Entity({

    position: { x: 100, y: 200 },
    attrs: {
        text: {
            fill: '#000',
            text: 'Customer',
            letterSpacing: 0,
            style: { textShadow: '1px 0 1px #333333' },
            fontSize: 10
        },
        '.outer': {
            fill: '#fff',
            stroke: 'none',
            filter: { name: 'dropShadow',  args: { dx: 0.5, dy: 2, blur: 2, color: '#333333' }}
        }
        // '.inner': {
        //     fill: '#fff',
        //     stroke: 'none',
        //     filter: { name: 'dropShadow',  args: { dx: 0.5, dy: 2, blur: 2, color: '#333333' }}
        // }
    }
});

// var wage = new erd.WeakEntity({

//     position: { x: 530, y: 200 },
//     attrs: {
//         text: {
//             fill: '#ffffff',
//             text: 'Wage',
//             letterSpacing: 0,
//             style: { textShadow: '1px 0 1px #333333' }
//         },
//         '.inner': {
//             fill: '#31d0c6',
//             stroke: 'none',
//             points: '155,5 155,55 5,55 5,5'
//         },
//         '.outer': {
//             fill: 'none',
//             stroke: '#31d0c6',
//             points: '160,0 160,60 0,60 0,0',
//             filter: { name: 'dropShadow',  args: { dx: 0.5, dy: 2, blur: 2, color: '#333333' }}
//         }
//     }
// });

// var paid = new erd.IdentifyingRelationship({

//     position: { x: 350, y: 190 },
//     attrs: {
//         text: {
//             fill: '#ffffff',
//             text: 'Gets paid',
//             letterSpacing: 0,
//             style: { textShadow: '1px 0 1px #333333' }
//         },
//         '.inner': {
//             fill: '#7c68fd',
//             stroke: 'none'
//         },
//         '.outer': {
//             fill: 'none',
//             stroke: '#7c68fd',
//             filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 1, color: '#333333' }}
//         }
//     }
// });

// var isa = new erd.ISA({

//     position: { x: 125, y: 300 },
//     attrs: {
//         text: {
//             text: 'ISA',
//             fill: '#ffffff',
//             letterSpacing: 0,
//             style: { 'text-shadow': '1px 0 1px #333333' }
//         },
//         polygon: {
//             fill: '#fdb664',
//             stroke: 'none',
//             filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 1, color: '#333333' }}
//         }
//     }
// });

var CustomerID = new erd.Key({

    position: { x: 10, y: 90 },
    attrs: {
        text: {
            fill: '#000',
            text: 'CustomerID',
            letterSpacing: 0,
            style: { textShadow: '1px 0 1px #000' },
            fontSize: 10
        },
        '.outer': {
            fill: '#fff',
            stroke: 'none',
            filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 2, color: '#222138' }}
        }
    }
});

var CustomerName = new erd.Normal({

    position: { x: 75, y: 30 },
    attrs: {
        text: {
            fill: '#000',
            text: 'CustomerName',
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
});

var CustomerPostalCode = new erd.Normal({

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
});

var CustomerAddress = new erd.Normal({

    position: { x: 325, y: 30 },
    attrs: {
        text: {
            fill: '#000',
            text: 'CustomerAddress',
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
});


// var skills = new erd.Multivalued({

//     position: { x: 150, y: 90 },
//     attrs: {
//         text: {
//             fill: '#ffffff',
//             text: 'Skills',
//             letterSpacing: 0,
//             style: { 'text-shadow': '1px 0px 1px #333333' }
//         },
//         '.inner': {
//             fill: '#fe8550',
//             stroke: 'none',
//             rx: 43,
//             ry: 21

//         },
//         '.outer': {
//             fill: '#464a65',
//             stroke: '#fe8550',
//             filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 2, color: '#222138' }}
//         }
//     }
// });

// var amount = new erd.Derived({

//     position: { x: 440, y: 80 },
//     attrs: {
//         text: {
//             fill: '#ffffff',
//             text: 'Amount',
//             letterSpacing: 0,
//             style: { textShadow: '1px 0 1px #333333' }
//         },
//         '.inner': {
//             fill: '#fca079',
//             stroke: 'none',
//             display: 'block'
//         },
//         '.outer': {
//             fill: '#464a65',
//             stroke: '#fe854f',
//             'stroke-dasharray': '3,1',
//             filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 2, color: '#222138' }}
//         }
//     }
// });

// var uses = new erd.Relationship({

//     position: { x: 300, y: 390 },
//     attrs: {
//         text: {
//             fill: '#ffffff',
//             text: 'Uses',
//             letterSpacing: 0,
//             style: { textShadow: '1px 0 1px #333333' }
//         },
//         '.outer': {
//             fill: '#797d9a',
//             stroke: 'none',
//             filter: { name: 'dropShadow',  args: { dx: 0, dy: 2, blur: 1, color: '#333333' }}
//         }
//     }
// });

// Create new shapes by cloning

// var salesman = Customer.clone().translate(0, 200).attr('text/text', 'Salesman');

// var date = CustomerName.clone().position(585, 80).attr('text/text', 'Date');

// var car = Customer.clone().position(430, 400).attr('text/text', 'Company car');

// var plate = CustomerID.clone().position(405, 500).attr('text/text', 'Plate');


// Helpers

var createLink = function(elm1, elm2) {

    var myLink = new erd.Line({
        markup: [
            '<path class="connection" stroke="black" d="M 0 0 0 0"/>',
            '<path class="connection-wrap" d="M 0 0 0 0"/>',
            '<g class="labels"/>',
            '<g class="marker-vertices"/>'
            // '<g class="marker-arrowheads"/>'
        ].join(''),
        source: { id: elm1.id },
        target: { id: elm2.id }
    });

    return myLink.addTo(graph);
};

// var createLabel = function(txt) {
//     return {
//         labels: [{
//             position: -20,
//             attrs: {
//                 text: { dy: -8, text: txt, fill: '#ffffff' },
//                 rect: { fill: 'none' }
//             }
//         }]
//     };
// };

// Add shapes to the graph

// graph.addCells([Customer, salesman, wage, paid, isa, CustomerID, CustomerName, skills, amount, date, plate, car, uses]);
graph.addCells([Customer, CustomerID, CustomerName, CustomerAddress, CustomerPostalCode]);


// createLink(Customer, paid).set(createLabel('1'));
createLink(Customer, CustomerID);
createLink(Customer, CustomerName);
createLink(Customer, CustomerAddress);
createLink(Customer, CustomerPostalCode);
// createLink(Customer, skills).set(createLabel('1..1'));
// createLink(Customer, isa);
// createLink(isa, salesman);
// createLink(salesman, uses).set(createLabel('0..1'));
// createLink(car, uses).set(createLabel('1..1'));
// createLink(car, plate);
// createLink(wage, paid).set(createLabel('N'));
// createLink(wage, amount);
// createLink(wage, date);

    }

    render() {
        return <div ref="placeholder"></div>;
    }
}

export default OutputGraph;