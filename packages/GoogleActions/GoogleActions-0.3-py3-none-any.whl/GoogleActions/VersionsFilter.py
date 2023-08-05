class VersionsFilter(dict):
    """
    {
      'minVersion': number,
      'maxVersion': number
    }
    """

    def __init__(self, min_version: int = None, max_version: int = None):
        super().__init__()

        self['minVersion'] = min_version
        self['maxVersion'] = max_version
