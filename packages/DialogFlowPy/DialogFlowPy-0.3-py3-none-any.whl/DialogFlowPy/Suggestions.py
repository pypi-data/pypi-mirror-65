from typing import List

from DialogFlowPy.Suggestion import Suggestion


class Suggestions(dict):
    """
    {
      "suggestions": [
        {
          object(Suggestion)
        }
      ]
    }
    """

    def __init__(self, suggestions: List[Suggestion]):
        super().__init__()

        self['suggestions'] = suggestions

    def add_suggestions(self, suggestions: List[Suggestion]):
        for item in suggestions:
            self['suggestions'].append(item)
        return self
