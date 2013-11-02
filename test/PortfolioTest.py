import unittest
from pandas import *

from backtesting.Order import Order
from backtesting.Portfolio import Portfolio
from backtesting.Market import Market

class PortfolioTest(unittest.TestCase):
    def setUp(self):
        self.date_range = date_range('1/1/2011', periods=30, freq='D')
        self.ts = Series(0, index=self.date_range)

        self.market = Market(["AAPL","IBM"],"2011-01-01","2011-12-31")
        self.portfolio = Portfolio(self.market, 1000000)
        self.buy_aapl_order = Order(self.market, "2011-01-10", "AAPL", "Buy", 100)
        self.buy_ibm_order = Order(self.market, "2011-01-11", "IBM", "Buy", 15)
        self.sell_aapl_order = Order(self.market, "2011-01-12", "AAPL", "Sell", 50)
        self.sell_ibm_order = Order(self.market, "2011-01-14", "IBM", "Sell", 15)

    def test_add_orders(self):
        self.portfolio.add_order(self.buy_aapl_order)
        self.assertEqual(len(self.portfolio.orders), 1)

    def test_sort_orders(self):
        self.portfolio.add_order(self.buy_aapl_order)
        self.portfolio.add_order(self.sell_ibm_order)
        self.portfolio.add_order(self.sell_aapl_order)

        self.portfolio.sort_orders()

        self.assertEqual(self.portfolio.orders[0].symbol, self.buy_aapl_order.symbol)
        self.assertEqual(self.portfolio.orders[0].type, self.buy_aapl_order.type)
        self.assertEqual(self.portfolio.orders[1].type, self.sell_aapl_order.type)
        self.assertEqual(self.portfolio.orders[1].symbol, self.sell_aapl_order.symbol)
        self.assertEqual(self.portfolio.orders[2].symbol, self.sell_ibm_order.symbol)

    def test_execute_on_cash_ts(self):
        #assert initial amount
        self.assertEqual(self.portfolio.cash_ts["2011-01-07"],1000000)

        self.portfolio.execute_order_on_cash_ts(self.buy_aapl_order)
        self.assertEqual(self.portfolio.cash_ts["2011-01-11"],965901)

        self.portfolio.execute_order_on_cash_ts(self.buy_ibm_order)
        self.assertEqual(self.portfolio.cash_ts["2011-01-12"],963755)

        self.portfolio.execute_order_on_cash_ts(self.sell_aapl_order)
        self.assertEqual(self.portfolio.cash_ts["2011-01-14"],980902)

    def test_execute_orders(self):
        self.add_all_orders()
        self.portfolio.execute_orders()

        apple_ts = self.portfolio.holdings_shares["AAPL"]

        ibm_ts = self.portfolio.holdings_shares["IBM"]

        self.assertEqual(apple_ts["2011-01-04"],0)
        self.assertEqual(apple_ts["2011-01-04"],0)
        self.assertEqual(apple_ts["2011-01-11"],100)
        self.assertEqual(ibm_ts["2011-01-10"],0)
        self.assertEqual(ibm_ts["2011-01-12"],15)
        self.assertEqual(apple_ts["2011-01-14"],50)

    def test_calculate_holdings_value(self):
        self.add_all_orders()
        self.portfolio.execute_orders()
        self.portfolio.calculate_holdings_value()

        self.assertEqual(self.portfolio.get_holding_value("AAPL","2011-01-04"),0)
        self.assertEqual(self.portfolio.get_holding_value("AAPL","2011-01-11"),34018)
        self.assertEqual(self.portfolio.get_holding_value("AAPL","2011-01-14"),17349.5)

        self.assertEqual(self.portfolio.get_holding_value("IBM","2011-01-04"),0)
        self.assertEqual(self.portfolio.get_holding_value("IBM","2011-01-13"),2168.25)

        self.portfolio.get_holding_value("IBM","2011-01-18")
        self.assertEqual(self.portfolio.get_holding_value("IBM","2011-01-18"),0)

    #helper method
    def add_all_orders(self):
        self.portfolio.add_order(self.buy_ibm_order)
        self.portfolio.add_order(self.buy_aapl_order)
        self.portfolio.add_order(self.sell_aapl_order)
        self.portfolio.add_order(self.sell_ibm_order)

if __name__ == '__main__':
    unittest.main()