// tests/network.test.js

import config from '../config/network';
import fs from 'fs';
import path from 'path';

// Mock the file system and logger
jest.mock('fs');
jest.mock('winston', () => {
  return {
    createLogger: jest.fn(() => ({
      info: jest.fn(),
      error: jest.fn(),
    })),
  };
});

describe('Network Configuration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should load the Pi Network configuration correctly', () => {
    // Mock the environment variable
    process.env.NODE_ENV = 'development';

    // Mock the configuration file
    const mockConfig = {
      ethereum: {
        mainnet: {
          name: 'Ethereum Mainnet',
          chainId: '1',
          rpcUrl: 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID',
        },
        rinkeby: {
          name: 'Rinkeby Testnet',
          chainId: '4',
          rpcUrl: 'https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID',
        },
      },
      bitcoin: {
        mainnet: {
          name: 'Bitcoin Mainnet',
          chainId: '0',
          rpcUrl: 'https://bitcoin.org',
        },
      },
      pi: {
        mainnet: {
          name: 'Pi Network',
          chainId: 'your-pi-network-chain-id',
          rpcUrl: 'your-pi-network-rpc-url',
        },
      },
    };

    // Mock the file system to return the mock config
    fs.existsSync.mockReturnValue(true);
    fs.readFileSync.mockReturnValue(JSON.stringify(mockConfig));

    // Validate the configuration
    expect(config).toHaveProperty('pi.mainnet');
    expect(config.pi.mainnet.name).toBe('Pi Network');
    expect(config.pi.mainnet.chainId).toBe('your-pi-network-chain-id');
    expect(config.pi.mainnet.rpcUrl).toBe('your-pi-network-rpc-url');
  });

  it('should throw an error if the configuration file is missing', () => {
    process.env.NODE_ENV = 'development';
    fs.existsSync.mockReturnValue(false);

    expect(() => {
      require('../config/network');
    }).toThrow('Configuration file not found:');
  });

  it('should throw an error if required fields are missing', () => {
    process.env.NODE_ENV = 'development';

    const mockConfigWithMissingFields = {
      pi: {
        mainnet: {
          name: 'Pi Network',
          chainId: '', // Missing chainId
          rpcUrl: 'your-pi-network-rpc-url',
        },
      },
    };

    fs.existsSync.mockReturnValue(true);
    fs.readFileSync.mockReturnValue(JSON.stringify(mockConfigWithMissingFields));

    expect(() => {
      require('../config/network');
    }).toThrow('Invalid configuration for pi mainnet: Missing required fields.');
  });
});
