// src/services/blockchainService.js

import axios from 'axios';

// Base URL for the blockchain API
const BASE_URL = '/api/blockchain'; // Replace with actual API endpoint

// Function to mint new Pi coins
export const mintCoins = async (amount) => {
    try {
        const response = await axios.post(`${BASE_URL}/mint`, { amount });
        return response.data;
    } catch (error) {
        throw new Error('Failed to mint coins: ' + error.message);
    }
};

// Function to transfer Pi coins
export const transferCoins = async (recipientAddress, amount) => {
    try {
        const response = await axios.post(`${BASE_URL}/transfer`, {
            recipient: recipientAddress,
            amount,
        });
        return response.data;
    } catch (error) {
        throw new Error('Failed to transfer coins: ' + error.message);
    }
};

// Function to check the balance of a user
export const checkBalance = async (userId) => {
    try {
        const response = await axios.get(`${BASE_URL}/balance`, {
            params: { userId },
        });
        return response.data.balance;
    } catch (error) {
        throw new Error('Failed to fetch balance: ' + error.message);
    }
};

// Function to fetch transaction history
export const fetchTransactionHistory = async (userId) => {
    try {
        const response = await axios.get(`${BASE_URL}/transactions`, {
            params: { userId },
        });
        return response.data.transactions;
    } catch (error) {
        throw new Error('Failed to fetch transaction history: ' + error.message);
    }
};
