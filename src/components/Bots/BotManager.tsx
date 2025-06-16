import React, { useState } from 'react';
import { TradingBot } from '../../types/trading';

interface Props {
  bots: TradingBot[];
  onCreateBot: (bot: Omit<TradingBot, 'id'>) => void;
  onToggleBot: (botId: string) => void;
  onDeleteBot: (botId: string) => void;
}

const BotManager: React.FC<Props> = ({ bots, onCreateBot, onToggleBot, onDeleteBot }) => {
  const [exchange, setExchange] = useState('kucoin'); // inside component
  const [name, setName] = useState('');
  const [strategy, setStrategy] = useState('sentiment');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    onCreateBot({
      name,
      strategy,
      exchange,
      status: 'active',
    });

    setName('');
    setStrategy('sentiment');
    setExchange('kucoin'); // reset after submit
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Manage Your Bots</h2>

      <form onSubmit={handleSubmit} className="space-y-4 bg-gray-800 p-4 rounded-xl">
        <div className="flex flex-col md:flex-row gap-4">
          <input
            className="flex-1 px-4 py-2 rounded-md text-black"
            placeholder="Bot name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <select
            className="px-4 py-2 rounded-md text-black"
            value={strategy}
            onChange={(e) => setStrategy(e.target.value)}
          >
            <option value="sentiment">Sentiment</option>
            <option value="technical">Technical</option>
            <option value="hybrid">Hybrid</option>
          </select>

          <select
            className="px-4 py-2 rounded-md text-black"
            value={exchange}
            onChange={(e) => setExchange(e.target.value)}
          >
            <option value="kucoin">KuCoin</option>
            <option value="binance">Binance</option>
            <option value="coinbase">Coinbase</option>
          </select>

          <button
            type="submit"
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-md"
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
