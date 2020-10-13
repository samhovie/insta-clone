import React from 'react';
import ReactDOM from 'react-dom';
import Feed from './feed';

// This method is only called once
ReactDOM.render(
  <Feed url="/api/v1/p/" />,
  document.getElementById('reactEntry'),
);
