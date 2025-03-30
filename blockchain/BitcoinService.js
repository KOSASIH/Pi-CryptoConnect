import * as Bitcoin from 'bitcoinjs-lib';
import { BitcoinConfig } from '../config/BitcoinConfig';
import axios from 'axios';

class BitcoinService {
  private network: Bitcoin.Network;
  private keyPair: Bitcoin.ECPairInterface;

  constructor() {
    this.network = Bitcoin.networks[BitcoinConfig.NETWORK];
    this.keyPair = Bitcoin.ECPair.makeRandom({ network: this.network });
  }

  async getAccountBalance(): Promise<number> {
    try {
      const address = this.keyPair.getAddress();
      const response = await axios.get(`https://blockchain.info/q/addressbalance/${address}?confirmations=6`);
      return response.data / 100000000; // Convert satoshis to BTC
    } catch (error) {
      throw new Error(`Error fetching account balance: ${error.message}`);
    }
  }

  async sendTransaction(toAddress: string, value: number): Promise<string> {
    try {
      const fromAddress = this.keyPair.getAddress();
      const unspentOutputs = await this.getUnspentOutputs(fromAddress);
      const transaction = new Bitcoin.TransactionBuilder(this.network);

      let totalInputValue = 0;
      for (const output of unspentOutputs) {
        transaction.addInput(output.txid, output.vout);
        totalInputValue += output.value;
        if (totalInputValue >= value) break; // Stop if we have enough funds
      }

      if (totalInputValue < value) {
        throw new Error('Insufficient funds for transaction.');
      }

      transaction.addOutput(toAddress, value);
      const change = totalInputValue - value - 1000; // Subtract fee (1000 satoshis)
      if (change > 0) {
        transaction.addOutput(fromAddress, change); // Send change back to sender
      }

      const rawTransaction = transaction.buildIncomplete();
      const transactionHex = rawTransaction.toHex();
      const signedTransaction = await this.signTransaction(rawTransaction);
      const transactionHash = await this.broadcastTransaction(signedTransaction);
      return transactionHash;
    } catch (error) {
      throw new Error(`Error sending transaction: ${error.message}`);
    }
  }

  private async getUnspentOutputs(address: string): Promise<any[]> {
    try {
      const response = await axios.get(`https://blockchain.info/unspent?active=${address}`);
      return response.data.unspent_outputs;
    } catch (error) {
      throw new Error(`Error fetching unspent outputs: ${error.message}`);
    }
  }

  private async signTransaction(transaction: Bitcoin.Transaction): Promise<string> {
    const txb = Bitcoin.TransactionBuilder.fromTransaction(transaction, this.network);
    const fromAddress = this.keyPair.getAddress();
    const keyPair = this.keyPair;

    for (let i = 0; i < txb.tx.ins.length; i++) {
      txb.sign(i, keyPair);
    }

    return txb.build().toHex();
  }

  private async broadcastTransaction(transactionHex: string): Promise<string> {
    try {
      const response = await axios.post('https://api.blockcypher.com/v1/btc/main/txs/push', {
        tx: transactionHex,
      });
      return response.data.tx.hash;
    } catch (error) {
      throw new Error(`Error broadcasting transaction: ${error.message}`);
    }
  }
}

export default BitcoinService;
