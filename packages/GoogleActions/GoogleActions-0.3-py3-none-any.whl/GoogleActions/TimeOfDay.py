class TimeOfDay(dict):

    def __init__(self, nanos: int = 0, minutes: int = 0, hours: int = 0, seconds: int = 0):
        super(TimeOfDay, self).__init__()

        self['nanos'] = nanos
        self['minutes'] = minutes
        self['hours'] = hours
        self['seconds'] = seconds
