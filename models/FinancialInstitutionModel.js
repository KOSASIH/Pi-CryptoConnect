export class FinancialInstitutionModel {
  constructor(
    public id: string,
    public name: string,
    public type: string,
    public country: string,
    public city: string,
    public address: string,
    public createdAt: Date
  ) {}
}
