import React from 'react';
import { Play, Pause, Square, TrendingUp, TrendingDown } from 'lucide-react';
import { TradingBot } from '../../types/trading';

interface BotStatusProps {
  bots: TradingBot[];
  onToggleBot: (botId: string) => void;
}

export default function BotStatus({ bots, onToggleBot }: BotStatusProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <Play className="w-4 h-4 text-green-500" />;
      case 'paused':
        return <Pause className="w-4 h-4 text-yellow-500" />;
      case 'stopped':
        return <Square className="w-4 h-4 text-red-500" />;
      default:
        return <Square className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-500 bg-green-500/10 border-green-500/20';
      case 'paused':
        return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
      case 'stopped':
        return 'text-red-500 bg-red-500/10 border-red-500/20';
      default:
        return 'text-gray-500 bg-gray-500/10 border-gray-500/20';
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700">
      <div className="p-6 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white">Active Trading Bots</h2>
      </div>
      <div className="divide-y divide-gray-700">
        {bots.map((bot) => (
          <div key={bot.id} className="p-6 hover:bg-gray-750 transition-colors">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                {getStatusIcon(bot.status)}
                <div>
                  <h3 className="font-medium text-white">{bot.name}</h3>
                  <p className="text-sm text-gray-400">{bot.exchange} • {bot.pair}</p>
                </div>
              </div>
              <div className={`px-3 py-1 rounded-full border text-xs font-medium ${getStatusColor(bot.status)}`}>
                {bot.status.toUpperCase()}
              </div>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div>
                <p className="text-xs text-gray-400">P&L</p>
                <div className="flex items-center space-x-1">
                  <span className={`font-medium ${bot.pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                    ${bot.pnl.toLocaleString()}
                  </span>
                  {bot.pnl >= 0 ? (
                    <TrendingUp className="w-3 h-3 text-green-500" />
                  ) : (
                    <TrendingDown className="w-3 h-3 text-red-500" />
                  )}
                </div>
                <span className={`text-xs ${bot.pnlPercent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  {bot.pnlPercent >= 0 ? '+' : ''}{bot.pnlPercent}%
                </span>
              </div>
              
              <div>
                <p className="text-xs text-gray-400">Trades</p>
                <p className="font-medium text-white">{bot.trades}</p>
              </div>
              
              <div>
                <p className="text-xs text-gray-400">Win Rate</p>
                <p className="font-medium text-white">{bot.winRate}%</p>
              </div>
              
              <div>
                <p className="text-xs text-gray-400">Strategy</p>
                <p className="font-medium text-white text-xs">{bot.strategy}</p>
              </div>
            </div>
            
            <button
              onClick={() => onToggleBot(bot.id)}
              className={`w-full py-2 px-4 rounded-lg font-medium transition-colors ${
                bot.status === 'active'
                  ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
                  : 'bg-green-600 hover:bg-green-700 text-white'
              }`}
            >
              {bot.status === 'active' ? 'Pause Bot' : 'Start Bot'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}