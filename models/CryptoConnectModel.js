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
  ) {}
}
