// config/environment.js

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
    level: process.env.LOG_LEVEL || config.defaultLogLevel,
  },
  ethereum: {
    network: process.env.ETHEREUM_NETWORK || config.defaultNetwork,
    rpcUrl: process.env.ETHEREUM_RPC_URL || config.defaultEthereumRpcUrl,
    privateKey: process.env.ETHEREUM_PRIVATE_KEY,
  },
  bitcoin: {
    network: process.env.BITCOIN_NETWORK || config.defaultNetwork,
    rpcUrl: process.env.BITCOIN_RPC_URL || config.defaultBitcoinRpcUrl,
    privateKey: process.env.BITCOIN_PRIVATE_KEY,
  },
};

config.defaultLogLevel = LOG_LEVELS.INFO;
config.defaultEthereumRpcUrl = 'https://mainnet.infura.io/v3/YOUR_API_KEY';
config.defaultBitcoinRpcUrl = 'https://mainnet.bitcoin.com/';

if (isTest) {
  config.logging.level = LOG_LEVELS.WARN;
  config.ethereum.rpcUrl = 'http://localhost:8545';
  config.bitcoin.rpcUrl = 'http://localhost:18332';
}

if (isProduction) {
  config.logging.level = LOG_LEVELS.WARN;
}

module.exports = config;
