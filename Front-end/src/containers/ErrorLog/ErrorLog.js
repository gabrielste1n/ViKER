import React from 'react';
import classes from './ErrorLog.module.css';

const errorLog = () => {

  const text = "SUCCESS: Node 1 created\nSUCCESS: Node 2 created\nERROR: Nodes cannot be linked";
  return (
    <div className={classes.ErrorLog}>
      <div className={classes.TextAreaWrap}>
      <textarea className={classes.TextArea}>
      {text}
      </textarea>
      </div>
      <div className={classes.ButtonContainer}>
        <button>ER to AR</button>
        <button>AR to ER</button>
        <button>Load Model</button>
        <button>Save Model</button>
        <button>Save Error Log</button>
      </div>
    </div>
  );
}

export default errorLog;
