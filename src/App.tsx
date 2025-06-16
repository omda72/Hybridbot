import React, { useEffect, useState, useRef } from 'react';
import Header from './components/Layout/Header';
import PortfolioOverview from './components/Dashboard/PortfolioOverview';
import BotStatus from './components/Dashboard/BotStatus';
import PriceMonitor from './components/Dashboard/PriceMonitor';
import SignalFeed from './components/Signals/SignalFeed';
import BotManager from './components/Bots/BotManager';
import TradeHistory from './components/Trading/TradeHistory';
import SettingsPanel from './components/Settings/SettingsPanel';
import { TradingBot, Portfolio, Signal, Trade, Price } from './types/trading';
import {
  fetchBots,
  fetchPortfolio,
  fetchTrades,
  fetchSignals,
  fetchPrices
} from './services/api';

const WS_URL = 'wss://your-backend-websocket-url'; // Replace with actual WS URL
const API_BASE = 'https://api-r4eb5eatnq-uc.a.run.app'; // Firebase Function base

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [bots, setBots] = useState<TradingBot[]>([]);
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [prices, setPrices] = useState<Price[]>([]);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    function connect() {
      wsRef.current = new WebSocket(WS_URL);

      wsRef.current.onopen = () => {
        console.log('WebSocket connected');
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const chain = data.chain || 'unknown';

          switch (data.type) {
            case 'signal':
              setSignals(prev => [{ ...data.payload, chain }, ...prev]);
              break;

            case 'price':
              setPrices(prev => {
                const updatedPayload = { ...data.payload, chain };
                const existingIndex = prev.findIndex(p => p.symbol === updatedPayload.symbol);
                if (existingIndex > -1) {
                  const updated = [...prev];
                  updated[existingIndex] = updatedPayload;
                  return updated;
                }
                return [updatedPayload, ...prev];
              });
              break;

            case 'trade':
              setTrades(prev => [{ ...data.payload, chain }, ...prev]);
              break;

            default:
              console.warn('Unknown WebSocket message type:', data.type);
          }
        } catch (err) {
          console.error('Failed to parse WS message:', err);
        }
      };

      wsRef.current.onerror = (err) => {
        console.error('WebSocket error:', err);
      };

      wsRef.current.onclose = () => {
        console.log('WebSocket disconnected. Reconnecting in 3s...');
        reconnectTimeout.current = setTimeout(connect, 3000);
      };
    }

    connect();

    return () => {
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      wsRef.current?.close();
    };
  }, []);

  const fetchInitialData = async () => {
    try {
      const [botsData, portfolioData, signalData, priceData, tradeData] = await Promise.all([
        fetchBots(),
        fetchPortfolio(),
        fetchSignals(),
        fetchPrices(),
        fetchTrades()
      ]);
      setBots(botsData);
      setPortfolio(portfolioData);
      setSignals(signalData);
      setPrices(priceData);
      setTrades(tradeData);
    } catch (error) {
      console.error('Failed to fetch initial data:', error);
    }
  };

  const handleToggleBot = async (botId: string) => {
    const bot = bots.find(b => b.id === botId);
    if (!bot) return;

    const updatedStatus = bot.status === 'active' ? 'paused' : 'active';

    try {
      const res = await fetch(`${API_BASE}/bots/${botId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: updatedStatus })
      });

      if (!res.ok) throw new Error('Failed to update bot');

      setBots(prev =>
        prev.map(b => (b.id === botId ? { ...b, status: updatedStatus } : b))
      );
    } catch (err) {
      console.error('Failed to toggle bot status:', err);
    }
  };

  const handleCreateBot = async (newBot: Omit<TradingBot, 'id'>) => {
    try {
      const res = await fetch(`${API_BASE}/bots`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...newBot, status: 'active' })
      });
      const createdBot = await res.json();
      setBots(prev => [...prev, createdBot]);
    } catch (err) {
      console.error('Failed to create bot:', err);
    }
  };

  const handleDeleteBot = async (botId: string) => {
    try {
      await fetch(`${API_BASE}/bots/${botId}`, {
        method: 'DELETE'
      });
      setBots(prev => prev.filter(bot => bot.id !== botId));
    } catch (err) {
      console.error('Failed to delete bot:', err);
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <div className="space-y-8">
            {portfolio && <PortfolioOverview portfolio={portfolio} />}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
              <div className="space-y-8">
                <BotStatus bots={bots} onToggleBot={handleToggleBot} />
                <TradeHistory trades={trades} />
              </div>
              <div className="space-y-8">
                <PriceMonitor prices={prices} />
                <SignalFeed signals={signals} />
              </div>
            </div>
          </div>
        );
      case 'bots':
        return (
          <BotManager
            bots={bots}
            onCreateBot={handleCreateBot}
            onToggleBot={handleToggleBot}
            onDeleteBot={handleDeleteBot}
          />
        );
      case 'signals':
        return (
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
            <SignalFeed signals={signals} />
            <PriceMonitor prices={prices} />
          </div>
        );
      case 'settings':
        return <SettingsPanel />;
      default:
        return <div className="text-white">Page not found</div>;
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Header activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="p-6 max-w-7xl mx-auto">{renderContent()}</main>
    </div>
  );
}

export default App;
