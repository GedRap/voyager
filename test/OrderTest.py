import unittest
from pandas import *

from backtesting.Order import Order

class OrderTest(unittest.TestCase):
    def setUp(self):
        self.date_range = date_range('1/1/2011 16:00:00', periods=10, freq='D')
        self.ts = Series(0, index=self.date_range)
        self.buy_order = Order(None, "2011-01-02", "AAPL", "Buy", 100)
        self.sell_order = Order(None, "2011-01-03", "AAPL", "Sell", 50)

    def test_buy_order(self):
        new_ts = self.buy_order.execute_on_time_series(self.ts)

        self.assertEqual(self.ts["2011-01-01"],0)
        self.assertEqual(self.ts["2011-01-02"],100)
        self.assertEqual(self.ts["2011-01-03"],100)

    def test_buy_and_sell(self):
        new_ts = self.buy_order.execute_on_time_series(self.ts)
        new_ts = self.sell_order.execute_on_time_series(new_ts)
        self.assertEqual(self.ts["2011-01-01"],0)
        self.assertEqual(self.ts["2011-01-02"],100)
        self.assertEqual(self.ts["2011-01-03"],50)
        self.assertEqual(self.ts["2011-01-04"],50)

if __name__ == '__main__':
    unittest.main()