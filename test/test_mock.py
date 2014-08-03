# Example of patching / mocking
# @todo remove once I learn them :)
from mock import MagicMock, patch
from backtesting.StockMarket import StockMarket
import datetime

# returns different values
returns = [1,2]
def side_effects():
    result = returns.pop(0)
    return result

mock = MagicMock(side_effect = side_effects)
real = StockMarket(["IBM"], datetime.datetime(2011,1,1), datetime.datetime(2012,1,1))
real.get_symbol_price = mock

assert real.get_symbol_price() == 1
assert real.get_symbol_price() == 2

exit()

# always returns the same value
with patch('backtesting.StockMarket') as mock:
    instance = mock.return_value
    instance.get_symbol_price.return_value = 1
    real = backtesting.StockMarket(["IBM"], datetime.datetime(2011,1,1), datetime.datetime(2012,1,1))
    result = real.get_symbol_price()
    print result
    assert result == 1

