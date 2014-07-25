import unittest

from backtesting.Parser.OrderParser import OrderParser

class OrderParserTest(unittest.TestCase):
    def setUp(self):
        self.order_parser = OrderParser()

    def test_add_order(self):
        self.assertRaises(TypeError, self.order_parser, (None))