from . import ReasonType


class RejectionInfo(dict):
    """
    {
      "type": enum(ReasonType),
      "reason": string,
    }
    """

    def __init__(self, rejection_type: ReasonType, reason: str):
        super(RejectionInfo, self).__init__()

        self.rejection_type = rejection_type
        self.reason = reason

    @property
    def reason(self):
        return self.get('reason')

    @reason.setter
    def reason(self, reason: str):
        self['reason'] = reason

    @property
    def rejection_type(self):
        return ReasonType(self.get('type'))

    @rejection_type.setter
    def rejection_type(self, rejection_type: ReasonType):
        self['type'] = rejection_type.name
