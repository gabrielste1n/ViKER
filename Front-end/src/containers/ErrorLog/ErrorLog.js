import React from 'react';
import classes from './ErrorLog.module.css';

const errorLog = () => {
// currently hard-coded the errors in the log in order to see the over all design before funcitonality is added
  const errorText = 'SUCCESS: Node 1 created\nSUCCESS: Node 2 created\nERROR: Nodes cannot be linked';
  const fileSelector = document.createElement('input');
  fileSelector.setAttribute('type', 'file');

  let jsonInput = []
  let file = 0;

  const onLoadModelClicked = event => {
    fileSelector.click();
    // readit here, determine if it is reltional or entity
    file  = fileSelector.files;
    if(file.length > 0){
      console.log(file);
    }
    
    //if reltional, each entry in array is going to be a relation object 

    // // if entity, each entry in array is going to be an entity 
    // this.jsonInput = [
    //     {
    //       name: 'Customer',
    //       isStrong: true,
    //       attributes: [{
    //         AttributeName: 'CustomerID',     // make attribute object that has these props
    //         isIdentifier: true,
    //         isMultiValued: false,
    //         composedOf: [
    //         ]
    //     },
    //     {
    //         AttributeName: 'CustomerName',
    //         isIdentifier: false,
    //         isMultiValued: false,
    //         composedOf: [
    //         ]
    //     },
    //     {
    //         AttributeName: 'CustomerAddress',
    //         isIdentifier: false,
    //         isMultiValued: false,
    //         composedOf: [
    //         ]
    //     },
    //     {
    //         AttributeName: 'CustomerPostalCode',
    //         isIdentifier: false,
    //         isMultiValued: false,
    //         composedOf: [
    //         ]
    //     }],
    //     relationships: []
    //     },
    // ]
  }

  return (
    <div className={classes.ErrorLog}>
      <div className={classes.TextAreaWrap}>
      <textarea className={classes.TextArea} value={errorText} readOnly>
      </textarea>
      </div>
      <div className={classes.ButtonContainer}>
        <button onClick={onLoadModelClicked}>Load Model</button> {/* button to load model*/}
        <button>Transform Model</button> {/* button to transform model*/}
        <button>Save Transformation</button> {/* button to save converted model */}
        <button>Save Error Log</button> {/* button to save the output of the error log */}
      </div>
    </div>
  );
}

export default errorLog;
