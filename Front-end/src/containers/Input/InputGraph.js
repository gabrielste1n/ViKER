import React from 'react';
import ReactDOM from 'react-dom';
import { dia, shapes }  from 'jointjs';

class InputGraph extends React.Component {

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
            gridSize: 1
        });

        const rect = new shapes.basic.Rect({
            position: { x: 100, y: 30 },
            size: { width: 100, height: 30 },
            attrs: {
                rect: { fill: 'blue' },
                text: { text: 'my box', fill: 'white' }
            }
        });

        const rect2 = rect.clone();
        rect2.translate(300);

        const link = new dia.Link({
            source: { id: rect.id },
            target: { id: rect2.id }
        });

        this.graph.addCells([rect, rect2, link]);
    }

    render() {
        return <div ref="placeholder"></div>;
    }
}

export default InputGraph;