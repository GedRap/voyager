import unittest
from pandas import *
from datetime import *

from backtesting.Order import Order
from backtesting.Portfolio import Portfolio
from backtesting.Market import Market
from backtesting.Holding import Holding

class HoldingTest(unittest.TestCase):
    def setUp(self):
        self.date_range = date_range('1/1/2011', periods=30, freq='D')


        start_date = datetime(2011, 1, 1)
        end_date = datetime(2011, 12, 31)

        self.market = Market(["AAPL","IBM"],start_date,end_date)
        #self.portfolio = Portfolio(self.market, 1000000)
        self.buy_aapl_order = Order(self.market, "2011-01-10", "AAPL", "Buy", 100)
        self.buy_ibm_order = Order(self.market, "2011-01-11", "IBM", "Buy", 15)
        self.sell_aapl_order = Order(self.market, "2011-01-12", "AAPL", "Sell", 50)
        self.sell_ibm_order = Order(self.market, "2011-01-14", "IBM", "Sell", 15)

        self.short_open_aapl = Order(self.market, "2011-01-11", "AAPL", Order.TYPE_SHORT_OPEN, 100)
        self.short_close_appl = Order(self.market, "2011-01-14", "AAPL", Order.TYPE_SHORT_CLOSE, 50)

        self.holding = Holding(self.market.get_trading_days())

        self.ts = Series(0, index=self.market.get_trading_days())

    def test_get_holding_amount_no_data(self):
        amount = self.holding.get_latest_holding_amount(self.holding.POSITION_LONG, "HELLO")
        self.assertEqual(amount, 0)

    def test_update_holding(self):
        position_long = self.holding.POSITION_LONG
        position_short = self.holding.POSITION_SHORT

        self.holding.update_holding("TEST", position_long, 1)
        self.assertEqual(self.holding.get_latest_holding_amount(position_long, "TEST"), 1)

        self.holding.update_holding("TEST", position_long, -1)
        self.assertEqual(self.holding.get_latest_holding_amount(position_long, "TEST"), 0)

        #Try with different symbol
        self.holding.update_holding("HELLO", position_long, 5)
        self.assertEqual(self.holding.get_latest_holding_amount(position_long, "HELLO"), 5)

        self.holding.update_holding("TEST", position_short, 10)
        self.holding.update_holding("TEST", position_short, 20)
        self.assertEqual(self.holding.get_latest_holding_amount(position_short, "TEST"), 30)

        self.holding.update_holding("TEST", position_short, -5)
        self.assertEqual(self.holding.get_latest_holding_amount(position_short, "TEST"), 25)

    def test_update_number_of_shares_held_short(self):
        position_short = self.holding.POSITION_SHORT

        ts = self.holding.update_number_of_shares_held(self.short_open_aapl, self.ts)
        self.assertEqual(ts["2011-01-11"], self.short_open_aapl.quantity)
        self.assertEqual(ts["2011-01-14"], self.short_open_aapl.quantity)
        self.assertEqual(ts["2011-01-03"], 0)

        ts = self.holding.update_number_of_shares_held(self.short_close_appl, ts)
        self.assertEqual(ts["2011-01-14"], 50)
        self.assertEqual(ts["2011-01-20"], 50)
        self.assertEqual(ts["2011-01-11"], 100)
        self.assertEqual(ts["2011-01-03"], 0)

    def test_update_number_of_shares_held_long(self):
        ts = self.holding.update_number_of_shares_held(self.buy_ibm_order, self.ts)
        self.assertEqual(ts["2011-01-03"], 0)
        self.assertEqual(ts["2011-01-11"], self.buy_ibm_order.quantity)
        self.assertEqual(ts["2011-01-20"], self.buy_ibm_order.quantity)

        ts = self.holding.update_number_of_shares_held(self.sell_ibm_order, ts)
        self.assertEqual(ts["2011-01-03"], 0)
        self.assertEqual(ts["2011-01-11"], 15)
        self.assertEqual(ts["2011-01-14"], 0)
        self.assertEqual(ts["2011-01-20"], 0)

    def test_update_with_order(self):
        position_short = self.holding.POSITION_SHORT
        position_long = self.holding.POSITION_LONG

        self.holding.update_with_order(self.short_open_aapl)
        self.holding.update_with_order(self.buy_ibm_order)

        #IBM Long will be tested later
        amount = self.holding.get_holding_for_date(position_short, "AAPL", "2011-01-03")
        self.assertEqual(amount, 0)
        amount = self.holding.get_holding_for_date(position_short, "AAPL", "2011-01-14")
        self.assertEqual(amount, 100)
        amount = self.holding.get_holding_for_date(position_short, "AAPL", "2011-01-20")
        self.assertEqual(amount, 100)

        self.holding.update_with_order(self.sell_ibm_order)
        self.holding.update_with_order(self.short_close_appl)

        amount = self.holding.get_holding_for_date(position_short, "AAPL", "2011-01-03")
        self.assertEqual(amount, 0)
        amount = self.holding.get_holding_for_date(position_short, "AAPL", "2011-01-13")
        self.assertEqual(amount, 100)
        amount = self.holding.get_holding_for_date(position_short, "AAPL", "2011-01-14")
        self.assertEqual(amount, 50)
        amount = self.holding.get_holding_for_date(position_short, "AAPL", "2011-01-20")
        self.assertEqual(amount, 50)

        # Test IBM Long
        amount = self.holding.get_holding_for_date(position_long, "IBM", "2011-01-03")
        self.assertEqual(amount, 0)
        amount = self.holding.get_holding_for_date(position_long, "IBM", "2011-01-11")
        self.assertEqual(amount, 15)
        amount = self.holding.get_holding_for_date(position_long, "IBM", "2011-01-14")
        self.assertEqual(amount, 0)