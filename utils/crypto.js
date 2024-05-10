import { CryptoConnectModel } from '../models/CryptoConnectModel';

export const calculateMarketCap = (price: number, circulatingSupply: number): number => {
  return price * circulatingSupply;
};

export const formatPrice = (price: number): string => {
  return price.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
};

export const getCryptoById = (id: string, cryptos: CryptoConnectModel[]): CryptoConnectModel | undefined => {
  return cryptos.find((crypto) => crypto.id === id);
};
