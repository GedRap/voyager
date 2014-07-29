import unittest
from pandas import *

from backtesting.Order import Order
from backtesting.Portfolio import Portfolio
from backtesting.Market import Market

class PortfolioTest(unittest.TestCase):
    def setUp(self):
        self.date_range = date_range('1/1/2011', periods=30, freq='D')
        self.ts = Series(0, index=self.date_range)

        start_date = datetime(2011, 1, 1)
        end_date = datetime(2011, 12, 31)

        self.market = Market(["AAPL","IBM"],start_date,end_date)
        self.portfolio = Portfolio(self.market, 1000000)
        self.buy_aapl_order = Order(self.market, "2011-01-10", "AAPL", "Buy", 100)
        self.buy_ibm_order = Order(self.market, "2011-01-11", "IBM", "Buy", 15)
        self.sell_aapl_order = Order(self.market, "2011-01-12", "AAPL", "Sell", 50)
        self.sell_ibm_order = Order(self.market, "2011-01-14", "IBM", "Sell", 15)

    def test_sort_orders(self):
        self.portfolio.orders.append(self.buy_aapl_order)
        self.portfolio.orders.append(self.sell_ibm_order)
        self.portfolio.orders.append(self.sell_aapl_order)

        self.portfolio.sort_executed_orders()

        self.assertEqual(self.portfolio.orders[0].symbol, self.buy_aapl_order.symbol)
        self.assertEqual(self.portfolio.orders[0].type, self.buy_aapl_order.type)
        self.assertEqual(self.portfolio.orders[1].type, self.sell_aapl_order.type)
        self.assertEqual(self.portfolio.orders[1].symbol, self.sell_aapl_order.symbol)
        self.assertEqual(self.portfolio.orders[2].symbol, self.sell_ibm_order.symbol)

    def test_execute_on_cash_ts(self):
        #assert initial amount
        self.assertEqual(self.portfolio.cash_ts["2011-01-07"],1000000)

        self.portfolio.update_cash_with_order(self.buy_aapl_order)
        self.assertEqual(self.portfolio.cash_ts["2011-01-11"],965901)

        self.portfolio.update_cash_with_order(self.buy_ibm_order)
        self.assertEqual(self.portfolio.cash_ts["2011-01-12"],963755)

        self.portfolio.update_cash_with_order(self.sell_aapl_order)
        self.assertEqual(self.portfolio.cash_ts["2011-01-14"],980902)

    # This case is more of an integration test,
    # its components were tested separately
    def test_process_day(self):
        date0110 = datetime(2011,1,10,23) # buy aapl
        date0111 = datetime(2011,1,11,23) # buy ibm
        date0112 = datetime(2011,1,12,23) # sell aapl
        date0113 = datetime(2011,1,13,23) # no orders on this
        date0114 = datetime(2011,1,14,23) # sell ibm

        self.add_all_orders()

        self.assertEqual(self.get_long_holding("AAPL"), 0)

        orders = self.portfolio.process_up_to_date(date0110)
        self.assertEqual(self.get_long_holding("AAPL"), 100)
        self.assertEqual(self.get_long_holding("IBM"), 0)

        self.portfolio.process_up_to_date(date0111)
        self.assertEqual(self.get_long_holding("AAPL"), 100)
        self.assertEqual(self.get_long_holding("IBM"), 15)

        self.portfolio.process_up_to_date(date0112)
        self.assertEqual(self.get_long_holding("AAPL"), 50)
        self.assertEqual(self.get_long_holding("IBM"), 15)

        self.portfolio.process_up_to_date(date0113)
        self.assertEqual(self.get_long_holding("AAPL"), 50)
        self.assertEqual(self.get_long_holding("IBM"), 15)

        self.portfolio.process_up_to_date(date0114)
        self.assertEqual(self.get_long_holding("AAPL"), 50)
        self.assertEqual(self.get_long_holding("IBM"), 0)

    #helper method
    def add_all_orders(self):
        self.portfolio.add_future_order(self.buy_aapl_order) #100
        self.portfolio.add_future_order(self.buy_ibm_order) #15
        self.portfolio.add_future_order(self.sell_aapl_order) #-50
        self.portfolio.add_future_order(self.sell_ibm_order) #-15

    def get_long_holding(self, symbol):
        position_long = self.portfolio.holding.POSITION_LONG
        return self.portfolio.holding.get_latest_holding_amount(position_long, symbol)
if __name__ == '__main__':
    unittest.main()