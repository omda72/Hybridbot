import React, { useEffect, useState, useRef } from 'react';
import Header from './components/Layout/Header';
import PortfolioOverview from './components/Dashboard/PortfolioOverview';
import BotStatus from './components/Dashboard/BotStatus';
import PriceMonitor from './components/Dashboard/PriceMonitor';
import SignalFeed from './components/Signals/SignalFeed';
import BotManager from './components/Bots/BotManager';
import TradeHistory from './components/Trading/TradeHistory';
import SettingsPanel from './components/Settings/SettingsPanel';
import AuthManager from './components/Auth/AuthManager';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import { TradingBot, Portfolio, Signal, Trade, Price } from './types/trading';
import {
  fetchBots,
  fetchPortfolio,
  fetchTrades,
  fetchSignals,
  fetchPrices
} from './services/api';
import ReconnectingWebSocket from 'reconnecting-websocket';

// For local development, assuming your FastAPI runs on port 8000
// UPDATE THESE URLs to point to your FastAPI backend
const API_BASE = "http://localhost:8000"; // Local development API base URL
const WS_URL = 'ws://localhost:8000/ws/data'; // Local development WebSocket URL

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [bots, setBots] = useState<TradingBot[]>([]);
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [prices, setPrices] = useState<Price[]>([]);

  const wsRef = useRef<ReconnectingWebSocket | null>(null);
  const reconnectTimeout = useRef<number | null>(null);

  // Function to establish WebSocket connection
  const connectWebSocket = () => {
    wsRef.current = new ReconnectingWebSocket(WS_URL, [], {
      reconnectInterval: 1000,
      maxReconnectAttempts: 5,
    });

    wsRef.current.onopen = () => {
      console.log('WebSocket connected');
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
        reconnectTimeout.current = null;
      }
    };

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Handle different message types
        switch (data.type) {
          case 'bot_status_update':
            setBots(prevBots => 
              prevBots.map(bot => 
                bot.id === data.bot_id 
                  ? { ...bot, status: data.status, lastUpdate: data.timestamp }
                  : bot
              )
            );
            break;
          case 'new_signal':
            setSignals(prevSignals => [data.signal, ...prevSignals.slice(0, 49)]);
            break;
          case 'new_trade':
            setTrades(prevTrades => [data.trade, ...prevTrades.slice(0, 99)]);
            break;
          case 'price_update':
            setPrices(prevPrices => 
              prevPrices.map(price => 
                price.symbol === data.symbol 
                  ? { ...price, ...data.price }
                  : price
              )
            );
            break;
          case 'portfolio_update':
            setPortfolio(data.portfolio);
            break;
          default:
            console.warn('Unknown message type:', data.type);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    wsRef.current.onclose = (event) => {
      console.warn('WebSocket disconnected:', event);
      // Attempt to reconnect after a delay
      if (!reconnectTimeout.current) {
        reconnectTimeout.current = window.setTimeout(connectWebSocket, 5000);
      }
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      wsRef.current?.close(); // Close to trigger onclose and reconnect
    };
  };

  useEffect(() => {
    // Initial data fetches
    const loadData = async () => {
      try {
        const [botsData, portfolioData, tradesData, signalsData, pricesData] =
          await Promise.all([
            fetchBots(API_BASE),
            fetchPortfolio(API_BASE),
            fetchTrades(API_BASE),
            fetchSignals(API_BASE),
            fetchPrices(API_BASE),
          ]);
        setBots(botsData);
        setPortfolio(portfolioData);
        setTrades(tradesData);
        setSignals(signalsData);
        setPrices(pricesData);
      } catch (error) {
        console.error('Error fetching initial data:', error);
      }
    };

    loadData();
    connectWebSocket(); // Establish WebSocket connection on component mount

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
      }
    };
  }, []); // Empty dependency array means this runs once on mount

  // Handlers for bot actions
  const handleCreateBot = async (newBot: Omit<TradingBot, 'id'>) => {
    try {
      const response = await fetch(`${API_BASE}/bots`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newBot),
      });
      if (!response.ok) throw new Error('Failed to create bot');
      // WebSocket will update state via 'bot_status_update'
    } catch (error) {
      console.error('Error creating bot:', error);
    }
  };

  const handleToggleBot = async (botId: string) => {
    try {
      const response = await fetch(`${API_BASE}/bots/${botId}/toggle`, {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to toggle bot status');
      // Update local state if needed, or rely on WebSocket for updates
      // For now, WebSocket listener handles bot_status_update
    } catch (error) {
      console.error('Error toggling bot:', error);
    }
  };

  const handleDeleteBot = async (botId: string) => {
    try {
      const response = await fetch(`${API_BASE}/bots/${botId}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Failed to delete bot');
      // WebSocket listener handles bot_deleted update
    } catch (error) {
      console.error('Error deleting bot:', error);
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
    <AuthProvider>
      <div className="min-h-screen bg-gray-950 text-white">
        <AuthManager>
          <Header activeTab={activeTab} onTabChange={setActiveTab} />
        </AuthManager>
        <main className="container mx-auto p-8 pt-24">
          <ProtectedRoute>
            {renderContent()}
          </ProtectedRoute>
        </main>
      </div>
    </AuthProvider>
  );
}

export default App;