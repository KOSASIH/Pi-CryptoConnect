// config/network.js

import { NETWORKS } from './constants';
import fs from 'fs';
import path from 'path';
import winston from 'winston';

// Set up logging
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'network.log' })
  ]
});

// Load environment-specific configuration
const loadNetworkConfig = () => {
  const env = process.env.NODE_ENV || 'development';
  const configFilePath = path.join(__dirname, `network.${env}.json`);

  if (!fs.existsSync(configFilePath)) {
    logger.error(`Configuration file not found: ${configFilePath}`);
    throw new Error(`Configuration file not found: ${configFilePath}`);
  }

  const configData = JSON.parse(fs.readFileSync(configFilePath, 'utf-8'));
  logger.info(`Loaded network configuration for ${env} environment.`);
  return configData;
};

// Define the network configuration
const config = {
  ethereum: {
    mainnet: {
      name: NETWORKS.ETHEREUM.NAME,
      chainId: NETWORKS.ETHEREUM.CHAIN_ID,
      rpcUrl: NETWORKS.ETHEREUM.RPC_URL,
      ...loadNetworkConfig().ethereum.mainnet // Load environment-specific settings
    },
    rinkeby: {
      name: NETWORKS.RINKEBY.NAME,
      chainId: NETWORKS.RINKEBY.CHAIN_ID,
      rpcUrl: NETWORKS.RINKEBY.RPC_URL,
      ...loadNetworkConfig().ethereum.rinkeby // Load environment-specific settings
    }
  },
  bitcoin: {
    mainnet: {
      name: NETWORKS.BITCOIN.NAME,
      chainId: NETWORKS.BITCOIN.CHAIN_ID,
      rpcUrl: NETWORKS.BITCOIN.RPC_URL,
      ...loadNetworkConfig().bitcoin.mainnet // Load environment-specific settings
    }
  },
  pi: {
    mainnet: {
      name: 'Pi Network',
      chainId: 'your-pi-network-chain-id', // Replace with actual chain ID
      rpcUrl: 'your-pi-network-rpc-url', // Replace with actual RPC URL
      ...loadNetworkConfig().pi.mainnet // Load environment-specific settings
    }
  }
};

// Validate the network configuration
const validateConfig = (config) => {
  for (const network in config) {
    for (const env in config[network]) {
      const { name, chainId, rpcUrl } = config[network][env];
      if (!name || !chainId || !rpcUrl) {
        logger.error(`Invalid configuration for ${network} ${env}: Missing required fields.`);
        throw new Error(`Invalid configuration for ${network} ${env}: Missing required fields.`);
      }
    }
  }
};

// Validate the loaded configuration
validateConfig(config);

export default config;
