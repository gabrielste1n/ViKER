import React from 'react';
import ReactDOM from 'react-dom';
import { dia, shapes}  from 'jointjs';

class InputGraph extends React.Component {

    constructor(props) {
        super(props);
        this.graph = new dia.Graph();
    }

    componentDidMount() {
        let graph = this.graph;
        let uml = shapes.uml;

        this.paper = new dia.Paper({
            el: ReactDOM.findDOMNode(this.refs.placeholder),
            width: 720,
            height: 500,
            model: this.graph,
            gridSize: 1
        });

        var classes = {

            customer: new uml.Class({
                position: { x:300  , y: 50 },
                size: { width: 240, height: 100 },
                name: 'Customer',
                attributes: ['*Self'],
                methods: ['{CustomerID: Integer} -> self', 'CustomerName: String', 'CustomerAddress: String', 'CustomerPostalCode: Integer'],
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
                    '.uml-class-attrs-text': {
                        ref: '.uml-class-attrs-rect',
                        'ref-y': 0.5,
                        'y-alignment': 'middle'
                    },
                    '.uml-class-methods-text': {
                        ref: '.uml-class-methods-rect',
                        'ref-y': 0.5,
                        'y-alignment': 'middle'
                    }
        
                }
            }),
        
            person: new uml.Class({
                position: { x:300  , y: 300 },
                size: { width: 260, height: 100 },
                name: 'Person',
                attributes: ['firstName: String','lastName: String'],
                methods: ['+ setName(first: String, last: String): Void','+ getName(): String'],
                attrs: {
                    '.uml-class-name-rect': {
                        fill: '#68ddd5',
                        stroke: '#ffffff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-attrs-rect': {
                        fill: '#9687fe',
                        stroke: '#fff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-methods-rect': {
                        fill: '#9687fe',
                        stroke: '#fff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-methods-text, .uml-class-attrs-text': {
                        fill: '#fff'
                    }
                }
            }),
        
            bloodgroup: new uml.Class({
                position: { x:20  , y: 190 },
                size: { width: 220, height: 100 },
                name: 'BloodGroup',
                attributes: ['bloodGroup: String'],
                methods: ['+ isCompatible(bG: String): Boolean'],
                attrs: {
                    '.uml-class-name-rect': {
                        fill: '#ff8450',
                        stroke: '#fff',
                        'stroke-width': 0.5,
                    },
                    '.uml-class-attrs-rect': {
                        fill: '#fe976a',
                        stroke: '#fff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-methods-rect': {
                        fill: '#fe976a',
                        stroke: '#fff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-attrs-text': {
                        ref: '.uml-class-attrs-rect',
                        'ref-y': 0.5,
                        'y-alignment': 'middle'
                    },
                    '.uml-class-methods-text': {
                        ref: '.uml-class-methods-rect',
                        'ref-y': 0.5,
                        'y-alignment': 'middle'
                    }
                }
            }),
        
            address: new uml.Class({
                position: { x:630  , y: 190 },
                size: { width: 160, height: 100 },
                name: 'Address',
                attributes: ['houseNumber: Integer','streetName: String','town: String','postcode: String'],
                methods: [],
                attrs: {
                    '.uml-class-name-rect': {
                        fill: '#ff8450',
                        stroke: '#fff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-attrs-rect': {
                        fill: '#fe976a',
                        stroke: '#fff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-methods-rect': {
                        fill: '#fe976a',
                        stroke: '#fff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-attrs-text': {
                        'ref-y': 0.5,
                        'y-alignment': 'middle'
                    }
                }
        
            }),
        
        };
        
        Object.keys(classes).forEach(function(key) {
            graph.addCell(classes[key]);
        });
        
        var relations = [
            new uml.Implementation({ source: { id: classes.person.id }, target: { id: classes.customer.id }}),
            new uml.Aggregation({ source: { id: classes.person.id }, target: { id: classes.address.id }}),
            new uml.Composition({ source: { id: classes.person.id }, target: { id: classes.bloodgroup.id }})
        ];
        
        Object.keys(relations).forEach(function(key) {
            graph.addCell(relations[key]);
        });

        // const rect = new shapes.basic.Rect({
        //     position: { x: 100, y: 30 },
        //     size: { width: 100, height: 30 },
        //     attrs: {
        //         rect: { fill: 'blue' },
        //         text: { text: 'my box', fill: 'white' }
        //     }
        // });

        // const rect2 = rect.clone();
        // rect2.translate(300);

        // const link = new dia.Link({
        //     source: { id: rect.id },
        //     target: { id: rect2.id }
        // });

        // this.graph.addCells([rect, rect2, link]);
    }

    render() {
        return <div ref="placeholder"></div>;
    }
}

export default InputGraph;