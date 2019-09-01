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

    }

    render() {
        return <div ref="placeholder"></div>;
    }
}

export default ARModel;