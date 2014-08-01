import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

#Market entity used to get market prices for given stock at a given time
class StockMarket:
    def __init__(self, symbols, start_date, end_date):
        """
        Initialize Market object by storing some basic data

        Parameters:
        symbols - List of symbols traded
        start_date - datetime object, used as a time range when loading
        historical historical_data
        end_date - datetime object, used as a time range when loading
        historical data
        """

        self.dt_start = start_date
        self.dt_end = end_date

        self.ldt_timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours=16))

        self.symbols = symbols
        self.historical_data_loaded = False

    def load_historical_data(self):
        """
        Load historical data from Yahoo
        """
        self.dataobj = da.DataAccess('Yahoo')
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        ldf_data = self.dataobj.get_data(self.ldt_timestamps, self.symbols, ls_keys)
        self.d_data = dict(zip(ls_keys, ldf_data))
        self.historical_data_loaded = True

    def check_if_data_loaded(self):
        """
        Check if the historical data is loaded, do it if
        it's not yet
        """
        if not self.historical_data_loaded:
            self.load_historical_data()

    def get_stock_price(self, symbol, timestamp, price):
        """
        Get stock price for given timestamp

        symbol - Stock ticker, e.g. GOOG
        timestamp - Date/time
        price - Price type (open, high, low, close)
        """
        self.check_if_data_loaded()
        values = self.d_data[price]

        return values[symbol].ix[timestamp]

    def get_trading_days(self):
        """
        List of trading days in NYSE in the range of start and end dates given
        when initializing the market object
        """
        return self.ldt_timestamps

    def get_trading_days_ts(self):
        """
        Create a timeseries using trading days as index, 0 as default value
        """
        days = self.get_trading_days()
        ts = pd.Series(0, index=days)

        return ts

    def get_symbol_ts(self, symbol, price):
        """
        Get time series with prices for given symbol

        symbol - Stock symbol, e.g. GOOG
        price - Price type (open, high, low, close)
        """
        return self.d_data[price][symbol]

    def print_daily_prices(self, symbol, timestamp):
        """
        Print daily prices for the given symbol at given date
        """
        print timestamp
        print "Open " + str(self.d_data['open'][symbol].ix[timestamp])
        print "High " + str(self.d_data['high'][symbol].ix[timestamp])
        print "Low " + str(self.d_data['low'][symbol].ix[timestamp])
        print "Close " + str(self.d_data['close'][symbol].ix[timestamp])
        print "Volume " + str(self.d_data['volume'][symbol].ix[timestamp])
        print "Actual close " + str(self.d_data['actual_close'][symbol].ix[timestamp])
