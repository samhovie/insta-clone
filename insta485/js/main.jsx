import React from 'react';
import ReactDOM from 'react-dom';
import Post from './post';

// This method is only called once
ReactDOM.render(
  <Post postid={1} url="/api/v1/p/1/" />,
  document.getElementById('reactEntry'),
);
