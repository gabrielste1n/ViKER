import React from 'react';
import classes from './Header.module.css';

const header = (props) => {
  return (
    <div className={classes.Header}>
      {props.header}
    </div>
  );
}

export default header;
