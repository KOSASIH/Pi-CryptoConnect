// src/services/kycService.js

import axios from 'axios';

// Base URL for the KYC API
const BASE_URL = '/api/kyc'; // Replace with actual API endpoint

// Function to submit KYC data
export const submitKYC = async (kycData) => {
    try {
        const response = await axios.post(`${BASE_URL}/submit`, kycData, {
            headers: {
                'Content-Type': 'multipart/form-data', // For file uploads
            },
        });
        return response.data;
    } catch (error) {
        throw new Error('Failed to submit KYC data: ' + error.message);
    }
};

// Function to check KYC status
export const checkKYCStatus = async (userId) => {
    try {
        const response = await axios.get(`${BASE_URL}/status`, {
            params: { userId },
        });
        return response.data.status;
    } catch (error) {
        throw new Error('Failed to fetch KYC status: ' + error.message);
    }
};

// Function to retrieve KYC documents
export const getKYCDocuments = async (userId) => {
    try {
        const response = await axios.get(`${BASE_URL}/documents`, {
            params: { userId },
        });
        return response.data.documents;
    } catch (error) {
        throw new Error('Failed to fetch KYC documents: ' + error.message);
    }
};
