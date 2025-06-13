import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { Portfolio } from '../../types/trading';

interface PortfolioOverviewProps {
  portfolio: Portfolio;
}

export default function PortfolioOverview({ portfolio }: PortfolioOverviewProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-gray-300 text-sm font-medium mb-2">Total Portfolio Value</h3>
        <p className="text-2xl font-bold text-white">${portfolio.totalValue.toLocaleString()}</p>
      </div>
      
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-gray-300 text-sm font-medium mb-2">Total P&L</h3>
        <div className="flex items-center space-x-2">
          <p className={`text-2xl font-bold ${portfolio.totalPnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            ${portfolio.totalPnl.toLocaleString()}
          </p>
          {portfolio.totalPnl >= 0 ? (
            <TrendingUp className="w-5 h-5 text-green-500" />
          ) : (
            <TrendingDown className="w-5 h-5 text-red-500" />
          )}
        </div>
        <p className={`text-sm ${portfolio.totalPnlPercent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
          {portfolio.totalPnlPercent >= 0 ? '+' : ''}{portfolio.totalPnlPercent}%
        </p>
      </div>
      
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-gray-300 text-sm font-medium mb-2">Assets</h3>
        <div className="space-y-2">
          {portfolio.assets.slice(0, 2).map((asset) => (
            <div key={asset.symbol} className="flex justify-between items-center">
              <span className="text-white font-medium">{asset.symbol}</span>
              <div className="text-right">
                <p className="text-white">${asset.value.toLocaleString()}</p>
                <p className={`text-xs ${asset.change24h >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  {asset.change24h >= 0 ? '+' : ''}{asset.change24h}%
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}