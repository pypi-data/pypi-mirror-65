class LatLng(dict):
    """
    {
      "latitude": number,
      "longitude": number
    }
    """

    def __init__(self, latitude, longitude) -> None:
        super().__init__()

        self['latitude'] = latitude
        self['longitude'] = longitude
