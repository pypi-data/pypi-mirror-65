from collections import namedtuple
from playment.utilities import Decodable


def _json_object_hook(d):
    return namedtuple('job_status', d.keys())(*d.values())


class BatchSummary(Decodable):
    def __init__(self, id: str = None, project_id: str = None, name: str = None, jobs: list = []):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.jobs = jobs

    def json_object_hook(self, d):
        if 'jobs' in d:
            jobs = []
            for j in d['jobs']:
                j = dict(j._asdict())
                jobs.append(_json_object_hook(j))
            d['jobs'] = jobs
        obj = namedtuple(self.__class__.__name__, d.keys())(*d.values())
        return obj
