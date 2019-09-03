import React from 'react';
import ReactDOM from 'react-dom';
import { dia, shapes }  from 'jointjs';
import RelationGraphModel from './RelationGraphModel';

class ARModel extends React.Component {

    constructor(props) {
        super(props);
        this.graph = new dia.Graph();
        this.uml = shapes.uml;
        this.erd = shapes.erd;
    }

    componentDidMount() {
        let graph = this.graph;
        // let uml = this.uml;
        // let erd = this.erd;

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
            
            // console.log('key', key);
            // console.log('classes[key]', classes[key]);

        });

        //find which classes have foreign id's and then class that has same attribute but not foreign id
        let connections = [];

        for(let relation in this.props.classes){
            for(let attr in this.props.classes[relation].attributes){
                if(this.props.classes[relation].attributes[attr].isFK){
                    let foreignKey = this.props.classes[relation].attributes[attr].attributeName;
                    let foreignObject = this.props.classes[relation].name;
                    for(let relatedRel in this.props.classes){
                        for(let relatedAttr in this.props.classes[relatedRel].attributes){
                            if(this.props.classes[relatedRel].attributes[relatedAttr].attributeName === foreignKey && this.props.classes[relatedRel].attributes[relatedAttr].isFK === false){
                                let primaryObject = this.props.classes[relatedRel].name;
                                //currently makes source foreign key - should change
                                // let myLink = new erd.Line({
                                //     markup: [
                                //         '<path class="connection" stroke="black" d="M 0 0 0 0"/>',
                                //         '<path class="connection-wrap" d="M 0 0 0 0"/>',
                                //         '<g class="labels"/>',
                                //         '<g class="marker-vertices"/>'
                                //     ].join(''),
                                //     source: { id: classes[foreignObject].id },
                                //     target: { id: classes[primaryObject].id }
                                // });
                                let link = new shapes.standard.Link({ source: { id: classes[foreignObject].id }, target: { id: classes[primaryObject].id }});
                                link.attr('root/title', 'joint.shapes.standard.Link');
                                connections.push(link);
                        }
                    }
                }
                
            }
        }
    }
        
       
        Object.keys(connections).forEach(function(key) {
            graph.addCell(connections[key]);
        });

    }

    render() {
        return <div ref="placeholder"></div>;
    }
}

export default ARModel;