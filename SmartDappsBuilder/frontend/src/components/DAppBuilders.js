import React, { useState } from 'react';
import axios from 'axios';
import './DAppBuilder.css'; // Importing CSS for styling

const DAppBuilder = () => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');

        // Basic validation
        if (!name || !description) {
            setError('Please fill in all fields.');
            setLoading(false);
            return;
        }

        try {
            const response = await axios.post('/api/dapps/create', { name, description });
            setSuccess(`DApp "${response.data.name}" created successfully!`);
            setName('');
            setDescription('');
        } catch (err) {
            setError('Error creating DApp. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dapp-builder">
            <h1>Create Your DApp</h1>
            <form onSubmit={handleSubmit} className="dapp-form">
                <div className="form-group">
                    <label htmlFor="dappName">DApp Name:</label>
                    <input
                        type="text"
                        id="dappName"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="dappDescription">DApp Description:</label>
                    <textarea
                        id="dappDescription"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="submit-button" disabled={loading}>
                    {loading ? 'Creating...' : 'Create DApp'}
                </button>
            </form>
            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}
        </div>
    );
};

export default DAppBuilder;
