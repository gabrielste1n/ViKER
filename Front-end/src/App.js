import React from "react";
import ARModel from "./ARModel";
import ERModel from "./ERModel";
import classes from "./App.module.css";
import Files from "react-files";
import RelationModel from './RelationModel';
import RelationAttribute from './RelationAttribute';
import EntityModel from './EntityModel';
import EntityAttribute from './EntityAttribute';
import axios from 'axios';

// contains all the components to be rendered

class App extends React.Component {
  state = {
    inputJSONfile: {}, //file that the user loads
    outputJSONfile: {}, // file that the server sends back after transform button has been pressed
    inputModel: null,   // object for the input JSON
    outputModel: null,  // object for the ouput JSON
    errors: ["SUCCESS: Node 1 created", "SUCCESS: Node 2 created","FAILURE: Nodes cannot be linked" ],
    relations: [],     // stores all the relation objects
    entities: []       // stores all the entity objects
  }

  constructor(){
    super();
    this.postInputModel = this.postInputModel.bind(this);
    this.saveOutput = this.saveOutput.bind(this);
  }

  // parses the JSON data into a javascript object
  parseEntity(type, JSONfile){
    for(let entity in JSONfile.entities){
      let tempEntity = new EntityModel();
      for(let attr in JSONfile.entities[entity]){
        if(attr === 'name'){
          tempEntity.name = JSONfile.entities[entity][attr];
        }
        if(attr === 'attributes'){
          let relAttributes = [];
          for(let attribute in JSONfile.entities[entity][attr]){
          let tempAttribute = new EntityAttribute();
          for(let attributeType in JSONfile.entities[entity][attr][attribute]){
            if(attributeType === 'AttributeName'){
              tempAttribute.attributeName = JSONfile.entities[entity][attr][attribute][attributeType];
            }
            if(attributeType === 'isIdentifier'){
              tempAttribute.isIdentifier = JSONfile.entities[entity][attr][attribute][attributeType];
            }
            if(attributeType === 'isMultiValued'){
              tempAttribute.isMultiValued = JSONfile.entities[entity][attr][attribute][attributeType];
            }
            if(attributeType === 'composedOf'){
              tempAttribute.composedOf = JSONfile.entities[entity][attr][attribute][attributeType];
            }
            }
            relAttributes.push(tempAttribute);
          }
          tempEntity.attributes = relAttributes;
        }
        if(attr === 'isStrong'){
          tempEntity.isStrong = JSONfile.entities[entity][attr];
        }
        if(attr === 'relationships'){
          tempEntity.relationships = JSONfile.entities[entity][attr];
        }
      }
      this.state.entities.push(tempEntity);
    }

    this.renderEntityModel(type);
  }

  // parses the JSON data into a javascript object
  parseRelation(type, JSONfile){
    for(let relation in JSONfile.relations){
      let tempRelation = new RelationModel();
      for(let attr in JSONfile.relations[relation]){
        if(attr === 'name'){
          tempRelation.name = JSONfile.relations[relation][attr];
        }
        if(attr === 'attributes'){
          let relAttributes = [];
          for(let attribute in JSONfile.relations[relation][attr]){
          let tempAttribute = new RelationAttribute();
          for(let attributeType in JSONfile.relations[relation][attr][attribute]){
            if(attributeType === 'AttributeName'){
              tempAttribute.attributeName = JSONfile.relations[relation][attr][attribute][attributeType];
            }
            if(attributeType === 'isConcrete'){
              tempAttribute.isConcrete = JSONfile.relations[relation][attr][attribute][attributeType];
            }
            if(attributeType === 'dataType'){
              tempAttribute.dataType = JSONfile.relations[relation][attr][attribute][attributeType];
            }
            if(attributeType === 'isPathFunctionalDependancy'){
              tempAttribute.isPathFunctionalDependency = JSONfile.relations[relation][attr][attribute][attributeType];
            }
            if(attributeType === 'isFK'){
              tempAttribute.isFK = JSONfile.relations[relation][attr][attribute][attributeType];
            }
            }
            relAttributes.push(tempAttribute);
          }
          tempRelation.attributes = relAttributes;
        }
        if(attr === 'inheritsFrom'){
          tempRelation.inheritsFrom = JSONfile.relations[relation][attr];
        }
        if(attr === 'coveredBy'){
          tempRelation.coveredBy = JSONfile.relations[relation][attr];
        }
        if(attr === 'disjointWith'){
          tempRelation.disjointWith = JSONfile.relations[relation][attr];
        }
      }
      this.state.relations.push(tempRelation);
    }

    this.renderRelationModel(type);
  }

