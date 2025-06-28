import ccxt
from typing import Dict, List, Optional
from config import Config


class ExchangeClient:
    def __init__(self, exchange_id: str, config: Config):
        self.exchange_id = exchange_id.lower()
        self.config = config
        self.exchange = self._init_exchange()
        if self.exchange:
            self.exchange.enableRateLimit = True  # Enable ccxt's built-in rate limit handling

    def _init_exchange(self) -> Optional[ccxt.Exchange]:
        """Initializes the ccxt exchange instance based on exchange_id."""
        try:
            if self.exchange_id == 'kucoin':
                return ccxt.kucoin({
                    'apiKey': self.config.KUCOIN_API_KEY,
                    'secret': self.config.KUCOIN_API_SECRET,
                    'password': self.config.KUCOIN_API_PASSPHRASE,
                    'options': {
                        'defaultType': 'spot',  # or 'future' based on your needs
                        'adjustForTimeDifference': True,
                    },
                    'enableRateLimit': True,
                })
            elif self.exchange_id == 'binance':
                return ccxt.binance({
                    'apiKey': self.config.BINANCE_API_KEY,
                    'secret': self.config.BINANCE_API_SECRET,
                    'options': {
                        'defaultType': 'future',  # or 'spot' based on your needs
                        'adjustForTimeDifference': True,
                    },
                    'enableRateLimit': True,
                })
            elif self.exchange_id == 'coinbase':
                return ccxt.coinbasepro({
                    'apiKey': self.config.COINBASE_API_KEY,
                    'secret': self.config.COINBASE_API_SECRET,
                    'password': self.config.COINBASE_API_PASSPHRASE,
                    'options': {
                        'adjustForTimeDifference': True,
                    },
                    'enableRateLimit': True,
                })
            elif self.exchange_id == 'kraken':
                return ccxt.kraken({
                    'apiKey': self.config.KRAKEN_API_KEY,
                    'secret': self.config.KRAKEN_API_SECRET,
                    'options': {
                        'adjustForTimeDifference': True,
                    },
                    'enableRateLimit': True,
                })
            else:
                raise ValueError(f"Unsupported exchange ID: {self.exchange_id}")
        except Exception as e:
            # Handle exceptions without logging
            print(f"Error initializing {self.exchange_id} client: {e}")
            return None

    async def get_balance(self) -> Dict:
        """Get account balance"""
        if not self.exchange:
            return {'error': 'Exchange not initialized'}
        try:
            balance = await self.exchange.fetch_balance()
            return {
                'total': balance['total'],
                'free': balance['free'],
                'used': balance['used']
            }
        except ccxt.NetworkError as e:
            return {'error': f"Network error: {e}"}
        except ccxt.ExchangeError as e:
            return {'error': f"Exchange error: {e}"}
        except Exception as e:
            return {'error': str(e)}

    async def get_ticker(self, symbol: str) -> Dict:
        """Get current price for symbol"""
        if not self.exchange:
            return {'error': 'Exchange not initialized'}
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker.get('baseVolume', 'N/A'),
                'change': ticker.get('percentage', 'N/A')
            }
        except ccxt.NetworkError as e:
            return {'error': f"Network error: {e}"}
        except ccxt.ExchangeError as e:
            return {'error': f"Exchange error: {e}"}
        except Exception as e:
            return {'error': str(e)}

    async def place_market_order(self, symbol: str, side: str, amount: float) -> Dict:
        """Place market order"""
        if not self.exchange:
            return {'error': 'Exchange not initialized'}
        try:
            order = await self.exchange.create_market_order(
                symbol=symbol,
                side=side,
                amount=amount
            )
            return order
        except ccxt.NetworkError as e:
            return {'error': f"Network error: {e}"}
        except ccxt.ExchangeError as e:
            return {'error': f"Exchange error: {e}"}
        except ccxt.InvalidOrder as e:
            return {'error': f"Invalid order: {e}"}
        except Exception as e:
            return {'error': str(e)}

    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List[List]:
        """Fetch OHLCV data"""
        if not self.exchange:
            return []
        try:
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except ccxt.NetworkError as e:
            return []
        except ccxt.ExchangeError as e:
            return []
        except Exception as e:
            return []

    async def place_limit_order(self, symbol: str, side: str, amount: float, price: float) -> Dict:
        """Place limit order"""
        if not self.exchange:
            return {'error': 'Exchange not initialized'}
        try:
            order = await self.exchange.create_limit_order(
                symbol=symbol,
                side=side,
                amount=amount,
                price=price
            )
            return order
        except ccxt.NetworkError as e:
            return {'error': f"Network error: {e}"}
        except ccxt.ExchangeError as e:
            return {'error': f"Exchange error: {e}"}
        except ccxt