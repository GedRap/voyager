from backtesting.Market import Market
from backtesting.Order import Order
from backtesting.Parser.CSVOrderParser import CSVOrderParser
from backtesting.Portfolio import Portfolio
import matplotlib.pyplot as plt
import pylab

#A simple program used to run and play around with
#Portfolio and Market
#Plots value of all holdings

market = Market(["AAPL","IBM"],"2011-01-01","2011-01-31")
portfolio = Portfolio(market, 1000000)

order_parser = CSVOrderParser("test/data/SimpleOrdersFile.csv")
order_parser.parse()

for order in order_parser.get_parsed_orders():
    portfolio.add_order(order)

portfolio.execute()

figure = plt.figure()

figure.axes.append(portfolio.holdings_value_sum.plot())

pylab.show()