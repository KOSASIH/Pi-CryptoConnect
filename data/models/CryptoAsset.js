// data/models/CryptoAsset.js

import mongoose, { Schema, Document } from 'mongoose';

export interface ICryptoAsset extends Document {
  name: string;
  symbol: string;
  marketCap: number;
  price: number;
  volume: number;
  circulatingSupply: number;
  totalSupply: number;
  updatedAt: Date;
}

const CryptoAssetSchema: Schema = new Schema({
  name: { type: String, required: true },
  symbol: { type: String, required: true },
  marketCap: { type: Number, required: true },
  price: { type: Number, required: true },
  volume: { type: Number, required: true },
  circulatingSupply: { type: Number, required: true },
  totalSupply: { type: Number, required: true },
  updatedAt: { type: Date, default: Date.now },
});

export default mongoose.model<ICryptoAsset>('CryptoAsset', CryptoAssetSchema);
