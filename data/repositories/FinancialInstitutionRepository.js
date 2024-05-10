// data/repositories/FinancialInstitutionRepository.js

import { IFinancialInstitution, IFinancialInstitutionDocument } from '../models/FinancialInstitution';
import FinancialInstitution, { FinancialInstitutionModel } from '../models/FinancialInstitution';
import { FinancialInstitutionRepository } from './FinancialInstitutionRepository';

export class MongooseFinancialInstitutionRepository implements FinancialInstitutionRepository {
  async findAll(): Promise<IFinancialInstitution[]> {
    const financialInstitutions: IFinancialInstitutionDocument[] = await FinancialInstitutionModel.find();
    return financialInstitutions.map((financialInstitution) => financialInstitution.toObject());
  }

  async findById(id: string): Promise<IFinancialInstitution | null> {
    const financialInstitution: IFinancialInstitutionDocument | null = await FinancialInstitutionModel.findById(id);
    return financialInstitution ? financialInstitution.toObject() : null;
  }

  async save(financialInstitution: IFinancialInstitution): Promise<IFinancialInstitution> {
    const financialInstitutionDocument: IFinancialInstitutionDocument = new FinancialInstitutionModel(financialInstitution);
    return financialInstitutionDocument.save();
  }

  async update(id: string, financialInstitution: IFinancialInstitution): Promise<IFinancialInstitution | null> {
    const updatedFinancialInstitution: IFinancialInstitutionDocument | null = await FinancialInstitutionModel.findByIdAndUpdate(id, financialInstitution, { new: true });
    return updatedFinancialInstitution ? updatedFinancialInstitution.toObject() : null;}

  async delete(id: string): Promise<boolean> {
    const deletedFinancialInstitution: IFinancialInstitutionDocument | null = await FinancialInstitutionModel.findByIdAndDelete(id);
    return deletedFinancialInstitution !== null;
  }
}
