from backtesting.Order import Order

#Abstract class for Order Parser implementations
class OrderParser(object):
    def __init__(self):
        self.parsed_orders = []

    def add_parsed_order(self, order):
        if not isinstance(order):
            raise TypeError("Instance of Order must be given")

        self.parsed_orders.append(order)

        return True