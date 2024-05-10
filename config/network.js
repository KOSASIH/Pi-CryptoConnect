// config/network.js

import { NETWORKS } from './constants';

const config = {
  ethereum: {
    mainnet: {
      name: NETWORKS.ETHEREUM.NAME,
      chainId: NETWORKS.ETHEREUM.CHAIN_ID,
      rpcUrl: NETWORKS.ETHEREUM.RPC_URL,
    },
    rinkeby: {
      name: NETWORKS.RINKEBY.NAME,
      chainId: NETWORKS.RINKEBY.CHAIN_ID,
      rpcUrl: NETWORKS.RINKEBY.RPC_URL,
    },
  },
  bitcoin: {
    mainnet: {
      name: NETWORKS.BITCOIN.NAME,
      chainId: NETWORKS.BITCOIN.CHAIN_ID,
      rpcUrl: NETWORKS.BITCOIN.RPC_URL,
    },
  },
};

module.exports = config;
