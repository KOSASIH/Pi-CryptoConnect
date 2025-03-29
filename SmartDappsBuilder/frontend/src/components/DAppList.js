import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './DAppList.css'; // Importing CSS for styling

const DAppList = () => {
    const [dApps, setDApps] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchDApps = async () => {
            try {
                const response = await axios.get('/api/dapps/all');
                setDApps(response.data);
            } catch (err) {
                setError('Error fetching DApps. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchDApps();
    }, []);

    if (loading) {
        return <div className="loading-message">Loading DApps...</div>;
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <div className="dapp-list">
            <h2>Available DApps</h2>
            {dApps.length === 0 ? (
                <p>No DApps available. Create one now!</p>
            ) : (
                <ul>
                    {dApps.map((dApp) => (
                        <li key={dApp._id} className="dapp-item">
                            <h3>{dApp.name}</h3>
                            <p>{dApp.description}</p>
                            <p className="created-at">Created on: {new Date(dApp.createdAt).toLocaleDateString()}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default DAppList;
