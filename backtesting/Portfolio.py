import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
from backtesting.FutureOrders import FutureOrders
from backtesting.Holding import Holding

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

        #List of orders executed
        self.orders = []

        #List of orders to be executed in the future
        self.future_orders = FutureOrders()

        #Timeseries, which stores cash balance
        self.cash_ts = pd.Series(cash, index=self.trading_days)

        self.holding = Holding(self.trading_days)

        #Overall portfolio value (holdings+cash)
        self.portfolio_value = pd.Series(0, index=self.trading_days)

    def add_future_order(self, order):
        """Add order to the list of orders to be executed"""
        self.future_orders.add_order(order)


    def sort_executed_orders(self):
        """Sort orders by timestamp in the ascending order"""
        self.orders.sort(key=lambda x: x.timestamp, reverse=False)


    def update_cash_with_order(self, order, price='close'):
        """
        Execute order on cash time series

        Calculates the value of the order and updates the time
        series of cash balance respectively
        """
        quantity = order.quantity
        sharePrice = self.market.get_stock_price(order.symbol,order.timestamp,price)
        order_value = quantity * sharePrice

        if order.type == order.TYPE_BUY or order.type == order.TYPE_SHORT_OPEN:
            order_value = order_value * -1

        self.cash_ts[order.timestamp:] = self.cash_ts[order.timestamp] + order_value
        self.cash += order_value


    # @todo replace
    def calculate_holdings_value_sum(self):
        """
        Populate a time series, which holds the value of all
        holdings (shares) at the given date
        """
        for index, series in self.holdings_value.iterrows():
            self.holdings_value_sum[index] = series.sum()

    # @todo replace
    def calculate_portfolio_value(self):
        """
        Calculate total portfolio value (holdings+cash) and save it in time
        series
        """
        self.portfolio_value = self.holdings_value_sum + self.cash_ts

    def process_day(self, day):
        orders_for_day = self.future_orders.get_orders_to_date(day)

        if len(orders_for_day):
            for order in orders_for_day:
                self.update_cash_with_order(order)
                self.holding.update_with_order(order)

        return orders_for_day
