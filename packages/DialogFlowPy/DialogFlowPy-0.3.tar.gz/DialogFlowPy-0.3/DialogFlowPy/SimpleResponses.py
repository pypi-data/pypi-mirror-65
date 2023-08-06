from typing import List

from DialogFlowPy.SimpleResponse import SimpleResponse


class SimpleResponses(dict):

    def __init__(self, simple_responses: List[SimpleResponse]) -> None:
        super().__init__()

        self['simpleResponses'] = []
        self['simpleResponses'].extend(simple_responses)

    @property
    def simple_responses(self):
        return self.get('simpleResponses')

    @simple_responses.setter
    def simple_responses(self, simple_responses_list: List[SimpleResponse]):
        self['simpleResponses'] = []
        self['simpleResponses'].extend(simple_responses_list)

    @simple_responses.deleter
    def simple_responses(self):
        self['simpleResponses'] = []
