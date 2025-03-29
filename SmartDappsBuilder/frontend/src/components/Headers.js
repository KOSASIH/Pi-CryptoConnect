import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css'; // Importing CSS for styling

const Header = ({ isAuthenticated, onLogout }) => {
    return (
        <header className="header">
            <div className="logo">
                <h1>Smart DApps Builder</h1>
            </div>
            <nav className="nav">
                <ul>
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/create">Create DApp</Link>
                    </li>
                    <li>
                        <Link to="/dapps">DApps List</Link>
                    </li>
                    {isAuthenticated ? (
                        <>
                            <li>
                                <Link to="/profile">Profile</Link>
                            </li>
                            <li>
                                <button onClick={onLogout} className="logout-button">Logout</button>
                            </li>
                        </>
                    ) : (
                        <li>
                            <Link to="/login">Login</Link>
                        </li>
                    )}
                </ul>
            </nav>
        </header>
    );
};

export default Header;
