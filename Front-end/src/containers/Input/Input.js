import React from 'react';
import classes from './Input.module.css';
import * as SRD from "storm-react-diagrams";
import Header from '../Header/Header';
require("storm-react-diagrams/dist/style.min.css");


const input = () => {

// 1) setup the diagram engine
const engine = new SRD.DiagramEngine();
engine.installDefaultFactories();

// 2) setup the diagram model
const model = new SRD.DiagramModel();
model.setGridSize(1140);

// 3) create a default node
const node1 = new SRD.DefaultNodeModel("Professor", "rgb(242, 38, 19)");
let port1 = node1.addOutPort("First Name");
node1.setPosition(100, 100);

// 4) create another default node
const node2 = new SRD.DefaultNodeModel("Department", "rgb(255, 203, 5)");
let port2 = node2.addInPort("DepartmentID");
node2.setPosition(400, 100);

// 5) link the ports
let link1 = port1.link(port2);

// 6) add the models to the root graph
model.addAll(node1, node2, link1);

// 7) load model into engine
engine.setDiagramModel(model);


  return (
    // return the model
    <div className={classes.Diagram}>
      <Header header="Input"/>
      <SRD.DiagramWidget diagramEngine={engine} />
    </div>
  );
}

export default input;