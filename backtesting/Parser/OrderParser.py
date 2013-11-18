import datetime as dt
from backtesting.Order import Order

#Abstract class for Order Parser implementations
class OrderParser(object):

    def __init__(self):
        """
        Initialize generic parser structure
        """
        self.parsed_orders = []
        self.symbols_traded = set()
        #Timestamps for the first and the last trade because we need to
        #have a range for retrieving historical data
        self.first_trade_ts = None
        self.last_trade_ts = None


    def parse(self):
        """
        Should be implemented by a child class
        """
        raise NotImplementedError("Should be implemented in the child class")


    def add_parsed_order(self, order):
        """
        Add an order to list of parsed orders

        order - Instance of Order
        """
        if not isinstance(order, Order):
            raise TypeError("Instance of Order must be given")

        self.parsed_orders.append(order)

        return True

    def get_parsed_orders(self):
        """
        Return a list of parsed orders
        """
        return self.parsed_orders

    def add_symbol_traded(self, symbol):
        """
        Add a symbol (ticker) to a set of symbols traded
        """
        self.symbols_traded.add(symbol)

    def get_symbols_traded(self):
        """
        Get a set of symbols traded
        """
        return self.symbols_traded

    def get_dates_range(self):
        """
        Get the datetime objects of first and last orders (in the asceding
        order of timestamp)
        """
        return (self.first_trade_ts, self.last_trade_ts)

    def check_timestamp(self, timestamp):
        """
        Assert a timestamp if it's a new first_trade or last_trade timestamp

        timestamp - String timestamp, in %Y-%m-%d format
        """
        timestamp += " 16:00:00"
        timestamp_obj = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        if self.first_trade_ts is None:
            self.first_trade_ts = timestamp_obj

        else:
            if self.first_trade_ts > timestamp_obj:
                self.first_trade_ts = timestamp_obj

        if self.last_trade_ts is None:
            self.last_trade_ts = timestamp_obj
        else:
            if self.last_trade_ts < timestamp_obj:
                self.last_trade_ts = timestamp_obj


