import axios from 'axios';
import { CryptoConnectModel } from '../models/CryptoConnectModel';
import { CryptoConnectConfig } from '../config/CryptoConnectConfig';

class CryptoConnectAPI {
  constructor() {
    this.api = axios.create({
      baseURL: CryptoConnectConfig.API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async getCryptoData(symbol: string): Promise<CryptoConnectModel> {
    try {
      const response = await this.api.get(`/crypto-data/${symbol}`);
      return response.data;
    } catch (error) {
      throw new Error(`Error fetching crypto data: ${error.message}`);
    }
  }

  async getAllCryptoData(): Promise<CryptoConnectModel[]> {
    try {
      const response = await this.api.get('/crypto-data');
      return response.data;
    } catch (error) {
      throw new Error(`Error fetching all crypto data: ${error.message}`);
    }
  }
}

export default CryptoConnectAPI;
