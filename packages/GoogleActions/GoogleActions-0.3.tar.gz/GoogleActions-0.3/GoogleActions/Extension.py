class Extension(dict):
    """
    {
        "@type": string,
        field1: ...,
        ...
    }
    """

    def __init__(self, extension_type: str, **fields):
        super().__init__()

        if extension_type is not None:
            self['@type'] = extension_type

        self.add_fields(**fields)

    @property
    def extension_type(self):
        return self.get('@type')

    @extension_type.setter
    def extension_type(self, extension_type: str):
        self['@type'] = extension_type

    def add_fields(self, **kwargs) -> dict:
        self.update(kwargs)

        return self
