// data/models/FinancialInstitution.js

import mongoose, { Schema, Document } from 'mongoose';

export interface IFinancialInstitution extends Document {
  name: string;
  legalName: string;
  country: string;
  website: string;
  createdAt: Date;
  updatedAt: Date;
}

const FinancialInstitutionSchema: Schema = new Schema({
  name: { type: String, required: true },
  legalName: { type: String, required: true },
  country: { type: String, required: true },
  website: { type: String, required: true },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now },
});

FinancialInstitutionSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  next();
});

export default mongoose.model<IFinancialInstitution>('FinancialInstitution', FinancialInstitutionSchema);
