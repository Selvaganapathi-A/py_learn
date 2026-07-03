from abc import ABC, abstractmethod
from typing import NoReturn, Protocol


class OrderProtocol(Protocol):
    state: OrderState


class OrderState(ABC):
    @abstractmethod
    def ship(self, order: OrderProtocol): ...

    @abstractmethod
    def pay(self, order: OrderProtocol): ...


class NewOrder(OrderState):
    def pay(self, order: OrderProtocol) -> None:
        print('Payment accepted')
        order.state = PaidOrder()

    def ship(self, order: OrderProtocol) -> NoReturn:
        raise Exception('Order not paid yet')


class PaidOrder(OrderState):
    def pay(self, order: OrderProtocol) -> NoReturn:
        raise Exception('Already paid')

    def ship(self, order: OrderProtocol) -> None:
        print('Order shipped')
        order.state = ShippedOrder()


class ShippedOrder(OrderState):
    def pay(self, order: OrderProtocol) -> NoReturn:
        raise Exception('Already shipped')

    def ship(self, order: OrderProtocol) -> NoReturn:
        raise Exception('Already shipped')
