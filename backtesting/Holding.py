import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
from backtesting.FutureOrders import FutureOrders

from pandas import *

class Holding:
    POSITION_LONG = "long"
    POSITION_SHORT = "short"

    def __init__(self, trading_days):
        self.short_holdings = {}
        self.long_holdings = {}

        self.trading_days = trading_days

        #Products of number of shares and the stock price at any given date
        self.long_holdings_value = DataFrame(self.trading_days)
        #Total value of all assets held at given date
        self.long_holdings_value_sum = pd.Series(0,index=self.trading_days)
        #Number of shares held at a given date
        self.long_holdings_shares = DataFrame(self.trading_days)

        #Analogue to the ones listed above just for short orders
        self.short_holdings_value = DataFrame(self.trading_days)
        self.short_holdings_value_sum = pd.Series(0, index=self.trading_days)
        self.short_holdings_shares = DataFrame(self.trading_days)


    def update_with_order(self, order):
        if order.is_short():
            self.update_holding(order.symbol, self.POSITION_SHORT, order.quantity)
        else:
            self.update_holding(order.symbol, self.POSITION_LONG, order.quantity)

        self.calculate_holdings_on_dataframes(order)

    def calculate_holdings_on_dataframes(self, order):
        if order.is_short():
            ts = self.short_holdings_shares[order.symbol]
            self.short_holdings_shares[order.symbol] = self.update_number_of_shares_held(order, ts)
        else:
            ts = self.long_holdings_shares[order.symbol]
            self.long_holdings_shares[order.symbol] = self.update_number_of_shares_held(order, ts)



    def update_number_of_shares_held(self, order, ts):
        """
        Execute order on time series, which stores number of
        shares held on a given timestamp
        """
        if order.type == order.TYPE_BUY or order.type == order.TYPE_SHORT_OPEN:
            ts[order.timestamp:] = ts[order.timestamp] + order.quantity
        if order.type == order.TYPE_SELL or order.type == order.TYPE_SHORT_CLOSE:
            ts[order.timestamp:] = ts[order.timestamp] - order.quantity

        return ts

    def update_holding(self, symbol, position, amount):
        if position != self.POSITION_LONG and position != self.POSITION_SHORT:
            raise NotImplementedError("Position " + position + " is not supported")

        if position == self.POSITION_SHORT:
            if not symbol in self.short_holdings:
                self.short_holdings[symbol] = amount
            else:
                self.short_holdings[symbol] += amount

        if position == self.POSITION_LONG:
            if not symbol in self.long_holdings:
                self.long_holdings[symbol] = amount
            else:
                self.long_holdings[symbol] += amount

    def get_holding_amount(self, position, symbol):
        amount = 0

        if position == self.POSITION_LONG:
            if symbol in self.long_holdings:
                amount = self.long_holdings[symbol]

        if position == self.POSITION_SHORT:
            if symbol in self.short_holdings:
                amount = self.short_holdings[symbol]

        return amount

    # @todo refactor to support short orders
    def calculate_holdings_value_for_each_symbol(self):
        """
        Get all holdings (shares in the portfolio) value for every day
        """
        self.market.check_if_data_loaded()

        for symbol in self.traded_symbols:
            #Time series of number of shares held
            shares_held = self.holdings_shares[symbol]
            #Time series of close prices
            stock_prices = self.market.get_symbol_ts(symbol,"close")
            #Compute value by multiplying the price and number
            #of shares for every day
            self.holdings_value[symbol] = (shares_held * stock_prices)