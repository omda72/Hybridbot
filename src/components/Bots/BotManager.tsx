import React, { useState } from 'react';
import { Plus, Settings, Play, Pause, Trash2 } from 'lucide-react';
import { TradingBot } from '../../types/trading';
import CreateBotModal from './CreateBotModal';

interface BotManagerProps {
  bots: TradingBot[];
  onCreateBot: (bot: Omit<TradingBot, 'id'>) => void;
  onToggleBot: (botId: string) => void;
  onDeleteBot: (botId: string) => void;
}

export default function BotManager({ bots, onCreateBot, onToggleBot, onDeleteBot }: BotManagerProps) {
  const [showCreateModal, setShowCreateModal] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Trading Bots</h1>
          <p className="text-gray-400">Manage your automated trading strategies</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <Plus className="w-5 h-5" />
          <span>Create Bot</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {bots.map((bot) => (
          <div key={bot.id} className="bg-gray-800 rounded-xl border border-gray-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-white">{bot.name}</h3>
              <div className="flex items-center space-x-2">
                <button className="p-1 text-gray-400 hover:text-white">
                  <Settings className="w-4 h-4" />
                </button>
                <button 
                  onClick={() => onDeleteBot(bot.id)}
                  className="p-1 text-gray-400 hover:text-red-400"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="space-y-3 mb-4">
              <div className="flex justify-between">
                <span className="text-gray-400">Exchange</span>
                <span className="text-white">{bot.exchange}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Pair</span>
                <span className="text-white">{bot.pair}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Strategy</span>
                <span className="text-white text-sm">{bot.strategy}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">P&L</span>
                <span className={bot.pnl >= 0 ? 'text-green-500' : 'text-red-500'}>
                  ${bot.pnl.toLocaleString()} ({bot.pnlPercent >= 0 ? '+' : ''}{bot.pnlPercent}%)
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Win Rate</span>
                <span className="text-white">{bot.winRate}%</span>
              </div>
            </div>

            <button
              onClick={() => onToggleBot(bot.id)}
              className={`w-full flex items-center justify-center space-x-2 py-2 px-4 rounded-lg font-medium transition-colors ${
                bot.status === 'active'
                  ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
                  : 'bg-green-600 hover:bg-green-700 text-white'
              }`}
            >
              {bot.status === 'active' ? (
                <>
                  <Pause className="w-4 h-4" />
                  <span>Pause</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4" />
                  <span>Start</span>
                </>
              )}
            </button>
          </div>
        ))}
      </div>

      {showCreateModal && (
        <CreateBotModal
          onClose={() => setShowCreateModal(false)}
          onCreateBot={(bot) => {
            onCreateBot(bot);
            setShowCreateModal(false);
          }}
        />
      )}
    </div>
  );
}