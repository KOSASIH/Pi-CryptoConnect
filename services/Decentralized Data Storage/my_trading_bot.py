// Set the AI-powered trading bot data
const tradingBotData = {
  name: 'My Trading Bot',
  strategy: 'Bollinger Bands',
  assets: ['BTC', 'ETH'],
  timestamp: Date.now(),
};

// Set the AI-powered trading bot value path
const tradingBotValuePath = `${appPath}/trading-bots/${account.address}`;

// Set the AI-powered trading bot value
const tradingBotValue = {
  value: tradingBotData,
  nonce: -1,
};

// Set the AI-powered trading bot value
pinetwork.db.ref(tradingBotValuePath).set(tradingBotValue)
  .then(() => {
    console.log('Trading bot value set successfully');
  })
  .catch((error) => {
    console.error('Error setting trading bot value:', error);
  });

// Set the decentralized data storage value path
const dataStorageValuePath = `${appPath}/data/${account.address}`;

// Set the decentralized data storage value
const dataStorageValue = {
  value: {
    // Add your data here
  },
  nonce: -1,
};

// Set the decentralized data storage value
pinetwork.db.ref(dataStorageValuePath).set(dataStorageValue)
  .then(() => {
    console.log('Data storage value set successfully');
  })
  .catch((error) => {
    console.error('Error setting data storage value:', error);
  });
