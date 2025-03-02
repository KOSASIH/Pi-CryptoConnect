// src/services/tradingService.js

import axios from 'axios';

// Base URL for the trading API
const BASE_URL = '/api/trading'; // Replace with actual API endpoint

// Function to place a buy order
export const placeBuyOrder = async (pair, amount, price) => {
    try {
        const response = await axios.post(`${BASE_URL}/buy`, {
            pair,
            amount,
            price,
        });
        return response.data;
    } catch (error) {
        throw new Error('Failed to place buy order: ' + error.message);
    }
};

// Function to place a sell order
export const placeSellOrder = async (pair, amount, price) => {
    try {
        const response = await axios.post(`${BASE_URL}/sell`, {
            pair,
            amount,
            price,
        });
        return response.data;
    } catch (error) {
        throw new Error('Failed to place sell order: ' + error.message);
    }
};

// Function to fetch market data
export const fetchMarketData = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/marketdata`);
        return response.data;
    } catch (error) {
        throw new Error('Failed to fetch market data: ' + error.message);
    }
};

// Function to retrieve user trading history
export const fetchTradingHistory = async (userId) => {
    try {
        const response = await axios.get(`${BASE_URL}/history`, {
            params: { userId },
        });
        return response.data.history;
    } catch (error) {
        throw new Error('Failed to fetch trading history: ' + error.message);
    }
};
