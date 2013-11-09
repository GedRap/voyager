from backtesting.Parser.OrderParser import OrderParser
from backtesting.Order import Order
import pandas as pd

class CSVOrderParser(OrderParser):
    def __init__(self, filename):
        self.filename = filename

        super(CSVOrderParser, self).__init__()

    def parse(self):
        parsed_df = pd.read_csv(self.filename)

        for index, row in parsed_df.T.iteritems():
            timestamp = str(row['year']) + "-" + str(row['month']) + "-" + str(row['day'])
            new_order = Order(None, timestamp, row['symbol'], row['type'], row['shares'])

            super(CSVOrderParser,self).add_parsed_order(new_order)

        return True