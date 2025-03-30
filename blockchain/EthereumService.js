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
      throw new Error(`Error fetching account balance for ${address}: ${error.message}`);
    }
  }

  async sendTransaction(fromAddress: string, toAddress: string, value: string): Promise<string> {
    try {
      const gas = await this.web3.eth.estimateGas({ from: fromAddress, to: toAddress, value: this.web3.utils.toWei(value, 'ether') });
      const transaction = {
        from: fromAddress,
        to: toAddress,
        value: this.web3.utils.toWei(value, 'ether'),
        gas,
      };
      const signedTransaction = await this.web3.eth.accounts.signTransaction(transaction, EthereumConfig.PRIVATE_KEY);
      const receipt = await this.web3.eth.sendSignedTransaction(signedTransaction.rawTransaction);
      await this.waitForTransactionConfirmation(receipt.transactionHash);
      return receipt.transactionHash;
    } catch (error) {
      throw new Error(`Error sending transaction from ${fromAddress} to ${toAddress}: ${error.message}`);
    }
  }

  private async waitForTransactionConfirmation(transactionHash: string, confirmations: number = 1): Promise<void> {
    try {
      const receipt = await this.web3.eth.getTransactionReceipt(transactionHash);
      if (!receipt) {
        throw new Error(`Transaction ${transactionHash} not found.`);
      }
      let currentConfirmations = receipt.confirmations;
      while (currentConfirmations < confirmations) {
        await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for 1 second
        const updatedReceipt = await this.web3.eth.getTransactionReceipt(transactionHash);
        if (updatedReceipt) {
          currentConfirmations = updatedReceipt.confirmations;
        }
      }
      console.log(`Transaction ${transactionHash} confirmed with ${currentConfirmations} confirmations.`);
    } catch (error) {
      throw new Error(`Error waiting for transaction confirmation: ${error.message}`);
    }
  }

  async listenToEvents(contractAddress: string, eventName: string): Promise<void> {
    const contract = new this.web3.eth.Contract(EthereumConfig.CONTRACT_ABI, contractAddress);
    contract.events[eventName]({}, (error, event) => {
      if (error) {
        console.error(`Error listening to event ${eventName}: ${error.message}`);
      } else {
        console.log(`Event ${eventName} received:`, event);
      }
    });
  }
}

export default EthereumService;
