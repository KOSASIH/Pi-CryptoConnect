import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Profile.css'; // Optional: for styling

const Profile = ({ onLogout }) => {
    const [user, setUser ] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');

    useEffect(() => {
        const fetchUser Data = async () => {
            try {
                // Replace with your actual API endpoint
                const response = await axios.get('/api/user/profile');
                setUser (response.data);
                setUsername(response.data.username);
                setEmail(response.data.email);
            } catch (err) {
                setError('Failed to fetch user data.');
            } finally {
                setLoading(false);
            }
        };

        fetchUser Data();
    }, []);

    const handleUpdate = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.put('/api/user/profile', { username, email });
            if (response.data.success) {
                setUser (response.data.user);
                setError('Profile updated successfully!');
            } else {
                setError('Failed to update profile.');
            }
        } catch (err) {
            setError('An error occurred while updating the profile.');
        }
    };

    if (loading) {
        return <div>Loading...</div>; // Loading state
    }

    return (
        <div className="profile-container">
            <h2>User Profile</h2>
            {error && <div className="error-message">{error}</div>}
            {user ? (
                <form onSubmit={handleUpdate}>
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit">Update Profile</button>
                </form>
            ) : (
                <div>No user data available.</div>
            )}
            <button className="logout-button" onClick={onLogout}>Logout</button>
        </div>
    );
};

export default Profile;
