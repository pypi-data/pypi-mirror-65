from collections import namedtuple

from playment.utilities import Decodable


class JobResponse(Decodable):
    def __init__(self, job_id: str = None, reference_id: str = None, tag: str = None):
        self.job_id = job_id
        self.reference_id = reference_id
        self.tag = tag

    def json_object_hook(self, d):
        return namedtuple(self.__class__.__name__, d.keys())(*d.values())
