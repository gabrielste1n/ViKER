import React from "react";
import Header from "./containers/Header/Header";
import ARModel from "./ARModel";
import ERModel from "./ERModel";
import classes from "./App.module.css";
import Files from "react-files";
import RelationModel from './RelationModel';
import RelationAttribute from './RelationAttribute';

// contains all the components to be rendered

class App extends React.Component {
  state = {
    JSONfile: {},
    errors: ["SUCCESS: Node 1 created", "SUCCESS: Node 2 created","FAILURE: Nodes cannot be linked" ],
    relations: [],
    entities: []
  }

  constructor(){
    super();
    this.fileReader = new FileReader();
    this.fileReader.onload = event => {
      this.setState({ JSONfile: JSON.parse(event.target.result) }, () => {

        console.log(this.state.JSONfile.relations[0]);

        let type = this.state.JSONfile.entities ? 'entity' : 'relation';
        
        if(type === 'entity'){
          for(let entity in this.state.JSONfile.entities){
  
            for(let attr in this.state.JSONfile.entities[entity]){
              console.log(attr + ": " + this.state.JSONfile.entities[entity][attr]);
            }
          }
          
        }
        
//////////////////////////////////// start relation type ///////////////////////////////////////

        if(type === 'relation'){

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
              console.log(attr + ": " + this.state.JSONfile.relations[relation][attr]);

            }
            this.state.relations.push(tempRelation);
          }
        }
       
        //////////////////////////////////// end relation type ///////////////////////////////////////

      });
    };
  }
  
render(){

    const errorText =
      "SUCCESS: Node 1 created\nSUCCESS: Node 2 created\nERROR: Nodes cannot be linked";
  
  return (
    <div className={classes.App}>
      <div className={classes.GraphsWrapper}>
        <div className={classes.InputDiagram}>
          <Header header="Input" />
          <ARModel />
        </div>

        <div className={classes.OutputDiagram}>
          <Header header="Output" />
          <ERModel />
        </div>
      </div>

      <div className={classes.ErrorLog}>
        <div className={classes.TextAreaWrap}>
          <textarea
            className={classes.TextArea}
            value={errorText}
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
          <button>Transform Model</button> {/* button to transform model*/}
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
