import React, { useState } from 'react';
import Header from './components/Layout/Header';
import PortfolioOverview from './components/Dashboard/PortfolioOverview';
import BotStatus from './components/Dashboard/BotStatus';
import PriceMonitor from './components/Dashboard/PriceMonitor';
import SignalFeed from './components/Signals/SignalFeed';
import BotManager from './components/Bots/BotManager';
import TradeHistory from './components/Trading/TradeHistory';
import SettingsPanel from './components/Settings/SettingsPanel';
import { mockBots, mockPortfolio, mockSignals, mockTrades, mockPrices } from './data/mockData';
import { TradingBot } from './types/trading';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [bots, setBots] = useState(mockBots);

  const handleToggleBot = (botId: string) => {
    setBots(prevBots =>
      prevBots.map(bot =>
        bot.id === botId
          ? { ...bot, status: bot.status === 'active' ? 'paused' : 'active' }
          : bot
      )
    );
  };

  const handleCreateBot = (newBot: Omit<TradingBot, 'id'>) => {
    const bot: TradingBot = {
      ...newBot,
      id: Date.now().toString()
    };
    setBots(prevBots => [...prevBots, bot]);
  };

  const handleDeleteBot = (botId: string) => {
    setBots(prevBots => prevBots.filter(bot => bot.id !== botId));
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <div className="space-y-8">
            <PortfolioOverview portfolio={mockPortfolio} />
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
              <div className="space-y-8">
                <BotStatus bots={bots} onToggleBot={handleToggleBot} />
                <TradeHistory trades={mockTrades} />
              </div>
              <div className="space-y-8">
                <PriceMonitor prices={mockPrices} />
                <SignalFeed signals={mockSignals} />
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
            <SignalFeed signals={mockSignals} />
            <PriceMonitor prices={mockPrices} />
          </div>
        );
      case 'settings':
        return <SettingsPanel />;
      default:
        return <div>Page not found</div>;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900">
      <Header activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="p-6">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;