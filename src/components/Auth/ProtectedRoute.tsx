import React from 'react';
import { Lock, Shield, User, ArrowRight } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  onOpenLogin?: () => void;
  onOpenRegister?: () => void;
}

const DefaultFallback = ({ onOpenLogin, onOpenRegister }: { onOpenLogin?: () => void; onOpenRegister?: () => void }) => (
  <div className="min-h-[60vh] flex items-center justify-center">
    <div className="max-w-md w-full mx-auto text-center">
      <div className="bg-gray-900 border border-gray-700 rounded-xl p-8 shadow-2xl">
        {/* Icon */}
        <div className="w-16 h-16 bg-blue-600/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <Lock className="w-8 h-8 text-blue-400" />
        </div>

        {/* Content */}
        <h2 className="text-2xl font-bold text-white mb-4">Authentication Required</h2>
        <p className="text-gray-400 mb-8">
          Please sign in to access your trading dashboard and manage your crypto bots.
        </p>

        {/* Features List */}
        <div className="space-y-3 mb-8 text-left">
          <div className="flex items-center gap-3 text-gray-300">
            <Shield className="w-5 h-5 text-blue-400" />
            <span>Secure account protection</span>
          </div>
          <div className="flex items-center gap-3 text-gray-300">
            <User className="w-5 h-5 text-blue-400" />
            <span>Personalized trading experience</span>
          </div>
          <div className="flex items-center gap-3 text-gray-300">
            <ArrowRight className="w-5 h-5 text-blue-400" />
            <span>Access to all premium features</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-3">
          <button
            onClick={onOpenLogin}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition-colors"
          >
            Sign In to Continue
          </button>
          <button
            onClick={onOpenRegister}
            className="w-full bg-gray-700 hover:bg-gray-600 text-white font-medium py-3 px-4 rounded-lg transition-colors"
          >
            Create New Account
          </button>
        </div>

        {/* Additional Info */}
        <div className="mt-6 pt-6 border-t border-gray-700">
          <p className="text-xs text-gray-500">
            By signing up, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>
      </div>
    </div>
  </div>
);

export default function ProtectedRoute({ children, fallback, onOpenLogin, onOpenRegister }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Loading your account...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return fallback ? <>{fallback}</> : <DefaultFallback onOpenLogin={onOpenLogin} onOpenRegister={onOpenRegister} />;
  }

  return <>{children}</>;
}