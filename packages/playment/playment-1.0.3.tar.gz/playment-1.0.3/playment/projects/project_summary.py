from collections import namedtuple

from playment.utilities import Decodable


class ProjectSummary(Decodable):
    def __init__(self, name: str = None, base: str = None, total_batches: int = None, completed_batches: int = None,
                 total_jobs: int = None, completed_jobs: int = None,
                 total_frames: int = None, completed_frames: int = None, annotations: int = None):
        self.name = name
        self.base = base
        self.total_batches = total_batches
        self.completed_batches = completed_batches
        self.total_jobs = total_jobs
        self.completed_jobs = completed_jobs
        self.total_frames = total_frames
        self.completed_frames = completed_frames
        self.annotations = annotations

    def json_object_hook(self, d):
        return namedtuple(self.__class__.__name__, d.keys())(*d.values())
