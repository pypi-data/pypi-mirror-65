class DateTime(dict):

    def __init__(self, time: str, date: str):
        super().__init__()

        self['time'] = time
        self['date'] = date
