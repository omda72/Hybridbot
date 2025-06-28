import React, { useState } from 'react';
import { TradingBot } from '../../types/trading'; // Adjust path if necessary

interface Props {
  bots: TradingBot[];
  onCreateBot: (bot: Omit<TradingBot, 'id' | 'status' | 'pnl' | 'pnlPercent' | 'trades' | 'winRate' | 'createdAt' | 'symbol'> & { symbol: string }) => void;
  onToggleBot: (botId: string) => void;
  onDeleteBot: (botId: string) => void;
}

const BotManager: React.FC<Props> = ({ bots, onCreateBot, onToggleBot, onDeleteBot }) => {
  const [exchange, setExchange] = useState('kucoin'); // Default to 'kucoin'
  const [name, setName] = useState('');
  const [strategy, setStrategy] = useState('sentiment');
  const [symbol, setSymbol] = useState('BTC/USDT'); // NEW: Add state for symbol/pair

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !symbol.trim()) return; // Ensure name and symbol are not empty

    onCreateBot({
      name,
      strategy,
      exchange,
      symbol, // Pass the symbol
    });

    setName('');
    setStrategy('sentiment');
    setExchange('kucoin'); // reset after submit
    setSymbol('BTC/USDT'); // reset symbol
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Manage Your Bots</h2>

      <form onSubmit={handleSubmit} className="space-y-4 bg-gray-800 p-4 rounded-xl">
        <div className="flex flex-col md:flex-row gap-4">
          <input
            className="flex-1 px-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="text"
            placeholder="Bot Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input // NEW: Input for trading symbol
            className="flex-1 px-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="text"
            placeholder="Trading Symbol (e.g., BTC/USDT)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            required
          />
          <select
            className="px-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={strategy}
            onChange={(e) => setStrategy(e.target.value)}
          >
            <option value="sentiment">Sentiment-based</option>
            <option value="technical">Technical Analysis</option>
            <option value="hybrid">Hybrid</option>
          </select>
          <select // NEW: Add Kraken to exchange options
            className="px-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={exchange}
            onChange={(e) => setExchange(e.target.value)}
          >
            <option value="kucoin">KuCoin</option>
            <option value="binance">Binance</option>
            <option value="coinbase">Coinbase</option>
            <option value="kraken">Kraken</option>
          </select>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md transition-colors whitespace-nowrap"
          >
            ➕ Create Bot
          </button>
        </div>
      </form>

      <div className="grid md:grid-cols-2 gap-4">
        {bots.map((bot) => (
          <div
            key={bot.id}
            className="bg-gray-800 p-4 rounded-xl flex justify-between items-center"
          >
            <div>
              <p className="text-lg font-semibold text-white">{bot.name}</p>
              <p className="text-sm text-gray-400 capitalize">Strategy: {bot.strategy}</p>
              <p className="text-sm text-gray-400 capitalize">Symbol: {bot.symbol}</p> {/* Display symbol */}
              <p
                className={`text-sm ${
                  bot.status === 'active' ? 'text-green-400' : 'text-yellow-400'
                }`}
              >
                Status: {bot.status}
              </p>
              <p className="text-sm text-gray-400 capitalize">Exchange: {bot.exchange}</p>
            </div>
            <div className="space-x-2">
              <button
                onClick={() => onToggleBot(bot.id)}
                className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded"
              >
                {bot.status === 'active' ? 'Pause' : 'Resume'}
              </button>
              <button
                onClick={() => onDeleteBot(bot.id)}
                className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BotManager;