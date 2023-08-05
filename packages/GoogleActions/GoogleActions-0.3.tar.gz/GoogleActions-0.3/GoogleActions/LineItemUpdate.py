from .OrderState import OrderState
from .Price import Price
from .Extension import Extension
from .Money import Money
from . import PriceType


class LineItemUpdate(dict):
    """
    {
      "orderState": {
        object(OrderState)
      },
      "price": {
        object(Price)
      },
      "reason": string,
      "extension": {
        "@type": string,
        field1: ...,
        ...
      },
    }
    """

    def __init__(self, reason: str = '', price: Price = None, order_state: OrderState = None,
                 extension: Extension = None):
        super().__init__()

        if reason is not None:
            self['reason'] = reason

        if price is not None:
            self['price'] = price

        if order_state is not None:
            self['orderState'] = order_state

        if extension is not None:
            self['extension'] = extension

    def add_order_state(self, state: str, label: str) -> OrderState:
        self['orderState'] = OrderState(state=state, label=label)
        return self['orderState']

    def add_price(self, price_type: PriceType, amount, currency_code) -> Price:
        self['price'] = Price(price_type=price_type, amount=Money(amount=amount, currency_code=currency_code))
        return self['price']

    def add_extension(self, extension_type: str, **kwargs) -> Extension:
        self['extension'] = Extension(extension_type, **kwargs)
        return self['extension']
