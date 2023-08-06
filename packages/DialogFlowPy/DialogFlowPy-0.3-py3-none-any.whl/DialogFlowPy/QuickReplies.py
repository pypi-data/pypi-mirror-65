from typing import List


class QuickReplies(dict):
    """
    {
      "title": string,
      "quickReplies": [
        string
      ]
    }
    """

    def __init__(self, title: str, quick_replies: str):
        super().__init__()

        self['title'] = title
        self['quickReplies'] = []
        for item in quick_replies:
            self['quickReplies'].append(item)

    def add_quick_replies(self, quick_replies: str) -> List[str]:
        if self['quickReplies'] is None:
            self['quickReplies'] = []
        for item in quick_replies:
            self['quickReplies'].append(item)

        return self['quickReplies']

    @property
    def output(self):
        return {
            "title": self['title'],
            "quickReplies": self['quickReplies']
        }
