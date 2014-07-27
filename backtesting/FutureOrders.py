from backtesting.Order import Order

class FutureOrders:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        if not isinstance(order, Order):
            raise NotImplementedError("Only instances of Order are supported")
        self.orders.append(order)

    def get_orders_to_date(self, timestamp, remove=True):
        orders_to_date = []

        if len(self.orders) > 0:
            for order in self.orders:
                if order.timestamp <= timestamp:
                    orders_to_date.append(order)

            if remove:
                self.orders = list(set(self.orders) - set(orders_to_date))

        return orders_to_date