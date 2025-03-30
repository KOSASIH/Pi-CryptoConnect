// tests/environment.test.js

const config = require('../config/environment');

describe('Environment Configuration', () => {
  beforeEach(() => {
    jest.resetModules(); // Clear the module cache before each test
  });

  it('should load default configuration in development', () => {
    process.env.NODE_ENV = 'development';
    process.env.LOG_LEVEL = 'info';
    process.env.ETHEREUM_NETWORK = 'mainnet';
    process.env.ETHEREUM_RPC_URL = 'https://mainnet.infura.io/v3/YOUR_API_KEY';
    process.env.BITCOIN_NETWORK = 'mainnet';
    process.env.BITCOIN_RPC_URL = 'https://mainnet.bitcoin.com/';

    const config = require('../config/environment');

    expect(config.env).toBe('development');
    expect(config.isProduction).toBe(false);
    expect(config.isTest).toBe(false);
    expect(config.logging.level).toBe('info');
    expect(config.ethereum.network).toBe('mainnet');
    expect(config.ethereum.rpcUrl).toBe('https://mainnet.infura.io/v3/YOUR_API_KEY');
    expect(config.bitcoin.network).toBe('mainnet');
    expect(config.bitcoin.rpcUrl).toBe('https://mainnet.bitcoin.com/');
  });

  it('should throw an error if ETHEREUM_PRIVATE_KEY is missing', () => {
    process.env.NODE_ENV = 'development';
    process.env.ETHEREUM_PRIVATE_KEY = ''; // Simulate missing private key

    expect(() => {
      require('../config/environment');
    }).toThrow('ETHEREUM_PRIVATE_KEY is required.');
  });

  it('should throw an error if BITCOIN_PRIVATE_KEY is missing', () => {
    process.env.NODE_ENV = 'development';
    process.env.BITCOIN_PRIVATE_KEY = ''; // Simulate missing private key

    expect(() => {
      require('../config/environment');
    }).toThrow('BITCOIN_PRIVATE_KEY is required.');
  });

  it('should load test configuration', () => {
    process.env.NODE_ENV = 'test';
    process.env.ETHEREUM_PRIVATE_KEY = 'test-ethereum-private-key';
    process.env.BITCOIN_PRIVATE_KEY = 'test-bitcoin-private-key';

    const config = require('../config/environment');

    expect(config.logging.level).toBe('info'); // Default log level in test
    expect(config.ethereum.rpcUrl).toBe('http://localhost:8545');
    expect(config.bitcoin.rpcUrl).toBe('http://localhost:18332');
  });

  it('should load production configuration', () => {
    process.env.NODE_ENV = 'production';
    process.env.ETHEREUM_PRIVATE_KEY = 'prod-ethereum-private-key';
    process.env.BITCOIN_PRIVATE_KEY = 'prod-bitcoin-private-key';

    const config = require('../config/environment');

    expect(config.logging.level).toBe('warn'); // Log level in production
  });
});
