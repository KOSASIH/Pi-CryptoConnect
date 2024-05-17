const { Client } = require('@pinetwork-js/nodepi');

class PiNetworkService {
  constructor(apiKey, privateKey) {
    this.client = new Client(apiKey, {
      stellar: {
        privateKey: privateKey,
      },
    });

    this.client.stellar.on('ready', () => {
      console.log('Pi Network is ready to be used!');
    });

    this.client.stellar.on('operation', (operation) => {
      console.log('New operation', operation);
    });

    this.client.stellar.on('transaction', (transaction) => {
      console.log('New transaction', transaction);
    });
  }

  async getAccountBalance() {
    const account = await this.client.stellar.accounts.account(this.client.stellar.accounts.myAccountId());
    return account.balances.find(balance => balance.asset_type === 'native').balance;
  }

  async sendPi(amount, destination) {
    const transaction = await this.client.stellar.transactions.buildTransaction({
      source: this.client.stellar.accounts.myAccountId(),
      destination: destination,
      amount: amount,
      assetType: 'native',
    });

    const result = await this.client.stellar.transactions.submitTransaction(transaction);
    return result;
  }
}

module.exports = PiNetworkService;
