from playment.jobs import Job
from playment.config import urls
from playment.requests import Requests
from playment.batches.batch_handler import Batch
from playment.base.data import Data
from playment.utilities import JSON2Obj
from playment.projects import ProjectSummary, ProjectBatchSummary
from playment.batches import BatchSummary
from playment.jobs import JobResult
from playment.batches import BatchResponse
from playment.jobs import JobResponse
from playment.exception import ExceptionCodes
import json


class Client:
    def __init__(self, client_key: str):
        assert client_key is not None and type(client_key) is str
        self.client_key = client_key
        self.requester = Requests(client_key)

    def create_batch(self, name, label, description, project_id: str) -> Batch:
        assert name is not None
        assert label is not None
        assert description is not None
        assert project_id is not None
        url = urls.batch_creation.format(project_id)
        batch = Batch(name=name, label=label, description=description)
        response = self.requester.post(url=url, data=batch)
        batch_response = JSON2Obj(BatchResponse(), json.dumps(response.data)).json2obj()
        batch.id = batch_response.batch_id
        return batch

    def create_job(self, reference_id: str, tag: str, data: Data, project_id: str,
                   priority_weight: int = 5, batch_id: str = None) -> Job:
        assert project_id is not None and type(project_id) is str
        assert issubclass(type(data), Data) is True
        if not data.valid():
            raise ExceptionCodes.FS_0003
        url = urls.job_creation.format(project_id)
        job = Job(reference_id=reference_id, tag=tag, data=data, priority_weight=priority_weight, batch_id=batch_id)
        response = self.requester.post(
            url=url,
            data=job
        )
        job_response = JSON2Obj(JobResponse(), json.dumps(response.data)).json2obj()
        job.id = job_response.job_id
        return job

    def get_project_summary(self, project_id: str) -> ProjectSummary:
        assert project_id is not None
        url = urls.project_summary.format(project_id)
        response = self.requester.get(
            url=url
        )
        response = JSON2Obj(ProjectSummary(), json.dumps(response.data)).json2obj()
        return response

    def get_project_batches_summary(self, project_id: str)->ProjectBatchSummary:
        assert project_id is not None
        url = urls.project_batch_details.format(project_id)
        response = self.requester.get(
            url=url
        )
        response = JSON2Obj(ProjectBatchSummary(), json.dumps(response.data)).json2obj()
        return response

    def get_batch_summary(self, batch_id: str, project_id: str)->BatchSummary:
        assert batch_id is not None
        assert project_id is not None
        url = urls.batch_summary.format(project_id, batch_id)
        response = self.requester.get(
            url=url
        )
        response = JSON2Obj(BatchSummary(), json.dumps(response.data)).json2obj()
        return response

    def get_job_result(self, project_id: str, job_id: str) -> JobResult:
        assert project_id is not None
        assert job_id is not None
        url = urls.job_result.format(project_id, job_id)
        response = self.requester.get(
            url=url
        )
        response = JSON2Obj(JobResult(), json.dumps(response.data)).json2obj()
        return response
