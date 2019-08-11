import React from 'react';
import Input from './containers/Input/Input';
import ErrorLog from './containers/ErrorLog/ErrorLog';
import Output from './containers/Output/Output';
import './App.css';

// contains all the components to be rendered

const app = (props) => {
  return (
  <div className="App">
      <Input /> {/* renders the input model */}
      <Output /> {/* renders the output model */}
      <ErrorLog /> {/* renders the error log */}
  </div>
  );
}

export default app;
