import React from 'react';
import classes from './Output.module.css';
import Header from '../Header/Header';
import OutputGraph from './OutputGraph';


const output = () => {


  return (
    //return the model
    <div className={classes.Diagram}>
      <Header header="Output"/>
      <OutputGraph />
    </div>
  );
}

export default output;
