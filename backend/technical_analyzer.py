import ccxt
import pandas as pd
import numpy as np
import ta
from typing import Dict, List
# Update import for ExchangeClient
from exchange_client import ExchangeClient # From the new generic client
import logging

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    # Update __init__ to accept injected ExchangeClient
    def __init__(self, exchange_client: ExchangeClient):
        self.exchange_client = exchange_client

    async def analyze(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> Dict:
        """Perform technical analysis on a symbol"""
        try:
            # Use the injected exchange_client to fetch OHLCV
            ohlcv = await self.exchange_client.fetch_ohlcv(
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
            bb = ta.volatility.BollingerBands(df['close'])
            indicators['bollinger_bands'] = {
                'upper': bb.bollinger_hband().iloc[-1],
                'middle': bb.bollinger_mavg().iloc[-1],
                'lower': bb.bollinger_lband().iloc[-1]
            }

            # Moving Averages
            indicators['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator().iloc[-1]
            indicators['ema_50'] = ta.trend.EMAIndicator(df['close'], window=50).ema_indicator().iloc[-1]

            # Volume SMA (example)
            indicators['volume_sma_20'] = ta.volume.VolumeWeightedAveragePrice(
                df['high'], df['low'], df['close'], df['volume'], window=20
            ).volume_weighted_average_price().iloc[-1] # Corrected from SMAIndicator for volume

            # Stochastic Oscillator
            stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
            indicators['stochastic'] = {
                'k': stoch.stoch().iloc[-1],
                'd': stoch.stoch_signal().iloc[-1]
            }

            # Williams %R
            indicators['williams_r'] = ta.momentum.WilliamsRIndicator(df['high'], df['low'], df['close']).williams_r().iloc[-1]

            # Average True Range (ATR)
            indicators['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range().iloc[-1]


            overall_signal = self._generate_technical_signals(indicators)

            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'current_price': df['close'].iloc[-1],
                'indicators': indicators,
                'overall_signal': overall_signal
            }

        except Exception as e:
            logger.error(f"Error performing technical analysis for {symbol}: {e}", exc_info=True)
            return {'error': str(e)}

    def _generate_technical_signals(self, indicators: Dict) -> str:
        """Generate a simple buy/sell/neutral signal based on indicators"""
        buy_strength = 0
        sell_strength = 0

        # RSI
        if indicators['rsi'] < 30: # Oversold
            buy_strength += 1
        elif indicators['rsi'] > 70: # Overbought
            sell_strength += 1

        # MACD Crossover (simple logic)
        if indicators['macd']['macd'] > indicators['macd']['signal'] and indicators['macd']['histogram'] > 0:
            buy_strength += 1
        elif indicators['macd']['macd'] < indicators['macd']['signal'] and indicators['macd']['histogram'] < 0:
            sell_strength += 1

        # Bollinger Bands (price crossing outside)
        current_price = indicators['bollinger_bands']['middle'] # Using middle band as proxy for current price check
        if current_price < indicators['bollinger_bands']['lower']:
            buy_strength += 1
        elif current_price > indicators['bollinger_bands']['upper']:
            sell_strength += 1

        # Moving Averages Crossover (SMA20 over EMA50)
        if indicators['sma_20'] > indicators['ema_50']:
            buy_strength += 1
        elif indicators['sma_20'] < indicators['ema_50']:
            sell_strength += 1

        # Stochastic Oscillator
        if indicators['stochastic']['k'] < 20 and indicators['stochastic']['d'] < 20 and indicators['stochastic']['k'] > indicators['stochastic']['d']: # Oversold and K crossing above D
            buy_strength += 1
        elif indicators['stochastic']['k'] > 80 and indicators['stochastic']['d'] > 80 and indicators['stochastic']['k'] < indicators['stochastic']['d']: # Overbought and K crossing below D
            sell_strength += 1

        # Williams %R
        if indicators['williams_r'] < -80: # Oversold
            buy_strength += 1
        elif indicators['williams_r'] > -20: # Overbought
            sell_strength += 1

        if buy_strength > sell_strength:
            return 'buy'
        elif sell_strength > buy_strength:
            return 'sell'
        else:
            return 'neutral'

    async def get_support_resistance(self, symbol: str, timeframe: str = '1d', limit: int = 100) -> Dict:
        """Calculate support and resistance levels"""
        try:
            ohlcv = await self.exchange_client.fetch_ohlcv( # Use injected client
                symbol, timeframe, limit=limit
            )

            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # Find pivot points (simplified for example)
            highs = df['high'].rolling(window=10, center=True).max()
            lows = df['low'].rolling(window=10, center=True).min()

            # Identify support and resistance levels
            resistance_levels = []
            support_levels = []

            for i in range(10, len(df) - 10):
                if df['high'].iloc[i] == highs.iloc[i]:
                    resistance_levels.append(df['high'].iloc[i])
                if df['low'].iloc[i] == lows.iloc[i]:
                    support_levels.append(df['low'].iloc[i])

            # Get the most significant levels (by frequency)
            # A more robust approach would involve clustering or statistical analysis
            resistance_levels = sorted(list(set(resistance_levels)), reverse=True)[:5]
            support_levels = sorted(list(set(support_levels)))[:5]

            return {
                'symbol': symbol,
                'resistance_levels': resistance_levels,
                'support_levels': support_levels,
                'current_price': df['close'].iloc[-1]
            }

        except Exception as e:
            logger.error(f"Error calculating support/resistance: {e}", exc_info=True)
            return {'error': str(e)}