import ccxt
from config import Config

class CoinbaseClient:
    def __init__(self):
        self.client = ccxt.coinbasepro({
            'apiKey': Config.COINBASE_API_KEY,
            'secret': Config.COINBASE_API_SECRET,
            'password': Config.COINBASE_API_PASSPHRASE,
        })

    def get_balance(self):
        return self.client.fetch_balance()

    def get_ticker(self, symbol):
        return self.client.fetch_ticker(symbol)

    def create_order(self, symbol, side, amount):
        return self.client.create_order(symbol, 'market', side, amount)

