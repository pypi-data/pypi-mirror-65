from . import PriceType
from .Money import Money


class Price(dict):
    """
    {
      "type": enum(PriceType),
      "amount": {
        object(Money)
      },
    }
    """

    def __init__(self, price_type: PriceType, amount: Money):
        super().__init__()

        self.amount = amount
        self.price_type = price_type

    @property
    def amount(self):
        return self.get('amount')

    @amount.setter
    def amount(self, amount: Money):
        self['amount'] = amount

    @property
    def price_type(self):
        return PriceType(self.get('type'))

    @price_type.setter
    def price_type(self, price_type: PriceType):
        self['type'] = price_type.name
