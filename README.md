# Crypto Trading Bot with KuCoin Integration

A sophisticated cryptocurrency trading bot that combines sentiment analysis from social media platforms with technical analysis to make informed trading decisions on KuCoin exchange.

## Features

### 🤖 Automated Trading
- **Multi-strategy support**: Sentiment-based, technical analysis, and hybrid strategies
- **Risk management**: Configurable stop-loss and take-profit levels
- **Position sizing**: Dynamic position sizing based on risk tolerance
- **Real-time execution**: Automated buy/sell orders based on signals

### 📊 Sentiment Analysis
- **Twitter sentiment**: Real-time analysis of crypto-related tweets
- **Reddit monitoring**: Sentiment from cryptocurrency subreddits
- **LunarCrush integration**: Professional social sentiment data
- **Combined scoring**: Weighted sentiment scores from multiple sources

### 📈 Technical Analysis
- **20+ Technical indicators**: RSI, MACD, Bollinger Bands, Moving Averages, etc.
- **Support/Resistance levels**: Automatic identification of key price levels
- **Signal generation**: Combined technical signals with confidence scores
- **Multiple timeframes**: Analysis across different time periods

### 🎯 KuCoin Integration
- **Full API support**: Account balance, order management, real-time prices
- **Secure trading**: Encrypted API key management
- **Order types**: Market and limit orders with advanced options
- **Real-time data**: WebSocket connections for live price feeds

## Architecture

```
Frontend (React/TypeScript)
├── Dashboard with real-time updates
├── Bot management interface
├── Signal monitoring
└── Trading history

Backend (Python/FastAPI)
├── KuCoin API integration
├── Sentiment analysis engine
├── Technical analysis module
├── Trading bot orchestration
└── REST API server
```

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 2. Configure API Keys

Edit `backend/.env`:

```env
# KuCoin API (get from KuCoin Pro account)
KUCOIN_API_KEY=your_api_key
KUCOIN_API_SECRET=your_api_secret
KUCOIN_API_PASSPHRASE=your_passphrase
KUCOIN_SANDBOX=true  # Set to false for live trading

# Social Media APIs (optional but recommended)
TWITTER_BEARER_TOKEN=your_twitter_token
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret
LUNARCRUSH_API_KEY=your_lunarcrush_key
```

### 3. Start the Backend

```bash
cd backend
python run_bot.py
```

The API server will start at `http://localhost:8000`

### 4. Start the Frontend

```bash
npm install
npm run dev
```

The React app will be available at `http://localhost:5173`

## Bot Configuration

### Strategy Types

1. **Sentiment Momentum**
   - 40% sentiment analysis weight
   - 60% technical momentum weight
   - Best for: Swing trading, trend following

2. **Technical Sentiment**
   - 70% technical analysis weight
   - 30% sentiment confirmation
   - Best for: Scalping, short-term trades

3. **Balanced Strategy**
   - 50% sentiment, 50% technical
   - Best for: Medium-term position trading

### Risk Levels

- **Low Risk**: 0.5x position sizing, conservative signals
- **Medium Risk**: 1.0x position sizing, balanced approach
- **High Risk**: 1.5x position sizing, aggressive signals

## API Endpoints

### Bot Management
- `GET /api/bots` - List all bots
- `POST /api/bots` - Create new bot
- `PUT /api/bots/{id}` - Update bot status
- `DELETE /api/bots/{id}` - Delete bot

### Market Data
- `GET /api/ticker/{symbol}` - Current price
- `GET /api/balance` - Account balance
- `GET /api/orders` - Order history

### Analysis
- `GET /api/sentiment/{symbol}` - Sentiment analysis
- `GET /api/technical/{symbol}` - Technical analysis
- `GET /api/signals/{symbol}` - Combined signals

## Safety Features

### Risk Management
- **Maximum position size**: Configurable per bot (default 10%)
- **Stop-loss orders**: Automatic loss limitation (default 5%)
- **Take-profit orders**: Automatic profit taking (default 15%)
- **Daily limits**: Maximum trades per day per bot

### Security
- **API key encryption**: Secure storage of exchange credentials
- **Sandbox mode**: Test strategies without real money
- **Rate limiting**: Respect exchange API limits
- **Error handling**: Comprehensive error recovery

## Monitoring & Alerts

### Real-time Dashboard
- Live bot status and performance
- Current positions and P&L
- Signal feed with confidence scores
- Price monitoring with technical overlays

### Notifications (Coming Soon)
- Email alerts for significant events
- Telegram bot integration
- Push notifications for mobile app

## Performance Optimization

### Latency Considerations
- **Signal processing**: ~800ms average
- **Order execution**: 200-500ms to KuCoin
- **Suitable for**: 15min+ timeframe strategies
- **Not suitable for**: High-frequency trading

### Scalability
- **Multiple bots**: Run different strategies simultaneously
- **Symbol coverage**: Support for all KuCoin trading pairs
- **Resource usage**: Optimized for VPS deployment

## Deployment

### Local Development
```bash
# Backend
cd backend && python run_bot.py

# Frontend
npm run dev
```

### Production Deployment
```bash
# Backend (using Docker)
docker build -t crypto-bot-backend ./backend
docker run -d -p 8000:8000 crypto-bot-backend

# Frontend
npm run build
# Deploy dist/ folder to your web server
```

### VPS Deployment
Recommended specs:
- **CPU**: 2+ cores
- **RAM**: 4GB+
- **Storage**: 20GB SSD
- **Network**: Stable connection to exchange servers

## Legal Disclaimer

⚠️ **Important**: This software is for educational purposes only. Cryptocurrency trading involves substantial risk of loss. Past performance does not guarantee future results. Always:

- Start with small amounts
- Use sandbox mode first
- Understand the risks involved
- Comply with local regulations
- Never invest more than you can afford to lose

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- **Documentation**: Check the `/docs` folder
- **Issues**: Report bugs on GitHub
- **Community**: Join our Discord server
- **Email**: support@cryptobotpro.com

## License

MIT License - see LICENSE file for details.

---

**Happy Trading! 🚀**

*Remember: The best strategy is the one you understand and can stick with consistently.*