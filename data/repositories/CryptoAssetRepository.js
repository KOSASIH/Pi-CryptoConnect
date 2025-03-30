// data/repositories/CryptoAssetRepository.ts

import { ICryptoAsset, ICryptoAssetDocument } from '../models/CryptoAsset';
import CryptoAssetModel from '../models/CryptoAsset';
import { CryptoAssetRepository } from './CryptoAssetRepository';
import { Logger } from '../utils/logger'; // Assume you have a logger utility

export class MongooseCryptoAssetRepository implements CryptoAssetRepository {
  private logger = new Logger('MongooseCryptoAssetRepository');

  async findAll(page: number = 1, limit: number = 10, filter: Partial<ICryptoAsset> = {}): Promise<ICryptoAsset[]> {
    try {
      const cryptoAssets: ICryptoAssetDocument[] = await CryptoAssetModel.find(filter)
        .skip((page - 1) * limit)
        .limit(limit)
        .lean(); // Use lean for better performance
      return cryptoAssets.map((cryptoAsset) => cryptoAsset.toObject());
    } catch (error) {
      this.logger.error('Error fetching all crypto assets:', error);
      throw new Error('Could not fetch crypto assets');
    }
  }

  async findById(id: string): Promise<ICryptoAsset | null> {
    try {
      const cryptoAsset: ICryptoAssetDocument | null = await CryptoAssetModel.findById(id).lean();
      return cryptoAsset ? cryptoAsset.toObject() : null;
    } catch (error) {
      this.logger.error(`Error fetching crypto asset with id ${id}:`, error);
      throw new Error(`Could not fetch crypto asset with id ${id}`);
    }
  }

  async save(cryptoAsset: ICryptoAsset): Promise<ICryptoAsset> {
    try {
      const cryptoAssetDocument: ICryptoAssetDocument = new CryptoAssetModel(cryptoAsset);
      return await cryptoAssetDocument.save();
    } catch (error) {
      this.logger.error('Error saving crypto asset:', error);
      throw new Error('Could not save crypto asset');
    }
  }

  async update(id: string, cryptoAsset: ICryptoAsset): Promise<ICryptoAsset | null> {
    try {
      const updatedCryptoAsset: ICryptoAssetDocument | null = await CryptoAssetModel.findByIdAndUpdate(id, cryptoAsset, { new: true }).lean();
      return updatedCryptoAsset ? updatedCryptoAsset.toObject() : null;
    } catch (error) {
      this.logger.error(`Error updating crypto asset with id ${id}:`, error);
      throw new Error(`Could not update crypto asset with id ${id}`);
    }
  }

  async delete(id: string): Promise<boolean> {
    try {
      const deletedCryptoAsset: ICryptoAssetDocument | null = await CryptoAssetModel.findByIdAndDelete(id);
      return deletedCryptoAsset !== null;
    } catch (error) {
      this.logger.error(`Error deleting crypto asset with id ${id}:`, error);
      throw new Error(`Could not delete crypto asset with id ${id}`);
    }
  }

  async bulkSave(cryptoAssets: ICryptoAsset[]): Promise<ICryptoAsset[]> {
    try {
      const savedAssets = await CryptoAssetModel.insertMany(cryptoAssets);
      return savedAssets.map(asset => asset.toObject());
    } catch (error) {
      this.logger.error('Error bulk saving crypto assets:', error);
      throw new Error('Could not bulk save crypto assets');
    }
  }

  async bulkDelete(ids: string[]): Promise<number> {
    try {
      const result = await CryptoAssetModel.deleteMany({ _id: { $in: ids } });
      return result.deletedCount;
    } catch (error) {
      this.logger.error('Error bulk deleting crypto assets:', error);
      throw new Error('Could not bulk delete crypto assets');
    }
  }
               }
