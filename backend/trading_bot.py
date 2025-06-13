import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from kucoin_client import KuCoinClient
from sentiment_analyzer import SentimentAnalyzer
from technical_analyzer import TechnicalAnalyzer
from config import Config
import json

logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self, bot_config: Dict):
        self.bot_id = bot_config['id']
        self.name = bot_config['name']
        self.symbol = bot_config['symbol']
        self.strategy = bot_config['strategy']
        self.status = bot_config.get('status', 'stopped')
        self.risk_level = bot_config.get('risk_level', 'medium')
        
        # Initialize clients
        self.kucoin_client = KuCoinClient()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        
        # Trading parameters
        self.position_size = self._get_position_size()
        self.stop_loss = Config.STOP_LOSS_PERCENTAGE
        self.take_profit = Config.TAKE_PROFIT_PERCENTAGE
        
        # State tracking
        self.current_position = None
        self.last_signal_time = None
        self.trades_today = 0
        self.daily_pnl = 0.0
        
    def _get_position_size(self) -> float:
        """Calculate position size based on risk level"""
        base_size = Config.MAX_POSITION_SIZE
        
        risk_multipliers = {
            'low': 0.5,
            'medium': 1.0,
            'high': 1.5
        }
        
        return base_size * risk_multipliers.get(self.risk_level, 1.0)
    
    async def start(self):
        """Start the trading bot"""
        self.status = 'active'
        logger.info(f"Starting bot {self.name} for {self.symbol}")
        
        while self.status == 'active':
            try:
                await self.execute_trading_cycle()
                await asyncio.sleep(60)  # Wait 1 minute between cycles
            except Exception as e:
                logger.error(f"Error in trading cycle: {e}")
                await asyncio.sleep(30)  # Wait 30 seconds on error
    
    async def stop(self):
        """Stop the trading bot"""
        self.status = 'stopped'
        logger.info(f"Stopping bot {self.name}")
    
    async def pause(self):
        """Pause the trading bot"""
        self.status = 'paused'
        logger.info(f"Pausing bot {self.name}")
    
    async def execute_trading_cycle(self):
        """Execute one trading cycle"""
        try:
            # Get current market data
            ticker = await self.kucoin_client.get_ticker(self.symbol)
            if not ticker:
                return
            
            current_price = ticker['price']
            
            # Generate trading signal
            signal = await self.generate_signal(current_price)
            
            if signal and signal['action'] != 'hold':
                await self.execute_signal(signal, current_price)
            
            # Check existing positions
            await self.manage_positions(current_price)
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")
    
    async def generate_signal(self, current_price: float) -> Optional[Dict]:
        """Generate trading signal based on strategy"""
        try:
            # Get sentiment analysis
            sentiment_data = await self.sentiment_analyzer.get_combined_sentiment(
                self.symbol.split('/')[0]  # Extract base currency (e.g., BTC from BTC/USDT)
            )
            
            # Get technical analysis
            technical_data = await self.technical_analyzer.analyze(self.symbol)
            
            # Apply strategy logic
            if self.strategy == 'sentiment_momentum':
                return await self._sentiment_momentum_strategy(
                    sentiment_data, technical_data, current_price
                )
            elif self.strategy == 'technical_sentiment':
                return await self._technical_sentiment_strategy(
                    sentiment_data, technical_data, current_price
                )
            else:
                return await self._default_strategy(
                    sentiment_data, technical_data, current_price
                )
                
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return None
    
    async def _sentiment_momentum_strategy(self, sentiment: Dict, technical: Dict, price: float) -> Dict:
        """Strategy based on sentiment and momentum"""
        signal_strength = 0
        action = 'hold'
        
        # Sentiment component (40% weight)
        if 'combined_sentiment_score' in sentiment:
            sentiment_score = sentiment['combined_sentiment_score']
            signal_strength += sentiment_score * 0.4
        
        # Technical momentum component (60% weight)
        if 'rsi' in technical and 'macd' in technical:
            rsi = technical['rsi']
            macd_signal = technical['macd']['signal']
            
            # RSI momentum
            if rsi < 30:  # Oversold
                signal_strength += 0.3
            elif rsi > 70:  # Overbought
                signal_strength -= 0.3
            
            # MACD momentum
            if macd_signal > 0:  # Bullish
                signal_strength += 0.3
            else:  # Bearish
                signal_strength -= 0.3
        
        # Generate action based on signal strength
        if signal_strength > 0.3:
            action = 'buy'
        elif signal_strength < -0.3:
            action = 'sell'
        
        return {
            'action': action,
            'strength': abs(signal_strength),
            'confidence': min(abs(signal_strength) * 100, 100),
            'reasoning': f"Sentiment: {sentiment.get('sentiment_label', 'unknown')}, "
                        f"Technical: {'bullish' if signal_strength > 0 else 'bearish'}"
        }
    
    async def _technical_sentiment_strategy(self, sentiment: Dict, technical: Dict, price: float) -> Dict:
        """Strategy prioritizing technical analysis with sentiment confirmation"""
        # Implementation for technical-first strategy
        # Similar structure to sentiment_momentum_strategy but with different weights
        pass
    
    async def _default_strategy(self, sentiment: Dict, technical: Dict, price: float) -> Dict:
        """Default balanced strategy"""
        # Balanced approach between sentiment and technical analysis
        pass
    
    async def execute_signal(self, signal: Dict, current_price: float):
        """Execute trading signal"""
        try:
            if signal['action'] == 'buy' and not self.current_position:
                await self._execute_buy_order(current_price, signal)
            elif signal['action'] == 'sell' and self.current_position:
                await self._execute_sell_order(current_price, signal)
                
        except Exception as e:
            logger.error(f"Error executing signal: {e}")
    
    async def _execute_buy_order(self, price: float, signal: Dict):
        """Execute buy order"""
        try:
            # Calculate position size in base currency
            balance = await self.kucoin_client.get_balance()
            quote_balance = balance['free'].get('USDT', 0)  # Assuming USDT quote
            
            if quote_balance < 10:  # Minimum $10 trade
                logger.warning("Insufficient balance for trade")
                return
            
            trade_amount = min(quote_balance * self.position_size, quote_balance - 5)  # Keep $5 buffer
            quantity = trade_amount / price
            
            # Place market buy order
            order = await self.kucoin_client.place_market_order(
                symbol=self.symbol,
                side='buy',
                amount=quantity
            )
            
            if 'error' not in order:
                self.current_position = {
                    'side': 'long',
                    'entry_price': price,
                    'quantity': quantity,
                    'order_id': order['id'],
                    'timestamp': datetime.now(),
                    'stop_loss': price * (1 - self.stop_loss),
                    'take_profit': price * (1 + self.take_profit)
                }
                
                logger.info(f"Buy order executed: {order}")
                
        except Exception as e:
            logger.error(f"Error executing buy order: {e}")
    
    async def _execute_sell_order(self, price: float, signal: Dict):
        """Execute sell order"""
        try:
            if not self.current_position:
                return
            
            # Place market sell order
            order = await self.kucoin_client.place_market_order(
                symbol=self.symbol,
                side='sell',
                amount=self.current_position['quantity']
            )
            
            if 'error' not in order:
                # Calculate P&L
                entry_price = self.current_position['entry_price']
                pnl = (price - entry_price) * self.current_position['quantity']
                self.daily_pnl += pnl
                self.trades_today += 1
                
                logger.info(f"Sell order executed: {order}, P&L: ${pnl:.2f}")
                
                # Clear position
                self.current_position = None
                
        except Exception as e:
            logger.error(f"Error executing sell order: {e}")
    
    async def manage_positions(self, current_price: float):
        """Manage existing positions (stop loss, take profit)"""
        if not self.current_position:
            return
        
        try:
            position = self.current_position
            
            # Check stop loss
            if current_price <= position['stop_loss']:
                logger.info(f"Stop loss triggered at {current_price}")
                await self._execute_sell_order(current_price, {'action': 'sell', 'reason': 'stop_loss'})
            
            # Check take profit
            elif current_price >= position['take_profit']:
                logger.info(f"Take profit triggered at {current_price}")
                await self._execute_sell_order(current_price, {'action': 'sell', 'reason': 'take_profit'})
            
            # Check position age (close after 24 hours)
            elif datetime.now() - position['timestamp'] > timedelta(hours=24):
                logger.info("Position expired, closing")
                await self._execute_sell_order(current_price, {'action': 'sell', 'reason': 'expired'})
                
        except Exception as e:
            logger.error(f"Error managing positions: {e}")
    
    def get_status(self) -> Dict:
        """Get bot status and statistics"""
        return {
            'id': self.bot_id,
            'name': self.name,
            'symbol': self.symbol,
            'status': self.status,
            'strategy': self.strategy,
            'current_position': self.current_position,
            'trades_today': self.trades_today,
            'daily_pnl': self.daily_pnl,
            'risk_level': self.risk_level
        }