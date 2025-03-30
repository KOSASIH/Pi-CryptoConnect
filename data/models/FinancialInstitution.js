// data/models/FinancialInstitution.ts

import mongoose, { Schema, Document } from 'mongoose';

export interface IFinancialInstitution extends Document {
  name: string;
  legalName: string;
  country: string;
  website: string;
  createdAt: Date;
  updatedAt: Date;
}

// Define the schema with additional features
const FinancialInstitutionSchema: Schema = new Schema(
  {
    name: { type: String, required: true, trim: true },
    legalName: { type: String, required: true, trim: true },
    country: { type: String, required: true, trim: true },
    website: { 
      type: String, 
      required: true, 
      trim: true, 
      validate: {
        validator: function(v: string) {
          return /^(ftp|http|https):\/\/[^ "]+$/.test(v); // Simple URL validation
        },
        message: (props) => `${props.value} is not a valid URL!`
      }
    },
  },
  { timestamps: true } // Automatically manage createdAt and updatedAt
);

// Indexing for performance
FinancialInstitutionSchema.index({ name: 1 });
FinancialInstitutionSchema.index({ country: 1 });

// Static methods for common operations
FinancialInstitutionSchema.statics.findByName = async function (name: string) {
  return this.findOne({ name });
};

FinancialInstitutionSchema.statics.findByCountry = async function (country: string) {
  return this.find({ country });
};

// Pre-save middleware for additional validation or transformation
FinancialInstitutionSchema.pre<IFinancialInstitution>('save', function (next) {
  this.updatedAt = new Date(); // This is now handled by timestamps, but can be kept for clarity
  next();
});

export default mongoose.model<IFinancialInstitution>('FinancialInstitution', FinancialInstitutionSchema);
