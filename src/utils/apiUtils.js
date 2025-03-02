// src/utils/apiUtils.js

import axios from 'axios';

// Function to set the base URL for Axios
export const setBaseURL = (url) => {
    axios.defaults.baseURL = url;
};

// Function to handle API requests
export const apiRequest = async (method, url, data = null, params = null) => {
    try {
        const response = await axios({
            method,
            url,
            data,
            params,
        });
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error; // Rethrow the error after handling
    }
};

// Function to handle API errors
const handleApiError = (error) => {
    if (error.response) {
        // Server responded with a status other than 2xx
        console.error('API Error:', error.response.data);
    } else if (error.request) {
        // Request was made but no response received
        console.error('API Error: No response received', error.request);
    } else {
        // Something happened in setting up the request
        console.error('API Error:', error.message);
    }
};

// Function to set default headers (if needed)
export const setDefaultHeaders = (headers) => {
    Object.keys(headers).forEach((key) => {
        axios.defaults.headers.common[key] = headers[key];
    });
};
