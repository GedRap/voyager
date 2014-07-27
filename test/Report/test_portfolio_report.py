import unittest
from backtesting.Order import Order
from backtesting.Parser.CSVOrderParser import CSVOrderParser
from backtesting.Portfolio import Portfolio
from backtesting.Market import Market
from backtesting.Report.PortfolioReport import PortfolioReport

class PortfolioReportTest(unittest.TestCase):
    def setUp(self):
        parser = CSVOrderParser("data/SimpleOrdersFile.csv")
        parser.parse()
        orders = parser.get_parsed_orders()
        start_date, end_date = parser.get_dates_range()

        self.market = Market(parser.get_symbols_traded(),start_date,end_date)
        self.portfolio = Portfolio(self.market, 1000000)
        for order in orders:
            self.portfolio.add_future_order(order)

        self.portfolio.calculate_number_of_shares_held()
        self.portfolio.calculate_portfolio_value()

        self.portfolio_report = PortfolioReport(self.portfolio)

    def test_get_total_return(self):
        self.assertEqual(self.portfolio_report.get_total_return(), -61900)

    def test_get_return(self):
        self.assertEqual(self.portfolio_report.get_return(), -0.1267)