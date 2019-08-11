import React from 'react';
import Input from './containers/Input/Input';
import ErrorLog from './containers/ErrorLog/ErrorLog';
import Output from './containers/Output/Output';
import './App.css';

const app = (props) => {
  return (
  <div className="App">
      <Input />
      <Output />
      <ErrorLog />
  </div>
  );
}

export default app;
