import ccxt
import pandas as pd
import numpy as np
import ta
from typing import Dict, List
from kucoin_client import KuCoinClient
import logging

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    def __init__(self):
        self.kucoin_client = KuCoinClient()
    
    async def analyze(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> Dict:
        """Perform technical analysis on a symbol"""
        try:
            # Get historical data
            ohlcv = await self.kucoin_client.exchange.fetch_ohlcv(
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
                'lower': bb.bollinger_lband().iloc[-1],
                'width': bb.bollinger_wband().iloc[-1]
            }
            
            # Moving Averages
            indicators['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator().iloc[-1]
            indicators['ema_12'] = ta.trend.EMAIndicator(df['close'], window=12).ema_indicator().iloc[-1]
            indicators['ema_26'] = ta.trend.EMAIndicator(df['close'], window=26).ema_indicator().iloc[-1]
            
            # Volume indicators
            indicators['volume_sma'] = ta.volume.VolumeSMAIndicator(
                df['close'], df['volume'], window=20
            ).volume_sma().iloc[-1]
            
            # Stochastic
            stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
            indicators['stochastic'] = {
                'k': stoch.stoch().iloc[-1],
                'd': stoch.stoch_signal().iloc[-1]
            }
            
            # Williams %R
            indicators['williams_r'] = ta.momentum.WilliamsRIndicator(
                df['high'], df['low'], df['close']
            ).williams_r().iloc[-1]
            
            # Average True Range (ATR)
            indicators['atr'] = ta.volatility.AverageTrueRange(
                df['high'], df['low'], df['close']
            ).average_true_range().iloc[-1]
            
            # Generate signals
            signals = self._generate_technical_signals(indicators, df['close'].iloc[-1])
            
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'current_price': df['close'].iloc[-1],
                'indicators': indicators,
                'signals': signals,
                'timestamp': df['timestamp'].iloc[-1].isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {e}")
            return {'error': str(e)}
    
    def _generate_technical_signals(self, indicators: Dict, current_price: float) -> Dict:
        """Generate trading signals from technical indicators"""
        signals = {
            'overall': 'neutral',
            'strength': 0,
            'individual_signals': {}
        }
        
        signal_count = 0
        total_strength = 0
        
        # RSI signals
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            signals['individual_signals']['rsi'] = 'oversold_buy'
            total_strength += 1
        elif rsi > 70:
            signals['individual_signals']['rsi'] = 'overbought_sell'
            total_strength -= 1
        else:
            signals['individual_signals']['rsi'] = 'neutral'
        signal_count += 1
        
        # MACD signals
        macd_data = indicators.get('macd', {})
        if macd_data.get('macd', 0) > macd_data.get('signal', 0):
            signals['individual_signals']['macd'] = 'bullish'
            total_strength += 1
        else:
            signals['individual_signals']['macd'] = 'bearish'
            total_strength -= 1
        signal_count += 1
        
        # Bollinger Bands signals
        bb = indicators.get('bollinger_bands', {})
        if current_price < bb.get('lower', current_price):
            signals['individual_signals']['bollinger'] = 'oversold_buy'
            total_strength += 1
        elif current_price > bb.get('upper', current_price):
            signals['individual_signals']['bollinger'] = 'overbought_sell'
            total_strength -= 1
        else:
            signals['individual_signals']['bollinger'] = 'neutral'
        signal_count += 1
        
        # Moving Average signals
        sma_20 = indicators.get('sma_20', current_price)
        ema_12 = indicators.get('ema_12', current_price)
        ema_26 = indicators.get('ema_26', current_price)
        
        if current_price > sma_20 and ema_12 > ema_26:
            signals['individual_signals']['moving_averages'] = 'bullish'
            total_strength += 1
        elif current_price < sma_20 and ema_12 < ema_26:
            signals['individual_signals']['moving_averages'] = 'bearish'
            total_strength -= 1
        else:
            signals['individual_signals']['moving_averages'] = 'neutral'
        signal_count += 1
        
        # Stochastic signals
        stoch = indicators.get('stochastic', {})
        stoch_k = stoch.get('k', 50)
        if stoch_k < 20:
            signals['individual_signals']['stochastic'] = 'oversold_buy'
            total_strength += 1
        elif stoch_k > 80:
            signals['individual_signals']['stochastic'] = 'overbought_sell'
            total_strength -= 1
        else:
            signals['individual_signals']['stochastic'] = 'neutral'
        signal_count += 1
        
        # Calculate overall signal
        if signal_count > 0:
            strength_ratio = total_strength / signal_count
            signals['strength'] = strength_ratio
            
            if strength_ratio > 0.3:
                signals['overall'] = 'bullish'
            elif strength_ratio < -0.3:
                signals['overall'] = 'bearish'
            else:
                signals['overall'] = 'neutral'
        
        return signals
    
    async def get_support_resistance(self, symbol: str, timeframe: str = '4h', limit: int = 200) -> Dict:
        """Calculate support and resistance levels"""
        try:
            ohlcv = await self.kucoin_client.exchange.fetch_ohlcv(
                symbol, timeframe, limit=limit
            )
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Find pivot points
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
            resistance_levels = sorted(resistance_levels, reverse=True)[:5]
            support_levels = sorted(support_levels)[:5]
            
            return {
                'symbol': symbol,
                'resistance_levels': resistance_levels,
                'support_levels': support_levels,
                'current_price': df['close'].iloc[-1]
            }
            
        except Exception as e:
            logger.error(f"Error calculating support/resistance: {e}")
            return {'error': str(e)}