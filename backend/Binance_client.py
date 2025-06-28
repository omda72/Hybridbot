import ccxt
from config import Config

class BinanceClient:
    def __init__(self):
        self.client = ccxt.binance({
            'apiKey': Config.BINANCE_API_KEY,
            'secret': Config.BINANCE_API_SECRET,
        })

    def get_balance(self):
        return self.client.fetch_balance()

    def get_ticker(self, symbol):
        return self.client.fetch_ticker(symbol)

    def create_order(self, symbol, side, amount):
        return self.client.create_order(symbol, 'market', side, amount)