  // render the relational model
  renderRelationModel(type){
     type === 'input' ? this.setState({inputModel: <ARModel classes={this.state.relations} /> }) : this.setState({outputModel: <ARModel classes={this.state.relations} /> });
  }
  
  // render the entity model
  renderEntityModel(type){
    type === 'input' ? this.setState({inputModel: <ERModel classes={this.state.entities} /> }) : this.setState({outputModel: <ERModel classes={this.state.entities} /> });
 }

// send input model json data to server then get output json back
 postInputModel(){

  if(this.state.inputModel !== null){
    console.log('posting');
const url = "http://192.168.0.108:5000/api/transform"; 

axios.post( url, this.state.inputJSONfile).then((response) => {
  console.log(response.data);
  this.setState({ outputJSONfile: response.data });
  this.state.outputJSONfile.entities ? this.parseEntity('output',this.state.outputJSONfile) : this.parseRelation('output',this.state.outputJSONfile); // parse the JSON into the relevant data model

}).catch((e) => 
{
  console.error(e);
}); // set state to serverJSON then parse that
  }else{
    window.alert('No Input Model Has Been Loaded Yet!');
  }

 }

 //download the trandformation report including json structure of model and error log
 saveOutput(){
   if(this.state.outputModel !== null){
    let filename = "transformationReport.json";
    let contentType = "application/json;charset=utf-8;";
    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
      var blob = new Blob([decodeURIComponent(encodeURI(this.state.errors.join()))], { type: contentType });
      navigator.msSaveOrOpenBlob(blob, filename);
    } else {
      var a = document.createElement('a');
      a.download = filename;
      a.href = 'data:' + contentType + ',' + encodeURIComponent(JSON.stringify(this.state.outputJSONfile));
      a.target = '_blank';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
   }else{
window.alert('No Transformation Has Taken Place Yet!');
   }}

 // loads and parses the input JSON file
 loadModel(input){
  this.setState ({
    inputJSONfile: {}, //file that the user loads
    outputJSONfile: {}, // file that the server sends back after transform button has been pressed
    inputModel: null,   // object for the input JSON
    outputModel: null,  // object for the ouput JSON
    errors: ["SUCCESS: Node 1 created", "SUCCESS: Node 2 created","FAILURE: Nodes cannot be linked" ],
    relations: [],     // stores all the relation objects
    entities: []       // stores all the entity objects
  });

  this.fileReader = new FileReader();
  this.fileReader.readAsText(input);
  this.fileReader.onload = event => {
    this.setState({ inputJSONfile: JSON.parse(event.target.result) }, () => {

      this.state.inputJSONfile.entities ? this.parseEntity('input', this.state.inputJSONfile) : this.parseRelation('input', this.state.inputJSONfile); // parse the JSON into the relevant data model
      console.log(this.state.relations.length > 0 ? this.state.relations : this.state.entities);

    });
  };
  console.log('data',this.state.inputJSONfile);
 }

 // where the entire app is rendered
render(){
  
  return (
    <div className={classes.App}>
       <div className={classes.Header}>
      <div className={classes.InputHeader}>Input</div>
      <div className={classes.OutputHeader}>Output</div>
    </div>
      <div className={classes.GraphsWrapper}>

        <div className={classes.InputDiagram}>
          {this.state.inputModel === null ? null : this.state.inputModel} {/* while input type is unknown, render null, then when it is known, render something */}
        </div>                                                                                                    

        <div className={classes.OutputDiagram}>
          {this.state.outputModel === null ? null : this.state.outputModel } {/* while output type is unknown, render null, then when it is known, render something */}
        </div>
      </div>
      {/* error log */}
      <div className={classes.ErrorLog}>
        <div className={classes.TextAreaWrap}>
          <textarea
            className={classes.TextArea}
            value={this.state.errors.join('\n')}
            readOnly
          ></textarea>
        </div>
         {/* button container */}
        <div className={classes.ButtonContainer}>
          <button> {/* button to load model*/}
            <div className={classes.Files}>
          <Files
            className="files-dropzone"
            onChange={(file) => this.loadModel(file[0])}
            onError={err => console.log(err)}
            accepts={[".JSON"]}
            multiple
            maxFileSize={10000000}
            minFileSize={0}
            clickable
          >
            Load Model
          </Files>
        </div>
      </button>
          <button onClick={this.postInputModel}>Transform Model</button> {/* button to transform model*/}
          <button onClick={this.saveOutput}>Save Transformation Report</button>{/* button to save converted model and error log*/}
        </div>
      </div>
    </div>
  );
  }
  
  };

export default App;
