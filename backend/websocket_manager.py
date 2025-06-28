import ccxt
import asyncio
import logging
from typing import Dict, List, Optional, Any
from config import Config

logger = logging.getLogger(__name__)

class ExchangeClient:
    """
    A generic client for interacting with various cryptocurrency exchanges via CCXT.
    Supports KuCoin, Binance, and Coinbase, based on configuration.
    """
    def __init__(self, exchange_id: str):
        self.exchange_id = exchange_id.lower()
        self.exchange: Optional[ccxt.Exchange] = None
        self._initialize_exchange()

    def _initialize_exchange(self):
        """Initializes the CCXT exchange instance based on exchange_id."""
        exchange_class = getattr(ccxt, self.exchange_id, None)
        if not exchange_class:
            raise ValueError(f"Unsupported exchange ID: {self.exchange_id}")

        config_params = {}
        if self.exchange_id == 'kucoin':
            config_params = {
                'apiKey': Config.KUCOIN_API_KEY,
                'secret': Config.KUCOIN_API_SECRET,
                'password': Config.KUCOIN_API_PASSPHRASE,
                'sandbox': Config.KUCOIN_SANDBOX,
                'enableRateLimit': True,
            }
        elif self.exchange_id == 'binance':
            config_params = {
                'apiKey': Config.BINANCE_API_KEY,
                'secret': Config.BINANCE_API_SECRET,
                'options': {
                    'defaultType': 'spot', # 'spot', 'future', 'margin'
                },
                'enableRateLimit': True,
            }
        elif self.exchange_id == 'coinbase': # Coinbase Pro (Advanced Trade API)
            config_params = {
                'apiKey': Config.COINBASE_API_KEY,
                'secret': Config.COINBASE_API_SECRET,
                'password': Config.COINBASE_API_PASSPHRASE, # For Coinbase Pro
                'enableRateLimit': True,
            }
        # Add more exchanges here as needed

        if not all(config_params.values()):
            logger.warning(f"API credentials for {self.exchange_id} are incomplete. Some operations might fail.")
            # Depending on your need, you might raise an error here or continue
            # if public data access is sufficient.

        self.exchange = exchange_class(config_params)
        logger.info(f"Initialized {self.exchange_id} exchange client.")

    async def get_balance(self) -> Dict:
        """Get account balance for the initialized exchange."""
        try:
            if not self.exchange:
                return {'error': 'Exchange not initialized.'}
            balance = await self.exchange.fetch_balance()
            return {
                'total': balance['total'],
                'free': balance['free'],
                'used': balance['used']
            }
        except ccxt.NetworkError as e:
            logger.error(f"Network error fetching balance from {self.exchange_id}: {e}")
            return {'error': f"Network error: {e}"}
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error fetching balance from {self.exchange_id}: {e}")
            return {'error': f"Exchange error: {e}"}
        except Exception as e:
            logger.error(f"Unexpected error fetching balance from {self.exchange_id}: {e}", exc_info=True)
            return {'error': str(e)}

    async def get_ticker(self, symbol: str) -> Dict:
        """Get current price for a symbol from the initialized exchange."""
        try:
            if not self.exchange:
                return {'error': 'Exchange not initialized.'}
            ticker = await self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker['baseVolume'],
                'change': ticker['percentage']
            }
        except ccxt.NetworkError as e:
            logger.error(f"Network error fetching ticker for {symbol} from {self.exchange_id}: {e}")
            return {'error': f"Network error: {e}"}
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error fetching ticker for {symbol} from {self.exchange_id}: {e}")
            return {'error': f"Exchange error: {e}"}
        except Exception as e:
            logger.error(f"Unexpected error fetching ticker for {symbol} from {self.exchange_id}: {e}", exc_info=True)
            return {'error': str(e)}

    async def place_market_order(self, symbol: str, side: str, amount: float) -> Dict:
        """Place a market order on the initialized exchange."""
        try:
            if not self.exchange:
                return {'error': 'Exchange not initialized.'}
            order = await self.exchange.create_market_order(
                symbol=symbol,
                side=side,
                amount=amount
            )
            logger.info(f"Market {side} order placed on {self.exchange_id} for {amount} {symbol}: {order}")
            return order
        except ccxt.NetworkError as e:
            logger.error(f"Network error placing market order on {self.exchange_id}: {e}")
            return {'error': f"Network error: {e}"}
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error placing market order on {self.exchange_id}: {e}")
            return {'error': f"Exchange error: {e}"}
        except Exception as e:
            logger.error(f"Unexpected error placing market order on {self.exchange_id}: {e}", exc_info=True)
            return {'error': str(e)}

    async def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List[List[float]]:
        """Fetch OHLCV data from the initialized exchange."""
        try:
            if not self.exchange:
                return []
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except ccxt.NetworkError as e:
            logger.error(f"Network error fetching OHLCV for {symbol} from {self.exchange_id}: {e}")
            return []
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error fetching OHLCV for {symbol} from {self.exchange_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching OHLCV for {symbol} from {self.exchange_id}: {e}", exc_info=True)
            return []

    # You can add more generic methods here as needed, e.g.:
    # async def place_limit_order(self, symbol: str, side: str, amount: float, price: float) -> Dict:
    # async def cancel_order(self, order_id: str, symbol: str) -> Dict:
    # async def get_open_orders(self, symbol: str = None) -> List[Dict]:
    # async def get_order_history(self, symbol: str = None, limit: int = 50) -> List[Dict]:

# Example Usage (for testing purposes)
if __name__ == "__main__":
    import os
    # Basic logging setup for standalone execution
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Dummy Config for testing if config.py is not fully set up
    class TestConfig(Config):
        # Ensure these are populated from your .env for real tests
        KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY", "YOUR_KUCOIN_API_KEY")
        KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET", "YOUR_KUCOIN_API_SECRET")
        KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE", "YOUR_KUCOIN_API_PASSPHRASE")
        KUCOIN_SANDBOX = True # Set to False for production

        BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "YOUR_BINANCE_API_KEY")
        BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "YOUR_BINANCE_API_SECRET")

        COINBASE_API_KEY = os.getenv("COINBASE_API_KEY", "YOUR_COINBASE_API_KEY")
        COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET", "YOUR_COINBASE_API_SECRET")
        COINBASE_API_PASSPHRASE = os.getenv("COINBASE_API_PASSPHRASE", "YOUR_COINBASE_API_PASSPHRASE") # For Coinbase Pro

    async def test_exchange_client():
        # Test KuCoin
        print("\n--- Testing KuCoin Client ---")
        kucoin_client = ExchangeClient('kucoin')
        if kucoin_client.exchange:
            ticker = await kucoin_client.get_ticker('BTC/USDT')
            print(f"KuCoin BTC/USDT Ticker: {ticker}")
            balance = await kucoin_client.get_balance()
            print(f"KuCoin Balance: {balance.get('free', 'N/A')}")
            ohlcv = await kucoin_client.get_ohlcv('BTC/USDT', '1h', 5)
            print(f"KuCoin BTC/USDT OHLCV (last 5): {ohlcv}")
        else:
            print("KuCoin client not initialized (check API keys).")

        # Test Binance
        print("\n--- Testing Binance Client ---")
        binance_client = ExchangeClient('binance')
        if binance_client.exchange:
            ticker = await binance_client.get_ticker('BTC/USDT')
            print(f"Binance BTC/USDT Ticker: {ticker}")
            balance = await binance_client.get_balance()
            print(f"Binance Balance: {balance.get('free', 'N/A')}")
        else:
            print("Binance client not initialized (check API keys).")

        # Test Coinbase
        print("\n--- Testing Coinbase Client ---")
        coinbase_client = ExchangeClient('coinbase')
        if coinbase_client.exchange:
            ticker = await coinbase_client.get_ticker('BTC/USDT')
            print(f"Coinbase BTC/USDT Ticker: {ticker}")
            balance = await coinbase_client.get_balance()
            print(f"Coinbase Balance: {balance.get('free', 'N/A')}")
        else:
            print("Coinbase client not initialized (check API keys).")

    # To run the test, make sure you have ccxt installed: pip install ccxt aiohttp
    # And populate your .env file with actual API keys for testing.
    # Then run: python exchange_client.py
    asyncio.run(test_exchange_client())