// data/repositories/CryptoAssetRepository.js

import { ICryptoAsset, ICryptoAssetDocument } from '../models/CryptoAsset';
import CryptoAsset, { CryptoAssetModel } from '../models/CryptoAsset';
import { CryptoAssetRepository } from './CryptoAssetRepository';

export class MongooseCryptoAssetRepository implements CryptoAssetRepository {
  async findAll(): Promise<ICryptoAsset[]> {
    const cryptoAssets: ICryptoAssetDocument[] = await CryptoAssetModel.find();
    return cryptoAssets.map((cryptoAsset) => cryptoAsset.toObject());
  }

  async findById(id: string): Promise<ICryptoAsset | null> {
    const cryptoAsset: ICryptoAssetDocument | null = await CryptoAssetModel.findById(id);
    return cryptoAsset ? cryptoAsset.toObject() : null;
  }

  async save(cryptoAsset: ICryptoAsset): Promise<ICryptoAsset> {
    const cryptoAssetDocument: ICryptoAssetDocument = new CryptoAssetModel(cryptoAsset);
    return cryptoAssetDocument.save();
  }

  async update(id: string, cryptoAsset: ICryptoAsset): Promise<ICryptoAsset | null> {
    const updatedCryptoAsset: ICryptoAssetDocument | null = await CryptoAssetModel.findByIdAndUpdate(id, cryptoAsset, { new: true });
    return updatedCryptoAsset ? updatedCryptoAsset.toObject() : null;
  }

  async delete(id: string): Promise<boolean> {
    const deletedCryptoAsset: ICryptoAssetDocument | null = await CryptoAssetModel.findByIdAndDelete(id);
    return deletedCryptoAsset !== null;
  }
}
