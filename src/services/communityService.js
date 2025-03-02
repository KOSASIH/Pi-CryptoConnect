// src/services/communityService.js

import axios from 'axios';

// Base URL for the community API
const BASE_URL = '/api/community'; // Replace with actual API endpoint

// Function to create a new community event
export const createEvent = async (eventData) => {
    try {
        const response = await axios.post(`${BASE_URL}/events`, eventData);
        return response.data;
    } catch (error) {
        throw new Error('Failed to create event: ' + error.message);
    }
};

// Function to fetch all community events
export const fetchEvents = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/events`);
        return response.data.events;
    } catch (error) {
        throw new Error('Failed to fetch events: ' + error.message);
    }
};

// Function to RSVP for a community event
export const rsvpForEvent = async (eventId, userId) => {
    try {
        const response = await axios.post(`${BASE_URL}/events/rsvp`, {
            eventId,
            userId,
        });
        return response.data;
    } catch (error) {
        throw new Error('Failed to RSVP for event: ' + error.message);
    }
};

// Function to fetch RSVPs for a specific event
export const fetchEventRSVPs = async (eventId) => {
    try {
        const response = await axios.get(`${BASE_URL}/events/${eventId}/rsvps`);
        return response.data.rsvps;
    } catch (error) {
        throw new Error('Failed to fetch RSVPs for event: ' + error.message);
    }
};
