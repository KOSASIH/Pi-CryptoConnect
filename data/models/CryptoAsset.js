// data/models/CryptoAsset.ts

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
  createdAt: Date;
}

// Define the schema with additional features
const CryptoAssetSchema: Schema = new Schema(
  {
    name: { type: String, required: true, trim: true },
    symbol: { type: String, required: true, unique: true, uppercase: true, trim: true },
    marketCap: { type: Number, required: true, min: 0 },
    price: { type: Number, required: true, min: 0 },
    volume: { type: Number, required: true, min: 0 },
    circulatingSupply: { type: Number, required: true, min: 0 },
    totalSupply: { type: Number, required: true, min: 0 },
  },
  { timestamps: true } // Automatically manage createdAt and updatedAt
);

// Indexing for performance
CryptoAssetSchema.index({ symbol: 1 });
CryptoAssetSchema.index({ marketCap: -1 }); // Index for sorting by market cap

// Static methods for common operations
CryptoAssetSchema.statics.findBySymbol = async function (symbol: string) {
  return this.findOne({ symbol });
};

CryptoAssetSchema.statics.updatePrice = async function (symbol: string, newPrice: number) {
  return this.findOneAndUpdate(
    { symbol },
    { price: newPrice, updatedAt: new Date() },
    { new: true }
  );
};

// Pre-save middleware for additional validation or transformation
CryptoAssetSchema.pre<ICryptoAsset>('save', function (next) {
  // Example: Ensure price is not greater than market cap
  if (this.price > this.marketCap) {
    return next(new Error('Price cannot be greater than market cap.'));
  }
  next();
});

export default mongoose.model<ICryptoAsset>('CryptoAsset', CryptoAssetSchema);
