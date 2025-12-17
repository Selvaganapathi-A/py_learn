from base import NewOrder, OrderState, PaidOrder, ShippedOrder  # noqa: F401


class Order:
    def __init__(self):
        self.state: OrderState = NewOrder()

    def pay(self):
        self.state.pay(self)

    def ship(self):
        self.state.ship(self)


def main():
    order = Order()
    order.pay()
    # order.pay() # ! raise Exception as Order already paid.
    order.ship()
    # order.pay() # ! raise Exception as Order already shipped.


if __name__ == '__main__':
    main()
