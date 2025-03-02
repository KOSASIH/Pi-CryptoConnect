// utils/cryptoUtils.js

import axios from 'axios';

const COINGECKO_API_URL = 'https://api.coingecko.com/api/v3';

/**
 * Formats a price to a specified currency format.
 * @param {number} price - The price to format.
 * @param {string} currency - The currency code (e.g., 'USD').
 * @returns {string} - Formatted price string.
 */
export const formatPrice = (price, currency = 'USD') => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(price);
};

/**
 * Calculates the percentage change between two prices.
 * @param {number} currentPrice - The current price.
 * @param {number} previousPrice - The previous price.
 * @returns {number} - The percentage change.
 */
export const calculatePercentageChange = (currentPrice, previousPrice) => {
    if (previousPrice === 0) return 0;
    return ((currentPrice - previousPrice) / previousPrice) * 100;
};

/**
 * Fetches historical price data for a specific cryptocurrency.
 * @param {string} coinId - The ID of the cryptocurrency (e.g., 'bitcoin').
 * @param {string} currency - The currency to fetch data in (e.g., 'usd').
 * @param {string} days - The number of days of historical data to fetch (e.g., '30').
 * @returns {Promise<Array>} - An array of historical price data.
 */
export const fetchHistoricalData = async (coinId, currency = 'usd', days = '30') => {
    try {
        const response = await axios.get(`${COINGECKO_API_URL}/coins/${coinId}/market_chart`, {
            params: {
                vs_currency: currency,
                days: days,
                interval: 'daily',
            },
        });
        return response.data.prices; // Returns an array of [timestamp, price]
    } catch (error) {
        console.error('Error fetching historical data:', error);
        throw new Error('Failed to fetch historical data');
    }
};

/**
 * Calculates the average price from an array of price data.
 * @param {Array} priceData - An array of price data.
 * @returns {number} - The average price.
 */
export const calculateAveragePrice = (priceData) => {
    const total = priceData.reduce((acc, [timestamp, price]) => acc + price, 0);
    return total / priceData.length;
};

/**
 * Converts a timestamp to a human-readable date format.
 * @param {number} timestamp - The timestamp to convert.
 * @returns {string} - The formatted date string.
 */
export const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
};

/**
 * Fetches the current market data for a specific cryptocurrency.
 * @param {string} coinId - The ID of the cryptocurrency (e.g., 'bitcoin').
 * @returns {Promise<Object>} - The current market data.
 */
export const fetchCurrentMarketData = async (coinId) => {
    try {
        const response = await axios.get(`${COINGECKO_API_URL}/coins/${coinId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching current market data:', error);
        throw new Error('Failed to fetch current market data');
    }
};
