import unittest

from backtesting.Order import Order

from backtesting.Parser.CSVOrderParser import CSVOrderParser

class CSVOrderParserTest(unittest.TestCase):

    def test_parse_file(self):
        parser = CSVOrderParser("data/SimpleOrdersFile.csv")
        parser.parse()

        orders = parser.get_parsed_orders()

        symbols = parser.get_symbols_traded()

        self.assertEqual(len(symbols), 2)
        self.assertTrue("AAPL" in symbols)
        self.assertTrue("IBM" in symbols)

        first_trade, last_trade = parser.get_dates_range()
        self.assertEqual("2011-01-10", first_trade.strftime("%Y-%m-%d"))
        self.assertEqual("2011-01-13", last_trade.strftime("%Y-%m-%d"))

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