// config/app.config.js

// Application Constants
export const APP_NAME = process.env.APP_NAME || 'Pi-CryptoConnect';
export const APP_VERSION = process.env.APP_VERSION || '1.0.0';
export const API_BASE_URL = process.env.API_BASE_URL || 'https://api.example.com/crypto';

// Crypto Data Configuration
export const CRYPTO_DATA_REFRESH_INTERVAL = parseInt(process.env.CRYPTO_DATA_REFRESH_INTERVAL, 10) || 60000; // 1 minute
export const CRYPTO_DATA_MAX_AGE = parseInt(process.env.CRYPTO_DATA_MAX_AGE, 10) || 300000; // 5 minutes
export const CRYPTO_DATA_CACHE_SIZE = parseInt(process.env.CRYPTO_DATA_CACHE_SIZE, 10) || 100;
export const CRYPTO_DATA_API_KEY = process.env.CRYPTO_DATA_API_KEY || 'your-api-key-here';

// Validate required environment variables
const validateConfig = () => {
  if (!CRYPTO_DATA_API_KEY || CRYPTO_DATA_API_KEY === 'your-api-key-here') {
    throw new Error('CRYPTO_DATA_API_KEY is required and must be set to a valid API key.');
  }
};

// Call the validation function
validateConfig();
