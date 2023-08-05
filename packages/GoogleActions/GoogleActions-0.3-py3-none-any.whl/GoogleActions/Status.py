class Status(dict):
    """
    {
      "code": number,
      "message": string,
      "details": [
        {
          "@type": string,
          field1: ...,
          ...
        }
      ]
    }
    """

    def __init__(self, code: int = None, message: str = '', detail_type: str = '', **fields):
        super().__init__()

        if code is not None:
            self['code'] = code

        if message is not None:
            self['message'] = message

        if detail_type is not None:
            self['@type'] = detail_type

        for key, value in fields.items():
            self[key] = value

    def add_fields(self, **fields) -> dict:

        for key, value in fields.items():
            self[key] = value

        return self
