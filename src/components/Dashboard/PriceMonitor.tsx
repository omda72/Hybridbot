import React from 'react';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';
import { PriceData } from '../../types/trading';

interface PriceMonitorProps {
  prices: PriceData[];
}

export default function PriceMonitor({ prices }: PriceMonitorProps) {
  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700">
      <div className="p-6 border-b border-gray-700">
        <div className="flex items-center space-x-2">
          <Activity className="w-5 h-5 text-blue-500" />
          <h2 className="text-xl font-bold text-white">Live Prices</h2>
        </div>
      </div>
      <div className="divide-y divide-gray-700">
        {prices.map((price) => (
          <div key={price.symbol} className="p-6 hover:bg-gray-750 transition-colors">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
                  <span className="text-xs font-bold text-white">{price.symbol.slice(0, 2)}</span>
                </div>
                <div>
                  <h3 className="font-medium text-white">{price.symbol}</h3>
                  <p className="text-xs text-gray-400">Volume: ${(price.volume24h / 1e9).toFixed(1)}B</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-white">${price.price.toLocaleString()}</p>
                <div className="flex items-center space-x-1">
                  {price.change24h >= 0 ? (
                    <TrendingUp className="w-4 h-4 text-green-500" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-red-500" />
                  )}
                  <span className={`text-sm font-medium ${price.change24h >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                    {price.change24h >= 0 ? '+' : ''}{price.change24h}%
                  </span>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-400">24h High</p>
                <p className="text-white font-medium">${price.high24h.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-gray-400">24h Low</p>
                <p className="text-white font-medium">${price.low24h.toLocaleString()}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}