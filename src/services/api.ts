const API_BASE_URL = 'http://localhost:8000/api';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export interface BotConfig {
  name: string;
  symbol: string;
  strategy: string;
  risk_level: string;
}

export interface BotStatus {
  id: string;
  name: string;
  symbol: string;
  status: string;
  strategy: string;
  current_position?: any;
  trades_today: number;
  daily_pnl: number;
  risk_level: string;
}

export interface SentimentData {
  symbol: string;
  combined_sentiment_score: number;
  sentiment_label: string;
  confidence: number;
  sources: {
    twitter?: any;
    reddit?: any;
    lunarcrush?: any;
  };
}

export interface TechnicalData {
  symbol: string;
  timeframe: string;
  current_price: number;
  indicators: {
    rsi: number;
    macd: any;
    bollinger_bands: any;
    sma_20: number;
    ema_12: number;
    ema_26: number;
  };
  signals: {
    overall: string;
    strength: number;
    individual_signals: any;
  };
}

class ApiService {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Account & Balance
  async getBalance() {
    return this.request<any>('/balance');
  }

  async getTicker(symbol: string) {
    return this.request<any>(`/ticker/${symbol}`);
  }

  // Bot Management
  async getBots() {
    return this.request<{ bots: BotStatus[] }>('/bots');
  }

  async createBot(config: BotConfig) {
    return this.request<{ message: string; bot_id: string }>('/bots', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  async updateBot(botId: string, status: string) {
    return this.request<{ message: string }>(`/bots/${botId}`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  async deleteBot(botId: string) {
    return this.request<{ message: string }>(`/bots/${botId}`, {
      method: 'DELETE',
    });
  }

  // Analysis
  async getSentiment(symbol: string) {
    return this.request<SentimentData>(`/sentiment/${symbol}`);
  }

  async getTechnicalAnalysis(symbol: string, timeframe: string = '1h') {
    return this.request<TechnicalData>(`/technical/${symbol}?timeframe=${timeframe}`);
  }

  async getSignals(symbol: string) {
    return this.request<any>(`/signals/${symbol}`);
  }

  // Trading
  async getOrders() {
    return this.request<{ orders: any[] }>('/orders');
  }
}

export const apiService = new ApiService();