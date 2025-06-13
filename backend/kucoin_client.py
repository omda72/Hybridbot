import ccxt
import asyncio
from typing import Dict, List, Optional
from config import Config
import logging

logger = logging.getLogger(__name__)

class KuCoinClient:
    def __init__(self):
        self.exchange = ccxt.kucoin({
            'apiKey': Config.KUCOIN_API_KEY,
            'secret': Config.KUCOIN_API_SECRET,
            'password': Config.KUCOIN_API_PASSPHRASE,
            'sandbox': Config.KUCOIN_SANDBOX,
            'enableRateLimit': True,
        })
        
    async def get_balance(self) -> Dict:
        """Get account balance"""
        try:
            balance = await self.exchange.fetch_balance()
            return {
                'total': balance['total'],
                'free': balance['free'],
                'used': balance['used']
            }
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return {}
    
    async def get_ticker(self, symbol: str) -> Dict:
        """Get current price for symbol"""
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker['baseVolume'],
                'change': ticker['percentage']
            }
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return {}
    
    async def place_market_order(self, symbol: str, side: str, amount: float) -> Dict:
        """Place market order"""
        try:
            order = await self.exchange.create_market_order(
                symbol=symbol,
                side=side,
                amount=amount
            )
            logger.info(f"Order placed: {order}")
            return order
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return {'error': str(e)}
    
    async def place_limit_order(self, symbol: str, side: str, amount: float, price: float) -> Dict:
        """Place limit order"""
        try:
            order = await self.exchange.create_limit_order(
                symbol=symbol,
                side=side,
                amount=amount,
                price=price
            )
            logger.info(f"Limit order placed: {order}")
            return order
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            return {'error': str(e)}
    
    async def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """Get open orders"""
        try:
            orders = await self.exchange.fetch_open_orders(symbol)
            return orders
        except Exception as e:
            logger.error(f"Error fetching open orders: {e}")
            return []
    
    async def cancel_order(self, order_id: str, symbol: str) -> Dict:
        """Cancel order"""
        try:
            result = await self.exchange.cancel_order(order_id, symbol)
            return result
        except Exception as e:
            logger.error(f"Error canceling order: {e}")
            return {'error': str(e)}
    
    async def get_order_history(self, symbol: str = None, limit: int = 50) -> List[Dict]:
        """Get order history"""
        try:
            orders = await self.exchange.fetch_orders(symbol, limit=limit)
            return orders
        except Exception as e:
            logger.error(f"Error fetching order history: {e}")
            return []