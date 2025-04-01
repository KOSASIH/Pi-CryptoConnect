// utils/api.js

import axios from 'axios';
import NodeCache from 'node-cache';
import { API_BASE_URL, CACHE_TTL, RATE_LIMIT } from './config';
import logger from './logger';

// Initialize cache with a time-to-live (TTL)
const cache = new NodeCache({ stdTTL: CACHE_TTL });

// Rate limiting variables
let requestCount = 0;
let lastRequestTime = Date.now();

const rateLimit = () => {
    const currentTime = Date.now();
    if (currentTime - lastRequestTime < RATE_LIMIT) {
        throw new Error('Rate limit exceeded. Please try again later.');
    }
    lastRequestTime = currentTime;
    requestCount = 0; // Reset count after a successful request
};

const fetchFromCache = async (key) => {
    const cachedData = cache.get(key);
    if (cachedData) {
        logger.log(`Cache hit for key: ${key}`);
        return cachedData;
    }
    return null;
};

const saveToCache = (key, data) => {
    cache.set(key, data);
    logger.log(`Data cached for key: ${key}`);
};

export const fetchCryptoData = async (cryptoId) => {
    const cacheKey = `cryptoData:${cryptoId}`;
    
    // Check cache first
    const cachedData = await fetchFromCache(cacheKey);
    if (cachedData) {
        return cachedData;
    }

    // Rate limiting
    rateLimit();
    requestCount++;

    try {
        const response = await axios.get(`${API_BASE_URL}/coins/${cryptoId}`);
        saveToCache(cacheKey, response.data);
        return response.data;
    } catch (error) {
        logger.error(`Error fetching data for ${cryptoId}: ${error.message}`);
        throw error;
    }
};

export const fetchMarketData = async () => {
    const cacheKey = 'marketData';

    // Check cache first
    const cachedData = await fetchFromCache(cacheKey);
    if (cachedData) {
        return cachedData;
    }

    // Rate limiting
    rateLimit();
    requestCount++;

    try {
        const response = await axios.get(`${API_BASE_URL}/markets`);
        saveToCache(cacheKey, response.data);
        return response.data;
    } catch (error) {
        logger.error(`Error fetching market data: ${error.message}`);
        throw error;
    }
};

export const fetchHistoricalData = async (cryptoId, days) => {
    const cacheKey = `historicalData:${cryptoId}:${days}`;

    // Check cache first
    const cachedData = await fetchFromCache(cacheKey);
    if (cachedData) {
        return cachedData;
    }

    // Rate limiting
    rateLimit();
    requestCount++;

    try {
        const response = await axios.get(`${API_BASE_URL}/coins/${cryptoId}/market_chart`, {
            params: {
                vs_currency: 'usd',
                days: days,
            },
        });
        saveToCache(cacheKey, response.data);
        return response.data;
    } catch (error) {
        logger.error(`Error fetching historical data for ${cryptoId}: ${error.message}`);
        throw error;
    }
};
