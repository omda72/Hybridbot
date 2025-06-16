export interface TradingBot {
  id: string;
  name: string;
  status: 'active' | 'paused' | 'stopped';
  exchange: string;
  pair: string;
  strategy: string;
  pnl: number;
  pnlPercent: number;
  trades: number;
  winRate: number;
  createdAt: string;
}

export interface Portfolio {
  totalValue: number;
  totalPnl: number;
  totalPnlPercent: number;
  assets: Asset[];
}

export interface Asset {
  symbol: string;
  amount: number;
  value: number;
  change24h: number;
}

export interface Signal {
  id: string;
  source: 'twitter' | 'reddit' | 'lunarcrush' | 'technical';
  symbol: string;
  sentiment: 'bullish' | 'bearish' | 'neutral';
  strength: number;
  content: string;
  timestamp: string;
}

export interface Trade {
  id: string;
  botId: string;
  pair: string;
  side: 'buy' | 'sell';
  amount: number;
  price: number;
  pnl: number;
  timestamp: string;
  status: 'filled' | 'pending' | 'cancelled';
}

export interface PriceData {
  symbol: string;
  price: number;
  change24h: number;
  volume24h: number;
  high24h: number;
  low24h: number;
}