import Web3 from 'web3';
import { EthereumConfig } from '../config/EthereumConfig';

class EthereumService {
  private web3: Web3;

  constructor() {
    this.web3 = new Web3(EthereumConfig.PROVIDER_URL);
  }

  async getAccountBalance(address: string): Promise<string> {
    try {
      const balance = await this.web3.eth.getBalance(address);
      return this.web3.utils.fromWei(balance, 'ether');
    } catch (error) {
      throw new Error(`Error fetching account balance: ${error.message}`);
    }
  }

  async sendTransaction(fromAddress: string, toAddress: string, value: string): Promise<string> {
    try {
      const gas = await this.web3.eth.estimateGas({ from: fromAddress, to: toAddress, value });
      const transaction = { from: fromAddress, to: toAddress, value, gas };
      const signedTransaction = await this.web3.eth.accounts.signTransaction(transaction, EthereumConfig.PRIVATE_KEY);
      const receipt = await this.web3.eth.sendSignedTransaction(signedTransaction.rawTransaction);
      return receipt.transactionHash;
    } catch (error) {
      throw new Error(`Error sending transaction: ${error.message}`);
    }
  }
}

export default EthereumService;
