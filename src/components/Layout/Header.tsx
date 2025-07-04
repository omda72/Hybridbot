import React, { useState } from 'react';
import { Bot, Settings, Bell, User, LogIn } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import UserDropdown from '../Auth/UserDropdown';

interface HeaderProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  onOpenLogin?: () => void;
  onOpenRegister?: () => void;
}

export default function Header({ activeTab, onTabChange, onOpenLogin, onOpenRegister }: HeaderProps) {
  const [showProfile, setShowProfile] = useState(false);
  const { isAuthenticated, isLoading } = useAuth();
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: Bot },
    { id: 'bots', label: 'Trading Bots', icon: Bot },
    { id: 'signals', label: 'Signals', icon: Bell },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  return (
    <header className="bg-gray-900 border-b border-gray-800">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-3">
              <Bot className="w-8 h-8 text-blue-500" />
              <h1 className="text-xl font-bold text-white">CryptoBot Pro</h1>
            </div>
            
            <nav className="flex space-x-6">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => onTabChange(tab.id)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-300 hover:text-white hover:bg-gray-800'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <button className="p-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-blue-500 rounded-full"></span>
            </button>

            {/* Authentication Section */}
            {isLoading ? (
              <div className="w-8 h-8 bg-gray-700 rounded-full animate-pulse"></div>
            ) : isAuthenticated ? (
              <UserDropdown onOpenProfile={() => setShowProfile(true)} />
            ) : (
              <div className="flex items-center space-x-2">
                <button
                  onClick={onOpenLogin}
                  className="px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors font-medium"
                >
                  Sign In
                </button>
                <button
                  onClick={onOpenRegister}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
                >
                  Sign Up
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}