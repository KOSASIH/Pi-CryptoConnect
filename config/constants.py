import os
import json
import logging
from enum import Enum
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Environment(Enum):
    """Environment variables"""
    DEVELOPMENT = 'development'
    STAGING = 'staging'
    PRODUCTION = 'production'

class Network(Enum):
    """Pi Network environments"""
    MAINNET = 'mainnet'
    TESTNET = 'testnet'
    DEVNET = 'devnet'

class Currency(Enum):
    """Supported currencies"""
    PI = 'pi'
    BTC = 'btc'
    ETH = 'eth'

class PiCoinConfig:
    """Configuration constants for Pi Coin as a stablecoin."""

    # General Constants
    SYMBOL: str = "Pi"  # Symbol for Pi Coin
    VALUE: float = 314159.0  # Fixed value of Pi Coin in USD
    SUPPLY: int = 100_000_000_000  # Total supply of Pi Coin
    DECIMALS: int = 18  # Number of decimal places for Pi Coin
    OFFICIAL_WEBSITE: str = "https://minepi.com"  # Official website for Pi Network
    WHITEPAPER_URL: str = "https://minepi.com/whitepaper"  # Link to the whitepaper

    # Transaction Constants
    TRANSACTION_FEE: float = 0.01  # Transaction fee in USD
    MAX_TRANSACTION_SIZE: int = 1_000_000  # Maximum transaction size in bytes
    MIN_TRANSACTION_AMOUNT: float = 0.01  # Minimum transaction amount in USD

    # Block Constants
    BLOCK_TIME: int = 10  # Average block time in seconds
    GENESIS_BLOCK_TIMESTAMP: str = "2025-01-01T00:00:00Z"  # Timestamp of the genesis block
    MAX_BLOCK_SIZE: int = 2_000_000  # Maximum block size in bytes

class Config:
    """Configuration class"""
    def __init__(self, env: Environment):
        self.env = env
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self):
        """Load configuration from file or environment variables"""
        config_file = os.environ.get('CONFIG_FILE', 'config.json')
        logger.info(f"Loading configuration from {config_file}")

        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
            logger.info("Configuration loaded successfully.")
        except FileNotFoundError:
            logger.error(f"Configuration file {config_file} not found.")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {config_file}: {e}")
            raise

        # Override with environment variables
        self.config.update({
            'PI_NETWORK_API_ENDPOINT': os.environ.get('PI_NETWORK_API_ENDPOINT'),
            'WALLET_PRIVATE_KEY': os.environ.get('WALLET_PRIVATE_KEY'),
            'WALLET_PUBLIC_KEY': os.environ.get('WALLET_PUBLIC_KEY'),
        })

        # Validate required fields
        self.validate_config()

    def validate_config(self):
        """Validate required configuration fields"""
        required_fields = ['PI_NETWORK_API_ENDPOINT', 'WALLET_PRIVATE_KEY', 'WALLET_PUBLIC_KEY']
        for field in required_fields:
            if field not in self.config or not self.config[field]:
                logger.error(f"Missing required configuration field: {field}")
                raise ValueError(f"Missing required configuration field: {field}")

    @property
    def pi_network_api_endpoint(self) -> str:
        """Pi Network API endpoint"""
        return self.config.get('PI_NETWORK_API_ENDPOINT')

    @property
    def wallet_private_key(self) -> str:
        """Wallet private key"""
        return self.config.get('WALLET_PRIVATE_KEY')

    @property
    def wallet_public_key(self) -> str:
        """Wallet public key"""
        return self.config.get('WALLET_PUBLIC_KEY')

    @property
    def supported_currencies(self) -> List[Currency]:
        """Supported currencies"""
        return [Currency[c] for c in self.config.get('SUPPORTED_CURRENCIES', [])]

    @property
    def network(self) -> Network:
        """Pi Network environment"""
        return Network[self.config.get('NETWORK', Network.MAINNET.name)]

# Initialize the configuration
config = Config(Environment(os.environ.get('ENV', Environment.DEVELOPMENT.name)))
