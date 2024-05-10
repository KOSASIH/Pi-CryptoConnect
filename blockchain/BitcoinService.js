import Bitcoin from 'bitcoinjs-lib';
import { BitcoinConfig } from '../config/BitcoinConfig';

class BitcoinService {
  private network: any;
  private keyPair: any;

  constructor() {
    this.network = Bitcoin.networks[BitcoinConfig.NETWORK];
    this.keyPair = Bitcoin.ECPair.makeRandom({ network: this.network });
  }

  async getAccountBalance(): Promise<number> {
    try {
      const blockchain = new Bitcoin.Blockchain.Blockchain(this.network);
      const address = this.keyPair.getAddress();
      const balance = await blockchain.getBalance(address);
      return balance;
    } catch (error) {
      throw new Error(`Error fetching account balance: ${error.message}`);
    }
  }

  async sendTransaction(toAddress: string, value: number): Promise<string> {
    try {
      const transaction = new Bitcoin.TransactionBuilder(this.network);
      const fromAddress = this.keyPair.getAddress();
      const rawTransaction = transaction
        .addInput(fromAddress, 0)
        .addOutput(toAddress, value)
        .buildIncomplete()
        .sign(this.keyPair);

      const sender = new Bitcoin.Wallet(this.keyPair, { network: this.network });
      const transactionData = sender.broadcast(rawTransaction);
      return transactionData.toString('hex');
    } catch (error) {
      throw new Error(`Error sending transaction: ${error.message}`);
    }
  }
}

export default BitcoinService;
