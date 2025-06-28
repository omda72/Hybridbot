import ccxt
import pandas as pd
import numpy as np
import ta
from typing import Dict, List
# No longer import KuCoinClient directly, as it will be injected via ExchangeClient
# from kucoin_client import KuCoinClient
import logging

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    def __init__(self, exchange_client: any): # Type hint can be more specific, e.g., 'ExchangeClient'
        self.exchange_client = exchange_client
    
    async def analyze(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> Dict:
        """Perform technical analysis on a symbol"""
        try:
            # Use the injected exchange_client
            ohlcv = await self.exchange_client.exchange.fetch_ohlcv(
                symbol, timeframe, limit=limit
            )
            
            if not ohlcv:
                return {'error': 'No historical data available'}
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Calculate technical indicators
            indicators = {}
            
            # RSI
            indicators['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi().iloc[-1]
            
            # MACD
            macd = ta.trend.MACD(df['close'])
            indicators['macd'] = {
                'macd': macd.macd().iloc[-1],
                'signal': macd.macd_signal().iloc[-1],
                'histogram': macd.macd_diff().iloc[-1]
            }
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
            indicators['bollinger_bands'] = {
                'upper': bb.bollinger_hband().iloc[-1],
                'middle': bb.bollinger_mavg().iloc[-1],
                'lower': bb.bollinger_lband().iloc[-1]
            }

            return {'symbol': symbol, **indicators}
            
        except Exception as e:
            logger.error(f"Error performing technical analysis for {symbol}: {e}")
            return {'error': str(e)}

    async def calculate_support_resistance(self, symbol: str, timeframe: str = '1d', limit: int = 200) -> Dict:
        """Calculate support and resistance levels"""
        try:
            # Use the injected exchange_client
            ohlcv = await self.exchange_client.exchange.fetch_ohlcv(
                symbol, timeframe, limit=limit
            )
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Find pivot points (simplified for example)
            highs = df['high'].rolling(window=10, center=True).max()
            lows = df['low'].rolling(window=10, center=True).min()
            
            resistance_levels = []
            support_levels = []
            
            for i in range(10, len(df) - 10):
                if df['high'].iloc[i] == highs.iloc[i]:
                    resistance_levels.append(df['high'].iloc[i])
                if df['low'].iloc[i] == lows.iloc[i]:
                    support_levels.append(df['low'].iloc[i])
            
            resistance_levels = sorted(list(set(resistance_levels)), reverse=True)[:5]
            support_levels = sorted(list(set(support_levels)))[:5]
            
            return {
                'symbol': symbol,
                'resistance_levels': resistance_levels,
                'support_levels': support_levels,
                'current_price': df['close'].iloc[-1]
            }
            
        except Exception as e:
            logger.error(f"Error calculating support/resistance: {e}")
            return {'error': str(e)}