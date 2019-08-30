import React from 'react';
import ReactDOM from 'react-dom';
import { dia }  from 'jointjs';
import RelationGraphModel from './RelationGraphModel';

class ARModel extends React.Component {

    constructor(props) {
        super(props);
        this.graph = new dia.Graph();
    }

    componentDidMount() {
        let graph = this.graph;
    
        this.paper = new dia.Paper({
            el: ReactDOM.findDOMNode(this.refs.placeholder),
            width: 720,
            height: 500,
            model: this.graph,
            gridSize: 1
        });

        let graphModel = new RelationGraphModel(this.props.classes);
        let classes = graphModel.classes;
       
        Object.keys(classes).forEach(function(key) {
            graph.addCell(classes[key]);
            
        });
        
        // var relations = [
        //     new uml.Implementation({ source: { id: classes.person.id }, target: { id: classes.customer.id }})
        // ];
        
        // Object.keys(relations).forEach(function(key) {
        //     graph.addCell(relations[key]);
        // });

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

export default ARModel;