from typing import List


class PostalAddress(dict):
    """
    {
      "revision": number,
      "regionCode": string,
      "languageCode": string,
      "postalCode": string,
      "sortingCode": string,
      "administrativeArea": string,
      "locality": string,
      "sublocality": string,
      "addressLines": [
        string
      ],
      "recipients": [
        string
      ],
      "organization": string
    }
    """

    def __init__(self, revision: int = None, region_code: str = '', language_code: str = '',
                 postal_code: str = '',
                 sorting_code: str = '', administrative_area: str = '', locality: str = '',
                 sublocality: str = '',
                 address_lines: List[str] = None, recipients: List[str] = None, organization: str = ''):
        super().__init__()

        if revision is not None:
            self['revision'] = revision

        if region_code is not None:
            self['regionCode'] = region_code

        if language_code is not None:
            self['languageCode'] = language_code

        if postal_code is not None:
            self['postalCode'] = postal_code

        if sorting_code is not None:
            self['sortingCode'] = sorting_code

        if administrative_area is not None:
            self['administrativeArea'] = administrative_area

        if locality is not None:
            self['locality'] = locality

        if sublocality is not None:
            self['sublocality'] = sublocality

        if address_lines is not None:
            self['addressLines'] = address_lines

        if recipients is not None:
            self['recipients'] = recipients

        if organization is not None:
            self['organization'] = organization

    def add_address_lines(self, address_lines: str) -> List[str]:
        for item in address_lines:
            assert isinstance(item, str)
            self['addressLines'].append(item)

        return self['addressLines']

    def add_recipients(self, recipients: str) -> List[str]:

        for item in recipients:
            assert isinstance(item, str)
            self['recipients'].append(item)

        return self['recipients']
