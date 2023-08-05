from typing import List


class OptionInfo(dict):
    """
     {
          'key': string,
          'synonyms': [
            string
          ]
        }
    """

    def __init__(self, key: str = '', synonyms: List[str] = None):
        super().__init__()

        self['synonyms'] = list()

        if key is not None:
            self['key'] = key

        self['synonyms'].extend(synonyms)

    def add_synonyms(self, synonyms: str) -> List[str]:
        for item in synonyms:
            self['synonyms'].append(item)
        return self['synonyms']
