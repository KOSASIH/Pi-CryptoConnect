// src/components/CommunityEvents.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './CommunityEvents.css'; // Importing CSS for styling

const CommunityEvents = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [rsvpSuccess, setRsvpSuccess] = useState(false);

    // Fetch community events from an API
    const fetchEvents = async () => {
        try {
            const response = await axios.get('/api/events'); // Replace with actual API endpoint
            setEvents(response.data);
        } catch (err) {
            setError('Failed to fetch events');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEvents();
    }, []);

    const handleRSVP = async (eventId) => {
        setLoading(true);
        setError(null);
        setRsvpSuccess(false);

        try {
            const response = await axios.post(`/api/events/rsvp`, { eventId });
            if (response.status === 200) {
                setRsvpSuccess(true);
            }
        } catch (err) {
            setError('Failed to RSVP. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading events...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="community-events">
            <h2>Upcoming Community Events</h2>
            <ul className="event-list">
                {events.map((event) => (
                    <li key={event.id} className="event-item">
                        <h3>{event.title}</h3>
                        <p>{event.description}</p>
                        <p><strong>Date:</strong> {new Date(event.date).toLocaleString()}</p>
                        <p><strong>Location:</strong> {event.location}</p>
                        <button onClick={() => handleRSVP(event.id)}>RSVP</button>
                    </li>
                ))}
            </ul>
            {rsvpSuccess && <div className="success">RSVP successful!</div>}
        </div>
    );
};

export default CommunityEvents;
