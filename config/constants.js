// config/constants.js

export const NETWORKS = {
  ETHEREUM: {
    NAME: 'Ethereum',
    CHAIN_ID: 1,
    RPC_URL: 'https://mainnet.infura.io/v3/YOUR_API_KEY',
  },
  RINKEBY: {
    NAME: 'Rinkeby',
    CHAIN_ID: 4,
    RPC_URL: 'https://rinkeby.infura.io/v3/YOUR_API_KEY',
  },
  BITCOIN: {
    NAME: 'Bitcoin',
    CHAIN_ID: -1, // Bitcoin doesn't have a chain ID
    RPC_URL: 'https://mainnet.bitcoin.com/',
  },
};

export const ERC20_ABI = [
  // ERC20 ABI definition
];

export const ERC721_ABI = [
  // ERC721 ABI definition
];

export const WEB3_PROVIDERS = {
  HTTP: 'HTTP',
  IPC: 'IPC',
  WEBSocket: 'WEBSOCKET',
};

export const LOG_LEVELS = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
};

export const DEFAULT_LOG_LEVEL = LOG_LEVELS.INFO;

export const DEFAULT_WEB3_PROVIDER = WEB3_PROVIDERS.HTTP;

export const DEFAULT_NETWORK = NETWORKS.ETHEREUM;
