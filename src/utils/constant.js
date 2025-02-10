// Application Constants

// Pi Coin Configuration
const PI_COIN = {
    SYMBOL: "PI",
    VALUE: 314159.00, // Fixed value of Pi Coin in USD
    SUPPLY: 100_000_000_000, // Total supply of Pi Coin
    DYNAMIC_SUPPLY: false, // Disable dynamic supply adjustments for stability
    IS_STABLECOIN: true, // Indicates that Pi Coin is a stablecoin
    STABILITY_MECHANISM: "Collateralized", // Mechanism for maintaining stability
    COLLATERAL_RATIO: 1.5, // Collateralization ratio
    RESERVE_ASSETS: [
        "USD",  // US Dollar
        "BTC",  // Bitcoin
        "ETH",  // Ethereum
        "USDT", // Tether (US Dollar-pegged stablecoin)
        "BNB",  // Binance Coin
        "XRP",  // Ripple
        "LTC",  // Litecoin
        "ADA",  // Cardano
        "SOL",  // Solana
        "DOT",  // Polkadot
        "JPY",  // Japanese Yen
        "EUR",  // Euro
        "GBP",  // British Pound
        "CHF",  // Swiss Franc
        "AUD",  // Australian Dollar
        "GOLD",  // Gold (precious metal)
        "SILVER", // Silver (precious metal)
        "PLATINUM", // Platinum (precious metal)
        "OIL",   // Crude Oil (commodity)
        "NATURAL_GAS", // Natural Gas (commodity)
        "COPPER", // Copper (industrial metal)
        "WHEAT", // Wheat (agricultural commodity)
        "CORN",  // Corn (agricultural commodity)
        "COFFEE", // Coffee (agricultural commodity)
        "SUGAR", // Sugar (agricultural commodity)
        "PALLADIUM", // Palladium (precious metal)
        "REAL_ESTATE", // Real Estate (investment asset)
        "ART",   // Art (alternative investment)
        "NFT",   // Non-Fungible Tokens (digital assets)
    ], // List of assets backing the stablecoin
    TRANSACTION_FEE: 0.005, // Reduced transaction fee in USD
    TRANSACTION_FEE_ADJUSTMENT: 0.0005, // Dynamic adjustment factor for transaction fees
    BLOCK_TIME: 5, // Average block time in seconds
    BLOCK_TIME_ADJUSTMENT: 0.5, // Adjustment factor for block time based on network load
    MINING_DIFFICULTY: 500, // Reduced difficulty for increased mining participation
    MINING_DIFFICULTY_ADJUSTMENT: 0.05, // Adjustment factor for mining difficulty
    MINING_REWARD: 25, // Increased reward for mining a block
    MINING_REWARD_ADJUSTMENT: 1.0, // Dynamic adjustment for mining rewards
    NETWORK_PROTOCOL: "PoS", // Proof of Stake for energy efficiency
    NETWORK_PROTOCOL_VERSION: "2.0.0", // Updated version of the network protocol
    MAX_TRANSACTION_SIZE: 2_000_000, // Increased maximum transaction size in bytes
    DECIMALS: 18, // Number of decimal places for Pi Coin
    GENESIS_BLOCK_TIMESTAMP: "2025-01-01T00:00:00Z", // Timestamp of the genesis block
    GOVERNANCE_MODEL: "Decentralized", // Governance model for Pi Coin
    GOVERNANCE_VOTING_PERIOD: 1_209_600, // Voting period in seconds, 2 weeks
    ENCRYPTION_ALGORITHM: "AES-512", // Enhanced encryption algorithm for securing transactions
    HASHING_ALGORITHM: "SHA-3", // Advanced hashing algorithm for block verification
    SIGNATURE_SCHEME: "EdDSA", // More secure digital signature scheme for transaction signing
    SECURITY_AUDIT_INTERVAL: 43200, // Security audit interval in seconds, 12 hours
    MAX_PEERS: 500, // Increased maximum number of peers in the network
    NODE_TIMEOUT: 15, // Reduced timeout for node responses in seconds
    CONNECTION_RETRY_INTERVAL: 2, // Reduced retry interval for node connections in seconds
    STAKING_REWARD: 0.1, // Reward for staking Pi Coins
    MINIMUM_STAKE: 100, // Minimum amount required to stake
    STAKING_PERIOD: 604800, // Staking period in seconds, 1 week
    STAKING_REWARD_ADJUSTMENT: 0.01, // Dynamic adjustment for staking rewards
    SMART_CONTRACT_SUPPORT: true, // Enable smart contract functionality
    INTEROPERABILITY: true, // Support for cross-chain transactions
    DECENTRALIZED_IDENTITY: true, // Support for decentralized identity management
    DATA_PRIVACY_FEATURES: true, // Enhanced privacy features for user data
    TRANSACTION_COMPRESSION: true, // Enable transaction data compression for efficiency
    LOAD_BALANCING: true, // Enable load balancing across nodes for improved performance
    NETWORK_MONITORING: true, // Enable real-time network monitoring and analytics
    FUTURE_UPGRADE_PATH: "3.0.0", // Planned future upgrade version
    RESEARCH_AND_DEVELOPMENT_FUND: 0.01, // Percentage of transaction fees allocated for R&D
    DDOS_PROTECTION: true, // Enable DDoS protection mechanisms
    ANOMALY_DETECTION: true, // Enable anomaly detection for suspicious activities
    STABILITY_MONITORING_INTERVAL: 3600, // Interval for monitoring stability in seconds
    STABILITY_THRESHOLD: 0.05, // Threshold for acceptable price fluctuation (5%)
};

module.exports = {
    PI_COIN,
};
