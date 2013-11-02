from backtesting.Market import Market
from backtesting.Order import Order
from backtesting.Portfolio import Portfolio
import matplotlib.pyplot as plt
import pylab

#A simple program used to run and play around with
#Portfolio and Market
#Plots value of all holdings

market = Market(["AAPL","IBM"],"2011-01-01","2011-01-31")
portfolio = Portfolio(market, 1000000)
buy_aapl_order = Order(market, "2011-01-10", "AAPL", "Buy", 100)
buy_ibm_order = Order(market, "2011-01-11", "IBM", "Buy", 100)
sell_aapl_order = Order(market, "2011-01-12", "AAPL", "Sell", 50)
sell_ibm_order = Order(market, "2011-01-14", "IBM", "Sell", 100)
sell_aapl_order1 = Order(market, "2011-01-28", "AAPL", "Sell", 50)

portfolio.add_order(buy_ibm_order)
portfolio.add_order(buy_aapl_order)
portfolio.add_order(sell_ibm_order)
portfolio.add_order(sell_aapl_order)
portfolio.add_order(sell_aapl_order1)

portfolio.execute()

figure = plt.figure()

figure.axes.append(portfolio.holdings_value_sum.plot())

pylab.show()