import React from 'react';
import Header from './containers/Header/Header';
import Sidebar from './containers/Sidebar/Sidebar';
import ErrorLog from './containers/ErrorLog/ErrorLog';
import Diagram from './containers/Diagram/Diagram';
import './App.css';

const app = (props) => {
  return (
  <div className="App">
      <Header />
      <Sidebar />
      <Diagram />
      <ErrorLog />
  </div>
  );
}

export default app;
