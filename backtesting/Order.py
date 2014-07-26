import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import time

#Holds data related to order
#Executes order on a given timeseries
class Order:
    TYPE_BUY = "Buy"
    TYPE_SELL = "Sell"

    def __init__(self, market, timestamp, symbol, type, quantity):
        """
        Populates Order instance with initial data

        Parameters:
        market - Market object, where related stock's prices can be retrieved
        timestamp - Date in YYYY-mm-dd when to execute the order (closing price
        will be used by default)
        symbol - Stock symbol (e.g. GOOG)
        type - Buy/Sell
        quantity - Number of shares to buy/sell
        """
        self.market = market
        timestamp += " 16:00:00"
        self.timestamp = dt.datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")
        self.symbol = symbol
        self.type = type
        self.quantity = quantity

    def update_number_of_shares_held(self, ts):
        """
        Execute order on time series, which stores number of
        shares held on a given timestamp
        """
        if self.type == self.TYPE_BUY:
            ts[self.timestamp:] = ts[self.timestamp] + self.quantity
        if self.type == self.TYPE_SELL:
            ts[self.timestamp:] = ts[self.timestamp] - self.quantity

        return ts


    def to_string(self):
        """
        Return string with Order's data, useful for debugging
        """
        return self.symbol + ", " + self.type + ", " + str(self.quantity)