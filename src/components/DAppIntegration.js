// src/components/DAppIntegration.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './DAppIntegration.css'; // Importing CSS for styling

const DAppIntegration = () => {
    const [dApps, setDApps] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch DApps from an API or a local JSON file
    const fetchDApps = async () => {
        try {
            const response = await axios.get('/api/dapps'); // Replace with actual API endpoint
            setDApps(response.data);
        } catch (err) {
            setError('Failed to fetch DApps');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDApps();
    }, []);

    const handleConnect = (dApp) => {
        // Logic to connect to the selected DApp
        console.log(`Connecting to ${dApp.name}`);
        // Implement connection logic here
    };

    if (loading) return <div>Loading DApps...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dapp-integration">
            <h2>Decentralized Applications (DApps)</h2>
            <ul className="dapp-list">
                {dApps.map((dApp) => (
                    <li key={dApp.id} className="dapp-item">
                        <h3>{dApp.name}</h3>
                        <p>{dApp.description}</p>
                        <button onClick={() => handleConnect(dApp)}>Connect</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default DAppIntegration;
