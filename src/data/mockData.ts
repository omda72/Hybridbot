import { TradingBot, Portfolio, Signal, Trade, PriceData } from '../types/trading';

export const mockBots: TradingBot[] = [
  {
    id: '1',
    name: 'BTC Momentum Scalper',
    status: 'active',
    exchange: 'Binance',
    pair: 'BTC/USDT',
    strategy: 'RSI + MACD',
    pnl: 1247.83,
    pnlPercent: 12.4,
    trades: 47,
    winRate: 68.1,
    createdAt: '2024-01-15'
  },
  {
    id: '2',
    name: 'ETH Social Sentiment',
    status: 'active',
    exchange: 'Coinbase',
    pair: 'ETH/USD',
    strategy: 'Sentiment + Volume',
    pnl: -156.23,
    pnlPercent: -2.1,
    trades: 23,
    winRate: 43.5,
    createdAt: '2024-01-20'
  },
  {
    id: '3',
    name: 'SOL Trend Following',
    status: 'paused',
    exchange: 'Kraken',
    pair: 'SOL/USDT',
    strategy: 'EMA Cross + BB',
    pnl: 892.47,
    pnlPercent: 8.9,
    trades: 31,
    winRate: 71.0,
    createdAt: '2024-01-18'
  }
];

export const mockPortfolio: Portfolio = {
  totalValue: 15427.89,
  totalPnl: 1984.07,
  totalPnlPercent: 14.8,
  assets: [
    { symbol: 'BTC', amount: 0.25, value: 10500.00, change24h: 2.3 },
    { symbol: 'ETH', amount: 1.8, value: 3200.50, change24h: -1.2 },
    { symbol: 'SOL', amount: 15.3, value: 1727.39, change24h: 4.7 }
  ]
};

export const mockSignals: Signal[] = [
  {
    id: '1',
    source: 'twitter',
    symbol: 'BTC',
    sentiment: 'bullish',
    strength: 85,
    content: 'Major institutions accumulating BTC, whale activity increasing',
    timestamp: '2024-01-25T10:30:00Z'
  },
  {
    id: '2',
    source: 'lunarcrush',
    symbol: 'ETH',
    sentiment: 'bearish',
    strength: 72,
    content: 'Social volume declining, fear sentiment rising',
    timestamp: '2024-01-25T10:15:00Z'
  },
  {
    id: '3',
    source: 'reddit',
    symbol: 'SOL',
    sentiment: 'bullish',
    strength: 68,
    content: 'Ecosystem growth discussions trending, developer activity up',
    timestamp: '2024-01-25T09:45:00Z'
  },
  {
    id: '4',
    source: 'technical',
    symbol: 'BTC',
    sentiment: 'neutral',
    strength: 55,
    content: 'RSI at 58, consolidating near resistance level',
    timestamp: '2024-01-25T10:45:00Z'
  }
];

export const mockTrades: Trade[] = [
  {
    id: '1',
    botId: '1',
    pair: 'BTC/USDT',
    side: 'buy',
    amount: 0.01,
    price: 42150.00,
    pnl: 84.30,
    timestamp: '2024-01-25T10:20:00Z',
    status: 'filled'
  },
  {
    id: '2',
    botId: '2',
    pair: 'ETH/USD',
    side: 'sell',
    amount: 0.5,
    price: 2450.75,
    pnl: -23.12,
    timestamp: '2024-01-25T09:55:00Z',
    status: 'filled'
  },
  {
    id: '3',
    botId: '1',
    pair: 'BTC/USDT',
    side: 'sell',
    amount: 0.015,
    price: 42300.00,
    pnl: 156.75,
    timestamp: '2024-01-25T09:30:00Z',
    status: 'filled'
  }
];

export const mockPrices: PriceData[] = [
  {
    symbol: 'BTC',
    price: 42234.56,
    change24h: 2.34,
    volume24h: 28500000000,
    high24h: 42850.00,
    low24h: 41200.00
  },
  {
    symbol: 'ETH',
    price: 2456.78,
    change24h: -1.23,
    volume24h: 12300000000,
    high24h: 2520.00,
    low24h: 2420.00
  },
  {
    symbol: 'SOL',
    price: 112.89,
    change24h: 4.67,
    volume24h: 850000000,
    high24h: 115.50,
    low24h: 107.20
  }
];