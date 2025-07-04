#!/usr/bin/env python3
"""
Main script to run the crypto trading bot
"""
import asyncio
import logging
import signal
import sys
import os
from typing import Dict, List
# Add parent directory to path to import api_server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_server import app
from config import Config
import uvicorn

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TradingBotManager:
    def __init__(self):
        self.running = True
        
    async def start_api_server(self):
        """Start the FastAPI server"""
        config = uvicorn.Config(
            app, 
            host=Config.API_HOST, 
            port=Config.API_PORT,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    async def run(self):
        """Main run loop"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info("Starting Crypto Trading Bot Manager")
        logger.info(f"API Server will be available at http://{Config.API_HOST}:{Config.API_PORT}")
        
        try:
            # Start the API server
            await self.start_api_server()
        except Exception as e:
            logger.error(f"Error running bot manager: {e}")
        finally:
            logger.info("Bot manager stopped")

def main():
    """Main entry point"""
    manager = TradingBotManager()
    
    try:
        asyncio.run(manager.run())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()