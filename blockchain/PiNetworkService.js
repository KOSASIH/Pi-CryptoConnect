const { Client } = require('@pinetwork-js/nodepi');
const dotenv = require('dotenv');
const winston = require('winston');

// Load environment variables from .env file
dotenv.config();

// Configure logging
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'piNetworkService.log' })
  ],
});

class PiNetworkService {
  constructor(apiKey, privateKey) {
    this.client = new Client(apiKey, {
      stellar: {
        privateKey: privateKey,
      },
    });

    this.client.stellar.on('ready', () => {
      logger.info('Pi Network is ready to be used!');
    });

    this.client.stellar.on('operation', (operation) => {
      logger.info('New operation', operation);
    });

    this.client.stellar.on('transaction', (transaction) => {
      logger.info('New transaction', transaction);
    });
  }

  async getAccountBalance() {
    try {
      const account = await this.client.stellar.accounts.account(this.client.stellar.accounts.myAccountId());
      const balance = account.balances.find(balance => balance.asset_type === 'native');
      return balance ? balance.balance : 0;
    } catch (error) {
      logger.error('Error fetching account balance:', error);
      throw new Error('Could not fetch account balance');
    }
  }

  async sendPi(amount, destination) {
    try {
      const transaction = await this.client.stellar.transactions.buildTransaction({
        source: this.client.stellar.accounts.myAccountId(),
        destination: destination,
        amount: amount,
        assetType: 'native',
      });

      const result = await this.client.stellar.transactions.submitTransaction(transaction);
      logger.info('Transaction submitted:', result);
      return result;
    } catch (error) {
      logger.error('Error sending Pi:', error);
      throw new Error('Transaction failed');
    }
  }

  async getTransactionHistory() {
    try {
      const transactions = await this.client.stellar.transactions.getTransactions(this.client.stellar.accounts.myAccountId());
      return transactions;
    } catch (error) {
      logger.error('Error fetching transaction history:', error);
      throw new Error('Could not fetch transaction history');
    }
  }
}

module.exports = PiNetworkService;
