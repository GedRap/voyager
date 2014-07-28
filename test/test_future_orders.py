import unittest
from pandas import *
from datetime import *

from backtesting.Order import Order
from backtesting.FutureOrders import FutureOrders

class FutureOrdersTest(unittest.TestCase):
    def setUp(self):
        self.future_orders = FutureOrders()

        self.order1 = Order(None, "2014-07-27", "AAPL", Order.TYPE_SHORT_OPEN, 10)
        self.order2 = Order(None, "2014-07-27", "IBM", Order.TYPE_BUY, 5)
        self.order3 = Order(None, "2014-07-29", "GOOG", Order.TYPE_SELL, 20)

    def test_add_order(self):

        self.assertEqual(len(self.future_orders.orders), 0)

        self.future_orders.add_order(self.order1)
        self.future_orders.add_order(self.order2)
        self.future_orders.add_order(self.order3)

        self.assertEqual(len(self.future_orders.orders), 3)

    def test_get_orders_to_date_dont_remove(self):

        self.future_orders.add_order(self.order1)
        self.future_orders.add_order(self.order2)
        self.future_orders.add_order(self.order3)

        now = datetime(2014, 7, 10, 17)
        order = self.future_orders.get_orders_to_date(now, False)
        self.assertEqual(len(order), 0)
        self.assertEqual(len(self.future_orders.orders), 3)

        now = datetime(2014, 7, 27, 17)
        orders = self.future_orders.get_orders_to_date(now, False)
        self.assertEqual(len(orders), 2)
        self.assertEqual(len(self.future_orders.orders), 3)
        self.assertTrue(orders[0].symbol == "AAPL" or orders[1].symbol == "IBM", "Wrong orders returned")

    def test_get_orders_to_date_remove(self):

        self.future_orders.add_order(self.order1)
        self.future_orders.add_order(self.order2)
        self.future_orders.add_order(self.order3)

        now = datetime(2014, 7, 10, 17)
        order = self.future_orders.get_orders_to_date(now)
        self.assertEqual(len(order), 0)
        self.assertEqual(len(self.future_orders.orders), 3)

        now = datetime(2014, 7, 27, 17)
        orders = self.future_orders.get_orders_to_date(now)
        self.assertEqual(len(orders), 2)
        self.assertEqual(len(self.future_orders.orders), 1)
        self.assertTrue(orders[0].symbol == "AAPL" or orders[1].symbol == "IBM", "Wrong orders returned")