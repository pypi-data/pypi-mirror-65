class Date(dict):

    def __init__(self, year: int = None, month: int = None, day: int = None):
        super().__init__()

        self['year'] = year
        self['month'] = month
        self['day'] = day
