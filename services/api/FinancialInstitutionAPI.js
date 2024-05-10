import axios from 'axios';
import { FinancialInstitutionModel } from '../models/FinancialInstitutionModel';
import { FinancialInstitutionConfig } from '../config/FinancialInstitutionConfig';

class FinancialInstitutionAPI {
  constructor() {
    this.api = axios.create({
      baseURL: FinancialInstitutionConfig.API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async getFinancialInstitutionData(id: number): Promise<FinancialInstitutionModel> {
    try {
      const response = await this.api.get(`/financial-institution-data/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Error fetching financial institution data: ${error.message}`);
    }
  }

  async getAllFinancialInstitutionData(): Promise<FinancialInstitutionModel[]> {
    try {
      const response = await this.api.get('/financial-institution-data');
      return response.data;
    } catch (error) {
      throw new Error(`Error fetching all financial institution data: ${error.message}`);
    }
  }
}

export default FinancialInstitutionAPI;
