class ResponseMetadata(dict):

    def __init__(self, status: str):
        super().__init__()

        self['status'] = status
