import React from 'react';
import { Twitter, MessageCircle, BarChart3, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { Signal } from '../../types/trading';

interface SignalFeedProps {
  signals: Signal[];
}

export default function SignalFeed({ signals }: SignalFeedProps) {
  const getSourceIcon = (source: string) => {
    switch (source) {
      case 'twitter':
        return <Twitter className="w-4 h-4" />;
      case 'reddit':
        return <MessageCircle className="w-4 h-4" />;
      case 'lunarcrush':
        return <BarChart3 className="w-4 h-4" />;
      case 'technical':
        return <BarChart3 className="w-4 h-4" />;
      default:
        return <BarChart3 className="w-4 h-4" />;
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'bearish':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      case 'neutral':
        return <Minus className="w-4 h-4 text-gray-400" />;
      default:
        return <Minus className="w-4 h-4 text-gray-400" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return 'text-green-500 bg-green-500/10 border-green-500/20';
      case 'bearish':
        return 'text-red-500 bg-red-500/10 border-red-500/20';
      case 'neutral':
        return 'text-gray-400 bg-gray-400/10 border-gray-400/20';
      default:
        return 'text-gray-400 bg-gray-400/10 border-gray-400/20';
    }
  };

  const getSourceColor = (source: string) => {
    switch (source) {
      case 'twitter':
        return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      case 'reddit':
        return 'text-orange-400 bg-orange-400/10 border-orange-400/20';
      case 'lunarcrush':
        return 'text-purple-400 bg-purple-400/10 border-purple-400/20';
      case 'technical':
        return 'text-cyan-400 bg-cyan-400/10 border-cyan-400/20';
      default:
        return 'text-gray-400 bg-gray-400/10 border-gray-400/20';
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700">
      <div className="p-6 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white">Signal Feed</h2>
        <p className="text-sm text-gray-400 mt-1">Real-time signals from social media and technical analysis</p>
      </div>
      <div className="max-h-96 overflow-y-auto">
        <div className="divide-y divide-gray-700">
          {signals.map((signal) => (
            <div key={signal.id} className="p-6 hover:bg-gray-750 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg border ${getSourceColor(signal.source)}`}>
                    {getSourceIcon(signal.source)}
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-white">{signal.symbol}</span>
                      <div className={`flex items-center space-x-1 px-2 py-1 rounded-full border text-xs font-medium ${getSentimentColor(signal.sentiment)}`}>
                        {getSentimentIcon(signal.sentiment)}
                        <span>{signal.sentiment.toUpperCase()}</span>
                      </div>
                    </div>
                    <p className="text-xs text-gray-400 capitalize">{signal.source}</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-1">
                    <div className="w-16 bg-gray-700 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${signal.strength >= 70 ? 'bg-green-500' : signal.strength >= 40 ? 'bg-yellow-500' : 'bg-red-500'}`}
                        style={{ width: `${signal.strength}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-400">{signal.strength}%</span>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(signal.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
              <p className="text-sm text-gray-300">{signal.content}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}