from backtesting.Parser.OrderParser import OrderParser
from backtesting.Order import Order
import pandas as pd

# OrderParser implementation, reads from CSV files
class CSVOrderParser(OrderParser):
    def __init__(self, filename):
        """
        Save file name and set up parent
        """
        self.filename = filename

        super(CSVOrderParser, self).__init__()

    def parse(self):
        """
        Parse CSV file and create Order instances. Also generates set of
        symbols traded and trades timestamps range
        """
        parsed_df = pd.read_csv(self.filename)

        for index, row in parsed_df.T.iteritems():
            timestamp = str(row['year']) + "-" + str(row['month']) + "-" + str(row['day'])
            new_order = Order(None, timestamp, row['symbol'], row['type'], row['shares'])

            super(CSVOrderParser,self).add_parsed_order(new_order)
            super(CSVOrderParser,self).add_symbol_traded(row['symbol'])
            super(CSVOrderParser,self).check_timestamp(timestamp)

        return True