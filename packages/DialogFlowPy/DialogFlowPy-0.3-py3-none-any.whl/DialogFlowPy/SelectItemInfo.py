from typing import List


class SelectItemInfo(dict):
    """
    {
      "key": string,
      "synonyms": [
        string
      ]
    }
    """

    def __init__(self, key: str, synonyms: str):
        super().__init__()

        self['key'] = key
        self['synonyms'] = []
        self['synonyms'].extend(synonyms)

    def add_synonyms(self, synonyms: str) -> List[str]:
        self['synonyms'].extend(synonyms)
        return self['synonyms']
