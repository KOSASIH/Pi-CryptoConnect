// config/environment.js

const LOG_LEVELS = {
  INFO: 'info',
  WARN: 'warn',
  ERROR: 'error',
  DEBUG: 'debug',
};

const ENV = process.env.NODE_ENV || 'development';
const isProduction = ENV === 'production';
const isTest = ENV === 'test';

const config = {
  env: ENV,
  isProduction,
  isTest,
  app: {
    name: 'Pi-CryptoConnect',
    version: '1.0.0',
  },
  logging: {
    level: process.env.LOG_LEVEL || LOG_LEVELS.INFO,
  },
  ethereum: {
    network: process.env.ETHEREUM_NETWORK || 'mainnet',
    rpcUrl: process.env.ETHEREUM_RPC_URL || 'https://mainnet.infura.io/v3/YOUR_API_KEY',
    privateKey: process.env.ETHEREUM_PRIVATE_KEY,
  },
  bitcoin: {
    network: process.env.BITCOIN_NETWORK || 'mainnet',
    rpcUrl: process.env.BITCOIN_RPC_URL || 'https://mainnet.bitcoin.com/',
    privateKey: process.env.BITCOIN_PRIVATE_KEY,
  },
};

// Adjust configurations based on the environment
if (isTest) {
  config.logging.level = LOG_LEVELS.WARN;
  config.ethereum.rpcUrl = 'http://localhost:8545';
  config.bitcoin.rpcUrl = 'http://localhost:18332';
}

if (isProduction) {
  config.logging.level = LOG_LEVELS.WARN;
}

// Validate required environment variables
const validateConfig = () => {
  if (!config.ethereum.privateKey) {
    throw new Error('ETHEREUM_PRIVATE_KEY is required.');
  }
  if (!config.bitcoin.privateKey) {
    throw new Error('BITCOIN_PRIVATE_KEY is required.');
  }
};

// Call the validation function
validateConfig();

module.exports = config;
