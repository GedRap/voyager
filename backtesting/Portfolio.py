import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu

from pandas import *

#Holds portfolio related data such as cash available and assets held
#Performs calculations related to orders and assets (e.g. value of all
#assets at a given time
class Portfolio:
    def __init__(self, market, cash):
        """
        Initialize the portfolio

        Creates empty data frames, time series and other data structures
        which will be populated during the execution
        """
        self.market = market

        #List of timestamps with dates when market is open
        self.trading_days = self.market.get_trading_days()

        #Initial cash
        self.cash = cash

        #List of orders to be executed
        self.orders = []

        #Set of traded symbols
        self.traded_symbols = set()

        #Timeseries, which stores cash balance
        self.cash_ts = pd.Series(cash, index=self.trading_days)

        #Products of number of shares and the stock price at any given date
        self.holdings_value = DataFrame(self.market.get_trading_days_ts())
        #Total value of all assets held at given date
        self.holdings_value_sum = pd.Series(0,index=self.trading_days)
        #Number of shares held at a given date
        self.holdings_shares = DataFrame(self.market.get_trading_days_ts())

    def add_order(self, order):
        """Add order to the list of orders to be executed"""
        self.orders.append(order)


    def sort_orders(self):
        """Sort orders by timestamp in the ascending order"""
        self.orders.sort(key=lambda x: x.timestamp, reverse=False)


    def execute_orders(self):
        """
        'execute' all in the portfolio orders

        Populates holdings_shares data frame, which stores number
        of shares held for given symbol and given time
        """
        self.sort_orders()

        for order in self.orders:
            if not order.symbol in self.holdings_shares:
                #symb_time_series = Series(0, index=self.market.get_trading_days())
                self.holdings_shares[order.symbol] = 0
                self.traded_symbols.add(order.symbol)

            symb_time_series = self.holdings_shares[order.symbol]
            self.holdings_shares[order.symbol] = order.execute_on_time_series(symb_time_series)
            self.execute_order_on_cash_ts(order)


    def execute_order_on_cash_ts(self, order, price='close'):
        """
        Execute order on cash time series

        Calculates the value of the order and updates the time
        series of cash balance respectively
        """
        quantity = order.quantity
        sharePrice = self.market.get_stock_price(order.symbol,order.timestamp,price)
        orderValue = quantity * sharePrice

        if order.type == order.TYPE_BUY:
            orderValue = orderValue * -1

        self.cash_ts[order.timestamp:] = self.cash_ts[order.timestamp] + orderValue

    def get_holding_value(self,symbol,timestamp):
        """
        Get a holding value for any given date
        """
        return self.holdings_value[symbol][timestamp]

    def calculate_holdings_value(self):
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


    def calculate_holdings_value_sum(self):
        """
        Populate a time series, which holds the value of all
        holdings (shares) at the given date
        """
        for index, series in self.holdings_value.iterrows():
            self.holdings_value_sum[index] = series.sum()


    def execute(self):
        """
        Completely execute  all orders. Only this execution function should be
        called from outside the class.

        It does:
        1) Populates time series with number of shares held for every share
        2) Calculates cash balance for every date
        3) Calculates holdings value, for every share
        4) Sums all holdings values for any given date and saves as a
        time series
        """
        self.execute_orders()
        self.calculate_holdings_value()
        self.calculate_holdings_value_sum()
