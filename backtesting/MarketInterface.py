class MarketInterface:
    def get_symbol_price(self, symbol, timestamp, price_type):
        raise NotImplementedError("get_symbol_price must be implemented in child class")