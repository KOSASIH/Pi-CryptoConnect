import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './App';
import './index.css'; // Optional: for global styles

// Render the App component wrapped in Router for routing capabilities
ReactDOM.render(
    <Router>
        <App />
    </Router>,
    document.getElementById('root')
);
