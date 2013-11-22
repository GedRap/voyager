from __future__ import division
import decimal

from Report import Report

# Class to generate a report for a given portfolio after its
# orders have been executed
class PortfolioReport(Report):
    def __init__(self, portfolio):
        """
        Create PortfolioReport instance

        portfolio - Instance of Portfolio
        """
        self.portfolio = portfolio


    def get_total_return(self):
        """
        Get the total (absolute) return of the portfolio
        """
        first = self.portfolio.portfolio_value[0]
        last = self.portfolio.portfolio_value[len(self.portfolio.portfolio_value)-1]

        total_return = last - first

        return total_return

    def get_return(self):
        """
        Get the return of portfolio, in percentage.
        Returns a decimal number, rounded to 4 places.
        0.1 => 10% and etc.
        """
        first = self.portfolio.portfolio_value[0]
        last = self.portfolio.portfolio_value[len(self.portfolio.portfolio_value)-1]

        precise = decimal.Decimal((last / first) - 1)

        return round(precise, 4)
