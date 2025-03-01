import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import DAppBuilder from './components/DAppBuilder';
import DAppList from './components/DAppList';
import Login from './components/Login'; // Assuming you have a Login component
import Profile from './components/Profile'; // Assuming you have a Profile component
import './App.css'; // Optional: for global styles

const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Simulate an API call to check authentication status
        const checkAuthStatus = async () => {
            try {
                // Replace with actual API call
                const response = await fetch('/api/auth/status');
                const data = await response.json();
                setIsAuthenticated(data.isAuthenticated);
            } catch (err) {
                setError('Failed to check authentication status');
            } finally {
                setLoading(false);
            }
        };

        checkAuthStatus();
    }, []);

    const handleLogin = () => {
        setIsAuthenticated(true);
        // Additional login logic (e.g., API call)
    };

    const handleLogout = () => {
        setIsAuthenticated(false);
        // Additional logout logic (e.g., API call)
    };

    if (loading) {
        return <div>Loading...</div>; // Loading state
    }

    return (
        <Router>
            <Header isAuthenticated={isAuthenticated} onLogout={handleLogout} />
            {error && <div className="error">{error}</div>} {/* Error handling */}
            <Switch>
                <Route path="/" exact component={DAppBuilder} />
                <Route path="/create" component={DAppBuilder} />
                <Route path="/dapps" component={DAppList} />
                <Route path="/login" render={() => <Login onLogin={handleLogin} />} />
                <Route path="/profile" component={Profile} />
                {/* Add more routes as needed */}
            </Switch>
        </Router>
    );
};

export default App;
