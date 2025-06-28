# Binance API Keys
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

# Coinbase API Keys
COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
COINBASE_API_SECRET = os.getenv('COINBASE_API_SECRET')
COINBASE_API_PASSPHRASE = os.getenv('COINBASE_API_PASSPHRASE')

# Social Media APIs
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
LUNARCRUSH_API_KEY = os.getenv('LUNARCRUSH_API_KEY')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///trading_bot.db')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# Bot Configuration
MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_SIZE', '0.1'))  # 10% of portfolio
STOP_LOSS_PERCENTAGE = float(os.getenv('STOP_LOSS_PERCENTAGE', '0.05'))  # 5%
TAKE_PROFIT_PERCENTAGE = float(os.getenv('TAKE_PROFIT_PERCENTAGE', '0.15'))  # 15%

# API Server
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '8000'))