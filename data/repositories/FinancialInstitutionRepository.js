// data/repositories/FinancialInstitutionRepository.ts

import { IFinancialInstitution, IFinancialInstitutionDocument } from '../models/FinancialInstitution';
import FinancialInstitutionModel from '../models/FinancialInstitution';
import { FinancialInstitutionRepository } from './FinancialInstitutionRepository';
import { Logger } from '../utils/logger'; // Assume you have a logger utility

export class MongooseFinancialInstitutionRepository implements FinancialInstitutionRepository {
  private logger = new Logger('MongooseFinancialInstitutionRepository');

  async findAll(page: number = 1, limit: number = 10, filter: Partial<IFinancialInstitution> = {}): Promise<IFinancialInstitution[]> {
    try {
      const financialInstitutions: IFinancialInstitutionDocument[] = await FinancialInstitutionModel.find(filter)
        .skip((page - 1) * limit)
        .limit(limit)
        .lean(); // Use lean for better performance
      return financialInstitutions.map((financialInstitution) => financialInstitution.toObject());
    } catch (error) {
      this.logger.error('Error fetching all financial institutions:', error);
      throw new Error('Could not fetch financial institutions');
    }
  }

  async findById(id: string): Promise<IFinancialInstitution | null> {
    try {
      const financialInstitution: IFinancialInstitutionDocument | null = await FinancialInstitutionModel.findById(id).lean();
      return financialInstitution ? financialInstitution.toObject() : null;
    } catch (error) {
      this.logger.error(`Error fetching financial institution with id ${id}:`, error);
      throw new Error(`Could not fetch financial institution with id ${id}`);
    }
  }

  async save(financialInstitution: IFinancialInstitution): Promise<IFinancialInstitution> {
    try {
      const financialInstitutionDocument: IFinancialInstitutionDocument = new FinancialInstitutionModel(financialInstitution);
      return await financialInstitutionDocument.save();
    } catch (error) {
      this.logger.error('Error saving financial institution:', error);
      throw new Error('Could not save financial institution');
    }
  }

  async update(id: string, financialInstitution: IFinancialInstitution): Promise<IFinancialInstitution | null> {
    try {
      const updatedFinancialInstitution: IFinancialInstitutionDocument | null = await FinancialInstitutionModel.findByIdAndUpdate(id, financialInstitution, { new: true }).lean();
      return updatedFinancialInstitution ? updatedFinancialInstitution.toObject() : null;
    } catch (error) {
      this.logger.error(`Error updating financial institution with id ${id}:`, error);
      throw new Error(`Could not update financial institution with id ${id}`);
    }
  }

  async delete(id: string): Promise<boolean> {
    try {
      const deletedFinancialInstitution: IFinancialInstitutionDocument | null = await FinancialInstitutionModel.findByIdAndDelete(id);
      return deletedFinancialInstitution !== null;
    } catch (error) {
      this.logger.error(`Error deleting financial institution with id ${id}:`, error);
      throw new Error(`Could not delete financial institution with id ${id}`);
    }
  }

  async bulkSave(financialInstitutions: IFinancialInstitution[]): Promise<IFinancialInstitution[]> {
    try {
      const savedInstitutions = await FinancialInstitutionModel.insertMany(financialInstitutions);
      return savedInstitutions.map(institution => institution.toObject());
    } catch (error) {
      this.logger.error('Error bulk saving financial institutions:', error);
      throw new Error('Could not bulk save financial institutions');
    }
  }

  async bulkDelete(ids: string[]): Promise<number> {
    try {
      const result = await FinancialInstitutionModel.deleteMany({ _id: { $in: ids } });
      return result.deletedCount;
    } catch (error) {
      this.logger.error('Error bulk deleting financial institutions:', error);
      throw new Error('Could not bulk delete financial institutions');
    }
  }
    }
