from collections import namedtuple
from playment.utilities import Decodable


class BatchResponse(Decodable):
    def __init__(self, batch_id: str = None):
        self.batch_id = batch_id

    def json_object_hook(self, d):
        return namedtuple(self.__class__.__name__, d.keys())(*d.values())
