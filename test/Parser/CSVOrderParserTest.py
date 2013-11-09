import unittest

from backtesting.Order import Order

from backtesting.Parser.CSVOrderParser import CSVOrderParser

class CSVOrderParserTest(unittest.TestCase):

    def test_parse_file(self):
        parser = CSVOrderParser("data/SimpleOrdersFile.csv")
        parser.parse()

        orders = parser.get_parsed_orders()

        self.assertEqual(len(orders), 3)

        self.assertEqual(orders[0].symbol, "AAPL")
        self.assertEqual(orders[0].type, Order.TYPE_BUY)
        self.assertEqual(orders[0].quantity,1500)
        self.assertEqual(orders[0].timestamp.strftime("%Y-%m-%d %H:%M:%S"),"2011-01-10 16:00:00")

        self.assertEqual(orders[1].symbol, "AAPL")
        self.assertEqual(orders[1].type, Order.TYPE_SELL)
        self.assertEqual(orders[1].quantity,1500)
        self.assertEqual(orders[1].timestamp.strftime("%Y-%m-%d %H:%M:%S"),"2011-01-13 16:00:00")

        self.assertEqual(orders[2].symbol, "IBM")
        self.assertEqual(orders[2].type, Order.TYPE_BUY)
        self.assertEqual(orders[2].quantity,4000)
        self.assertEqual(orders[2].timestamp.strftime("%Y-%m-%d %H:%M:%S"),"2011-01-13 16:00:00")