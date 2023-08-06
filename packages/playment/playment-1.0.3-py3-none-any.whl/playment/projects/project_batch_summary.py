from collections import namedtuple
from playment.utilities import Decodable


def _json_object_hook(d):
    return namedtuple('BatchDetails', d.keys())(*d.values())


class ProjectBatchSummary(Decodable):
    def __init__(self, name: str = None, base: str = None, batches: list = []):
        self.name = name
        self.base = base
        self.batches = batches

    def json_object_hook(self, d):
        if 'batches' in d:
            jobs = []
            for j in d['batches']:
                j = dict(j._asdict())
                jobs.append(_json_object_hook(j))
            d['batches'] = jobs
        obj = namedtuple(self.__class__.__name__, d.keys())(*d.values())
        return obj
