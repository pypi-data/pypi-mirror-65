from math import modf


class Money(dict):

    def __init__(self, amount: float, currency_code: str):
        super().__init__()

        nanos, self['units'] = modf(amount)
        self['nanos'] = int(nanos * pow(10, 9))
        self['currencyCode'] = currency_code
