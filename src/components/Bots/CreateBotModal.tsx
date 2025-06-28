import React, { useState, useEffect } from 'react';
import { TradingBot } from '../../types/trading'; // Adjust path if necessary

interface CreateBotModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (bot: Omit<TradingBot, 'id'>) => void;
}

const CreateBotModal: React.FC<CreateBotModalProps> = ({ isOpen, onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    exchange: 'kucoin', // Default to 'kucoin'
    pair: 'BTC/USDT', // Default to a common pair
    strategy: 'sentiment', // Default strategy
    riskLevel: 'medium', // Default risk level
  });

  // Reset form when modal opens/closes
  useEffect(() => {
    if (!isOpen) {
      setFormData({
        name: '',
        exchange: 'kucoin',
        pair: 'BTC/USDT',
        strategy: 'sentiment',
        riskLevel: 'medium',
      });
    }
  }, [isOpen]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const newBot: Omit<TradingBot, 'id'> = {
      name: formData.name,
      status: 'stopped', // Bots are initially 'stopped' from the backend perspective
      exchange: formData.exchange,
      symbol: formData.pair, // Changed 'pair' to 'symbol' to match backend
      strategy: formData.strategy,
      pnl: 0,
      pnlPercent: 0,
      trades: 0,
      winRate: 0,
      createdAt: new Date().toISOString().split('T')[0]
    };

    // UPDATE THIS URL to point to your FastAPI backend's /api/bots endpoint
    // Assuming your FastAPI runs on http://localhost:8000
    fetch("http://localhost:8000/api/bots", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: newBot.name,
        exchange: newBot.exchange,
        symbol: newBot.symbol, // Changed 'pair' to 'symbol'
        strategy: newBot.strategy,
        riskLevel: formData.riskLevel,
        // user: "emaddev" // Optional, can remove or replace with actual user auth later
      }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.text().then(text => { throw new Error(`Failed to save bot to backend: ${text}`); });
        }
        return res.json(); // FastAPI returns JSON
      })
      .then((data) => {
        console.log("✅ Backend says:", data);
        // Assuming your onSubmit prop is used to update the bots list in App.tsx
        // If the backend returns the full bot object with ID, you might pass it directly
        // For now, let's just trigger a re-fetch in App.tsx or rely on WS
        onSubmit(newBot); // Call the prop function to update parent state
        onClose(); // Close the modal on success
      })
      .catch((err) => console.error("❌ Error creating bot:", err));
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-md border border-gray-700">
        <h3 className="text-xl font-bold text-white mb-4">Create New Trading Bot</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-300">Bot Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md bg-gray-700 border-gray-600 text-white shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
              required
            />
          </div>

          <div>
            <label htmlFor="exchange" className="block text-sm font-medium text-gray-300">Exchange</label>
            <select
              id="exchange"
              name="exchange"
              value={formData.exchange}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md bg-gray-700 border-gray-600 text-white shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="kucoin">KuCoin</option>
              <option value="binance">Binance</option>
              <option value="coinbase">Coinbase</option>
              <option value="kraken">Kraken</option> {/* NEW: Add Kraken */}
            </select>
          </div>

          <div>
            <label htmlFor="pair" className="block text-sm font-medium text-gray-300">Trading Pair (e.g., BTC/USDT)</label>
            <input
              type="text"
              id="pair"
              name="pair"
              value={formData.pair}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md bg-gray-700 border-gray-600 text-white shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
              required
            />
          </div>

          <div>
            <label htmlFor="strategy" className="block text-sm font-medium text-gray-300">Strategy</label>
            <select
              id="strategy"
              name="strategy"
              value={formData.strategy}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md bg-gray-700 border-gray-600 text-white shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="sentiment">Sentiment-based</option>
              <option value="technical">Technical Analysis</option>
              <option value="hybrid">Hybrid</option>
            </select>
          </div>

          <div>
            <label htmlFor="riskLevel" className="block text-sm font-medium text-gray-300">Risk Level</label>
            <select
              id="riskLevel"
              name="riskLevel"
              value={formData.riskLevel}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md bg-gray-700 border-gray-600 text-white shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div className="flex justify-end space-x-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-md text-gray-300 bg-gray-600 hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white transition-colors"
            >
              Create Bot
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateBotModal;