export class FinancialInstitutionModel {
  constructor(
    public id: string,
    public name: string,
    public type: string,
    public country: string,
    public city: string,
    public address: string,
    public createdAt: Date
  ) {
    this.validate();
  }

  // Validate the properties of the model
  private validate() {
    if (!this.id) throw new Error("ID is required.");
    if (!this.name) throw new Error("Name is required.");
    if (!this.type) throw new Error("Type is required.");
    if (!this.country) throw new Error("Country is required.");
    if (!this.city) throw new Error("City is required.");
    if (!this.address) throw new Error("Address is required.");
  }

  // Format the full address
  public formatAddress(): string {
    return `${this.address}, ${this.city}, ${this.country}`;
  }

  // Get a summary of the financial institution
  public getSummary(): string {
    return `${this.name} (${this.type}) - Located at: ${this.formatAddress()}`;
  }

  // Compare two FinancialInstitutionModel instances by name
  public compareByName(other: FinancialInstitutionModel): number {
    return this.name.localeCompare(other.name);
  }
}

// Example usage
if (require.main === module) {
  const bank = new FinancialInstitutionModel(
    "1",
    "Global Bank",
    "Commercial",
    "USA",
    "New York",
    "123 Finance St",
    new Date()
  );

  console.log(bank.getSummary());
    }
