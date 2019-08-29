import React from 'react';
import classes from './Header.module.css';

//custom header component to display diagram title

const header = (props) => {
  return (
    <div className={classes.Header}>
      {props.header}
    </div>
  );
}

export default header;
