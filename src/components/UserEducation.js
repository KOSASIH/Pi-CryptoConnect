// src/components/UserEducation.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './UserEducation.css'; // Importing CSS for styling

const UserEducation = () => {
    const [resources, setResources] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all');

    // Fetch educational resources from an API
    const fetchResources = async () => {
        try {
            const response = await axios.get('/api/education'); // Replace with actual API endpoint
            setResources(response.data);
        } catch (err) {
            setError('Failed to fetch educational resources');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchResources();
    }, []);

    const handleFilterChange = (e) => {
        setFilter(e.target.value);
    };

    const filteredResources = resources.filter((resource) => 
        filter === 'all' || resource.category === filter
    );

    if (loading) return <div>Loading educational resources...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="user-education">
            <h2>User Education Resources</h2>
            <div className="filter">
                <label htmlFor="filter">Filter by category:</label>
                <select id="filter" value={filter} onChange={handleFilterChange}>
                    <option value="all">All</option>
                    <option value="tutorial">Tutorials</option>
                    <option value="articles">Articles</option>
                    <option value="videos">Videos</option>
                </select>
            </div>
            <ul className="resource-list">
                {filteredResources.map((resource) => (
                    <li key={resource.id} className="resource-item">
                        <h3>{resource.title}</h3>
                        <p>{resource.description}</p>
                        <a href={resource.link} target="_blank" rel="noopener noreferrer">Learn More</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default UserEducation;
