import React from 'react';
import classes from './ErrorLog.module.css';

const errorLog = () => {
// currently hard-coded the errors in the log in order to see the over all design before funcitonality is added
  const text = "SUCCESS: Node 1 created\nSUCCESS: Node 2 created\nERROR: Nodes cannot be linked";
  return (
    <div className={classes.ErrorLog}>
      <div className={classes.TextAreaWrap}>
      <textarea className={classes.TextArea}>
      {text}
      </textarea>
      </div>
      <div className={classes.ButtonContainer}>
        <button>Load Model</button> {/* button to load model*/}
        <button>Transform Model</button> {/* button to transform model*/}
        <button>Save Transformation</button> {/* button to save converted model */}
        <button>Save Error Log</button> {/* button to save the output of the error log */}
      </div>
    </div>
  );
}

export default errorLog;
