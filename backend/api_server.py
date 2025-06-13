from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import logging
from datetime import datetime

from trading_bot import TradingBot
from kucoin_client import KuCoinClient
from sentiment_analyzer import SentimentAnalyzer
from technical_analyzer import TechnicalAnalyzer
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Crypto Trading Bot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
kucoin_client = KuCoinClient()
sentiment_analyzer = SentimentAnalyzer()
technical_analyzer = TechnicalAnalyzer()
active_bots: Dict[str, TradingBot] = {}

# Pydantic models
class BotConfig(BaseModel):
    name: str
    symbol: str
    strategy: str
    risk_level: str = "medium"

class BotUpdate(BaseModel):
    status: str

# API Routes
@app.get("/")
async def root():
    return {"message": "Crypto Trading Bot API", "status": "running"}

@app.get("/api/balance")
async def get_balance():
    """Get account balance"""
    try:
        balance = await kucoin_client.get_balance()
        return balance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ticker/{symbol}")
async def get_ticker(symbol: str):
    """Get current price for symbol"""
    try:
        ticker = await kucoin_client.get_ticker(symbol)
        return ticker
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sentiment/{symbol}")
async def get_sentiment(symbol: str):
    """Get sentiment analysis for symbol"""
    try:
        sentiment = await sentiment_analyzer.get_combined_sentiment(symbol)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/technical/{symbol}")
async def get_technical_analysis(symbol: str, timeframe: str = "1h"):
    """Get technical analysis for symbol"""
    try:
        analysis = await technical_analyzer.analyze(symbol, timeframe)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bots")
async def get_bots():
    """Get all trading bots"""
    try:
        bots_status = []
        for bot_id, bot in active_bots.items():
            status = bot.get_status()
            bots_status.append(status)
        return {"bots": bots_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bots")
async def create_bot(bot_config: BotConfig, background_tasks: BackgroundTasks):
    """Create a new trading bot"""
    try:
        bot_id = f"bot_{len(active_bots) + 1}_{int(datetime.now().timestamp())}"
        
        config = {
            "id": bot_id,
            "name": bot_config.name,
            "symbol": bot_config.symbol,
            "strategy": bot_config.strategy,
            "risk_level": bot_config.risk_level,
            "status": "stopped"
        }
        
        bot = TradingBot(config)
        active_bots[bot_id] = bot
        
        return {"message": "Bot created successfully", "bot_id": bot_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/bots/{bot_id}")
async def update_bot(bot_id: str, bot_update: BotUpdate, background_tasks: BackgroundTasks):
    """Update bot status (start/stop/pause)"""
    try:
        if bot_id not in active_bots:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        bot = active_bots[bot_id]
        
        if bot_update.status == "active":
            background_tasks.add_task(bot.start)
        elif bot_update.status == "stopped":
            await bot.stop()
        elif bot_update.status == "paused":
            await bot.pause()
        
        return {"message": f"Bot {bot_id} status updated to {bot_update.status}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/bots/{bot_id}")
async def delete_bot(bot_id: str):
    """Delete a trading bot"""
    try:
        if bot_id not in active_bots:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        bot = active_bots[bot_id]
        await bot.stop()
        del active_bots[bot_id]
        
        return {"message": f"Bot {bot_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders")
async def get_orders():
    """Get order history"""
    try:
        orders = await kucoin_client.get_order_history(limit=50)
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/signals/{symbol}")
async def get_signals(symbol: str):
    """Get combined trading signals"""
    try:
        # Get sentiment and technical analysis
        sentiment_task = sentiment_analyzer.get_combined_sentiment(symbol)
        technical_task = technical_analyzer.analyze(symbol)
        
        sentiment, technical = await asyncio.gather(sentiment_task, technical_task)
        
        # Combine into signal format
        signal = {
            "id": f"signal_{symbol}_{int(datetime.now().timestamp())}",
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "sentiment": sentiment,
            "technical": technical,
            "combined_score": 0
        }
        
        # Calculate combined score
        if 'combined_sentiment_score' in sentiment and 'signals' in technical:
            sentiment_score = sentiment['combined_sentiment_score']
            technical_strength = technical['signals'].get('strength', 0)
            signal['combined_score'] = (sentiment_score * 0.4) + (technical_strength * 0.6)
        
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)