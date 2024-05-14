# config/constants.py

import json
import os
from enum import Enum
from typing import Dict, List


class Environment(Enum):
    """Environment variables"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Network(Enum):
    """Pi Network environments"""

    MAINNET = "mainnet"
    TESTNET = "testnet"
    DEVNET = "devnet"


class Currency(Enum):
    """Supported currencies"""

    PI = "pi"
    BTC = "btc"
    ETH = "eth"


class Config:
    """Configuration class"""

    def __init__(self, env: Environment):
        self.env = env
        self.load_config()

    def load_config(self):
        """Load configuration from file or environment variables"""
        config_file = os.environ.get("CONFIG_FILE") or "config.json"
        with open(config_file, "r") as f:
            self.config = json.load(f)

        # Override with environment variables
        self.config.update(
            {
                "PI_NETWORK_API_ENDPOINT": os.environ.get("PI_NETWORK_API_ENDPOINT"),
                "WALLET_PRIVATE_KEY": os.environ.get("WALLET_PRIVATE_KEY"),
                "WALLET_PUBLIC_KEY": os.environ.get("WALLET_PUBLIC_KEY"),
            }
        )

    @property
    def pi_network_api_endpoint(self) -> str:
        """Pi Network API endpoint"""
        return self.config.get("PI_NETWORK_API_ENDPOINT")

    @property
    def wallet_private_key(self) -> str:
        """Wallet private key"""
        return self.config.get("WALLET_PRIVATE_KEY")

    @property
    def wallet_public_key(self) -> str:
        """Wallet public key"""
        return self.config.get("WALLET_PUBLIC_KEY")

    @property
    def supported_currencies(self) -> List[Currency]:
        """Supported currencies"""
        return [Currency[c] for c in self.config.get("SUPPORTED_CURRENCIES", [])]

    @property
    def network(self) -> Network:
        """Pi Network environment"""
        return Network[self.config.get("NETWORK", Network.MAINNET.name)]


config = Config(Environment(os.environ.get("ENV", Environment.DEVELOPMENT.name)))
