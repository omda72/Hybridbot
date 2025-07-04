import React from 'react';
import { TradingBot } from '../../types/trading';

interface Props {
  bots: TradingBot[];
  onCreateBot: (bot: any) => void;
  onToggleBot: (botId: string) => void;
  onDeleteBot: (botId: string) => void;
}

export default function SimpleBotManager({ bots, onCreateBot, onToggleBot, onDeleteBot }: Props) {
  return (
    <div className="space-y-6">
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Trading Bots</h2>
        
        {bots.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-400">No trading bots found. Create your first bot to get started.</p>
            <button
              onClick={() => onCreateBot({ name: 'Test Bot', strategy: 'DCA', exchange: 'binance', pair: 'BTC/USDT' })}
              className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              Create Test Bot
            </button>
          </div>
        ) : (
          <div className="grid gap-4">
            {bots.map((bot) => (
              <div key={bot.id} className="bg-gray-800 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-white font-medium">{bot.name}</h3>
                    <p className="text-gray-400 text-sm">{bot.strategy} • {bot.exchange}</p>
                    <p className="text-gray-400 text-sm">Pair: {bot.pair}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      bot.status === 'active' ? 'bg-green-600 text-green-100' :
                      bot.status === 'paused' ? 'bg-yellow-600 text-yellow-100' :
                      'bg-red-600 text-red-100'
                    }`}>
                      {bot.status}
                    </span>
                    <button
                      onClick={() => onToggleBot(bot.id)}
                      className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm transition-colors"
                    >
                      {bot.status === 'active' ? 'Pause' : 'Start'}
                    </button>
                    <button
                      onClick={() => onDeleteBot(bot.id)}
                      className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-sm transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}