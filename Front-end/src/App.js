import React from "react";
import Header from "./containers/Header/Header";
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
    JSONfile: {},
    inputModel: null,
    outputModel: null,
    errors: ["SUCCESS: Node 1 created", "SUCCESS: Node 2 created","FAILURE: Nodes cannot be linked" ],
    relations: [],
    entities: []
  }

  constructor(){
    super();
    this.fileReader = new FileReader();
    this.fileReader.onload = event => {
      this.setState({ JSONfile: JSON.parse(event.target.result) }, () => {

        this.state.JSONfile.entities ? this.parseEntity('input') : this.parseRelation('input'); // parse the JSON into the relevant data model
        console.log(this.state.relations.length > 0 ? this.state.relations : this.state.entities);

      });
    };
  }

  parseEntity(type){
    this.setState({inputType: 'entity'});
    for(let entity in this.state.JSONfile.entities){
      let tempEntity = new EntityModel();
      for(let attr in this.state.JSONfile.entities[entity]){
        if(attr === 'name'){
          tempEntity.name = this.state.JSONfile.entities[entity][attr];
        }
        if(attr === 'attributes'){
          let relAttributes = [];
          for(let attribute in this.state.JSONfile.entities[entity][attr]){
          let tempAttribute = new EntityAttribute();
          for(let attributeType in this.state.JSONfile.entities[entity][attr][attribute]){
            if(attributeType === 'AttributeName'){
              tempAttribute.attributeName = this.state.JSONfile.entities[entity][attr][attribute][attributeType];
            }
            if(attributeType === 'isIdentifier'){
              tempAttribute.isIdentifier = this.state.JSONfile.entities[entity][attr][attribute][attributeType];
            }
            if(attributeType === 'isMultiValued'){
              tempAttribute.isMultiValued = this.state.JSONfile.entities[entity][attr][attribute][attributeType];
            }
            if(attributeType === 'composedOf'){
              tempAttribute.composedOf = this.state.JSONfile.entities[entity][attr][attribute][attributeType];
            }
            }
            relAttributes.push(tempAttribute);
          }
          tempEntity.attributes = relAttributes;
        }
        if(attr === 'isStrong'){
          tempEntity.isStrong = this.state.JSONfile.entities[entity][attr];
        }
        if(attr === 'relationships'){
          tempEntity.relationships = this.state.JSONfile.entities[entity][attr];
        }
      }
      this.state.entities.push(tempEntity);
    }

    this.renderEntityModel(type);
  }

  parseRelation(type){
    this.setState({inputType: 'relation'});
    for(let relation in this.state.JSONfile.relations){
      let tempRelation = new RelationModel();
      for(let attr in this.state.JSONfile.relations[relation]){
        if(attr === 'name'){
          tempRelation.name = this.state.JSONfile.relations[relation][attr];
        }
        if(attr === 'attributes'){
          let relAttributes = [];
          for(let attribute in this.state.JSONfile.relations[relation][attr]){
          let tempAttribute = new RelationAttribute();
          for(let attributeType in this.state.JSONfile.relations[relation][attr][attribute]){
            if(attributeType === 'AttributeName'){
              tempAttribute.attributeName = this.state.JSONfile.relations[relation][attr][attribute][attributeType];
            }
            if(attributeType === 'isConcrete'){
              tempAttribute.isConcrete = this.state.JSONfile.relations[relation][attr][attribute][attributeType];
            }
            if(attributeType === 'dataType'){
              tempAttribute.dataType = this.state.JSONfile.relations[relation][attr][attribute][attributeType];
            }
            if(attributeType === 'isPathFunctionalDependency'){
              tempAttribute.isPathFunctionalDependency = this.state.JSONfile.relations[relation][attr][attribute][attributeType];
            }
            if(attributeType === 'isFK'){
              tempAttribute.isFK = this.state.JSONfile.relations[relation][attr][attribute][attributeType];
            }
            }
            relAttributes.push(tempAttribute);
          }
          tempRelation.attributes = relAttributes;
        }
        if(attr === 'inheritsFrom'){
          tempRelation.inheritsFrom = this.state.JSONfile.relations[relation][attr];
        }
        if(attr === 'coveredBy'){
          tempRelation.coveredBy = this.state.JSONfile.relations[relation][attr];
        }
        if(attr === 'disjointWith'){
          tempRelation.disjointWith = this.state.JSONfile.relations[relation][attr];
        }
      }
      this.state.relations.push(tempRelation);
    }

    this.renderRelationModel(type);

  }

  renderRelationModel(type){
     type === 'input' ? this.setState({inputModel: <ARModel classes={this.state.relations} /> }) : this.setState({outputModel: <ARModel classes={this.state.relations} /> });
  }
  
  renderEntityModel(type){
    type === 'input' ? this.setState({inputModel: <ERModel classes={this.state.relations} /> }) : this.setState({outputModel: <ERModel classes={this.state.relations} /> });
 }

// send input model json data to server then get output json back
 postInputModel(){
  const inputData = {
    inputModel: this.state.JSONfile
}
axios.post('http://localhost:3000/api/transform', inputData)
.then(res => console.log(res.data));
 }

render(){
  
  return (
    <div className={classes.App}>
      <div className={classes.GraphsWrapper}>
        <div className={classes.InputDiagram}>
          <Header header="Input" />
          {this.state.inputModel === null ? null : this.state.inputModel} {/* while input type is unknown, render null, then when it is known, render something */}
        </div>                                                                                                    

        <div className={classes.OutputDiagram}>
          <Header header="Output" />
          {this.state.outputModel === null ? null : this.state.outputModel } {/* while output type is unknown, render null, then when it is known, render something */}
        </div>
      </div>

      <div className={classes.ErrorLog}>
        <div className={classes.TextAreaWrap}>
          <textarea
            className={classes.TextArea}
            value={this.state.errors.join('\n')}
            readOnly
          ></textarea>
        </div>
        <div className={classes.ButtonContainer}>
          <button>
          <div className="files">
        <Files
          className="files-dropzone"
          onChange={file => {
            this.fileReader.readAsText(file[0]);
          }}
          onError={err => console.log(err)}
          accepts={[".JSON"]}
          multiple
          maxFiles={3}
          maxFileSize={10000000}
          minFileSize={0}
          clickable
        >
          Load Model
        </Files>
      </div></button>
          {/* button to load model*/}
          <button onClick={this.postInputModel}>Transform Model</button> {/* button to transform model*/}
          <button>Save Transformation</button>{" "}
          {/* button to save converted model */}
          <button>Save Error Log</button>{" "}
          {/* button to save the output of the error log */}
        </div>
      </div>
    </div>
  );
  }
  
  };

export default App;
