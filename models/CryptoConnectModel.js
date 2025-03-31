export class CryptoConnectModel {
  constructor(
    public id: string,
    public name: string,
    public symbol: string,
    public price: number,
    public marketCap: number,
    public volume: number,
    public circulatingSupply: number,
    public totalSupply: number,
    public updatedAt: Date
  ) {
    this.validate();
  }

  // Validate the properties of the model
  private validate() {
    if (!this.id) throw new Error("ID is required.");
    if (!this.name) throw new Error("Name is required.");
    if (!this.symbol) throw new Error("Symbol is required.");
    if (this.price < 0) throw new Error("Price must be a non-negative number.");
    if (this.marketCap < 0) throw new Error("Market Cap must be a non-negative number.");
    if (this.volume < 0) throw new Error("Volume must be a non-negative number.");
    if (this.circulatingSupply < 0) throw new Error("Circulating Supply must be a non-negative number.");
    if (this.totalSupply < 0) throw new Error("Total Supply must be a non-negative number.");
  }

  // Format price to a string with currency symbol
  public formatPrice(currencySymbol: string = "$"): string {
    return `${currencySymbol}${this.price.toFixed(2)}`;
  }

  // Format market cap to a string with currency symbol
  public formatMarketCap(currencySymbol: string = "$"): string {
    return `${currencySymbol}${this.marketCap.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  }

  // Compare two CryptoConnectModel instances by market cap
  public compareByMarketCap(other: CryptoConnectModel): number {
    return this.marketCap - other.marketCap;
  }

  // Get a summary of the cryptocurrency
  public getSummary(): string {
    return `${this.name} (${this.symbol}): Price: ${this.formatPrice()}, Market Cap: ${this.formatMarketCap()}`;
  }
}

// Example usage
if (require.main === module) {
  const bitcoin = new CryptoConnectModel(
    "1",
    "Bitcoin",
    "BTC",
    45000,
    850000000000,
    30000000000,
    19000000,
    21000000,
    new Date()
  );

  console.log(bitcoin.getSummary());
    }
