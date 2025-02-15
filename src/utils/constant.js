// Application Constants

// Pi Coin Configuration
const PI_COIN = {
    SYMBOL: "PI",
    VALUE: 314159.00, // Fixed value of Pi Coin in USD
    SUPPLY: 100_000_000_000, // Total supply of Pi Coin
    DYNAMIC_SUPPLY: true, // Enable dynamic supply adjustments based on market conditions
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
    TRANSACTION_FEE: 0.00000001, // Ultra-low transaction fee in USD
    TRANSACTION_FEE_ADJUSTMENT: 0.000000001, // Dynamic adjustment factor for transaction fees
    BLOCK_TIME: 0.005, // Ultra-fast block time in seconds for rapid transactions
    BLOCK_TIME_ADJUSTMENT: 0.0001, // Fine-tuned adjustment factor for block time based on network load
    MINING_DIFFICULTY: 50, // Significantly reduced difficulty for increased mining participation
    MINING_DIFFICULTY_ADJUSTMENT: 0.005, // Fine-tuned adjustment factor for mining difficulty
    MINING_REWARD: 200, // Increased reward for mining a block
    MINING_REWARD_ADJUSTMENT: 1.5, // Dynamic adjustment for mining rewards
    NETWORK_PROTOCOL: "PoS", // Proof of Stake for energy efficiency
    NETWORK_PROTOCOL_VERSION: "5.0.0", // Updated version of the network protocol
    MAX_TRANSACTION_SIZE: 500_000_000, // Increased maximum transaction size in bytes
    DECIMALS: 18, // Number of decimal places for Pi Coin
    GENESIS_BLOCK_TIMESTAMP: "2025-01-01T00:00:00Z", // Timestamp of the genesis block
    GOVERNANCE_MODEL: "Decentralized Autonomous Organization", // Governance model for Pi Coin
    GOVERNANCE_VOTING_PERIOD: 1_209_600, // Voting period in seconds, 2 weeks
    ENCRYPTION_ALGORITHM: "AES-1024-GCM", // Enhanced encryption algorithm for securing transactions
    HASHING_ALGORITHM: "SHA-3-512", // Advanced hashing algorithm for block verification
    SIGNATURE_SCHEME: "EdDSA", // More secure digital signature scheme for transaction signing
    SECURITY_AUDIT_INTERVAL: 600, // Security audit interval in seconds (10 minutes)
    MAX_PEERS: 5_000, // Increased maximum number of peers in the network
    NODE_TIMEOUT: 3, // Reduced timeout for node responses in seconds
    CONNECTION_RETRY_INTERVAL: 0.2, // Reduced retry interval for node connections in seconds
    STAKING_REWARD: 1.0, // Reward for staking Pi Coins
    MINIMUM_STAKE : 10, // Minimum amount required to stake
    STAKING_PERIOD: 172800, // Staking period in seconds, 2 days
    STAKING_REWARD_ADJUSTMENT: 0.005, // Dynamic adjustment for staking rewards
    SMART_CONTRACT_SUPPORT: true, // Enable smart contract functionality
    INTEROPERABILITY: true, // Support for cross-chain transactions
    DECENTRALIZED_IDENTITY: true, // Support for decentralized identity management
    DATA_PRIVACY_FEATURES: true, // Enhanced privacy features for user data
    TRANSACTION_COMPRESSION: true, // Enable transaction data compression for efficiency
    LOAD_BALANCING: true, // Enable load balancing across nodes for improved performance
    NETWORK_MONITORING: true, // Enable real-time network monitoring and analytics
    FUTURE_UPGRADE_PATH: "6.0.0", // Planned future upgrade version
    RESEARCH_AND_DEVELOPMENT_FUND: 0.1, // Percentage of transaction fees allocated for R&D
    DDOS_PROTECTION: true, // Enable DDoS protection mechanisms
    ANOMALY_DETECTION: true, // Enable anomaly detection for suspicious activities
    STABILITY_MONITORING_INTERVAL: 600, // Interval for monitoring stability in seconds
    STABILITY_THRESHOLD: 0.01, // Threshold for acceptable price fluctuation (1%)
    MULTI_SIGNATURE_SUPPORT: true, // Enable multi-signature transactions for enhanced security
    LIQUIDITY_POOL_SUPPORT: true, // Support for liquidity pools to enhance trading
    INFLATION_RATE: 0.002, // Annual inflation rate for new coin issuance
    REWARD_HALVING_INTERVAL: 5000, // Interval for halving mining rewards
    COMMUNITY_FUND: 0.05, // Percentage of transaction fees allocated for community projects
    EMERGENCY_STOP: false, // Flag to enable emergency stop of transactions if needed
    MAX_TRANSACTIONS_PER_BLOCK: 1_000_000, // Increased maximum number of transactions per block
    SECURITY_AUDIT_FREQUENCY: 0.2, // Increased frequency of security audits in days
    ENABLE_SMART_CONTRACTS: true, // Enable smart contracts on the blockchain
    SMART_CONTRACT_VERSION: '10.0.0', // Updated version of the smart contract framework
    MAX_CONTRACT_SIZE: 1_000_000_000, // Increased maximum size of smart contracts in bytes
    INTEROPERABILITY_PROTOCOL: 'IBC', // Inter-Blockchain Communication protocol for cross-chain interactions
    ENABLE_MULTI_SIG: true, // Enable multi-signature transactions for added security
    MULTI_SIG_THRESHOLD: 15, // Increased number of signatures required for multi-sig transactions
    ENABLE_SHARDING: true, // Enable sharding for improved scalability
    SHARDING_FACTOR: 2048, // Increased number of shards in the network
    DYNAMIC_SHARDING: true, // Enable dynamic sharding based on network load
    ENABLE_CACHING: true, // Enable caching for faster transaction processing
    CACHE_EXPIRATION_TIME: 20, // Reduced cache expiration time in seconds (20 seconds)
    MAX_CONCURRENT_CONNECTIONS: 2_000_000, // Maximum number of concurrent connections to the network
    TRANSACTION_CONFIRMATION_TIME: 0.005, // Target transaction confirmation time in seconds
    ENABLE_ANALYTICS: true, // Enable analytics for transaction monitoring and insights
    ANALYTICS_INTERVAL: 30, // Interval for analytics data collection in seconds (30 seconds)
    USER_FRIENDLY_INTERFACE: true, // Enable a user-friendly interface for transactions
    MULTI_LANGUAGE_SUPPORT: true, // Support for multiple languages in the user interface
    GREEN_MINING: true, // Enable eco-friendly mining practices
    CARBON_OFFSET_PROGRAM: true, // Participation in carbon offset programs
    MAX_FUTURE_BLOCKS: 100_000_000, // Maximum number of future blocks to be processed
    FUTURE_BLOCK_TIME: 0.02, // Target future block time in seconds
    ENABLE_FUTURE_UPGRADES: true, // Allow for future upgrades to the protocol and features
};

module.exports = {
    PI_COIN,
};
