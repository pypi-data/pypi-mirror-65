import json
from collections import namedtuple


def _json_object_hook(d):
    return namedtuple('api_urls', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


data = {
    "job_creation": "https://api.playment.in/projectsvc/projects/{}/jobs",
    "batch_creation": "v1/project/{}/batch",
    "project_overview": "v0/projects/{}/stats",
    "project_details": "v0/projects/{}/details",
    "batch_summary": "v0/projects/{}/batch/{}",
    "job_result": "v0/projects/{}/jobs/{}",
    "base_url": "https://api.playment.io"
}

apis = {
    "job_creation": data['job_creation'],
    "batch_creation": data['base_url'] + "/" + data['batch_creation'],
    "project_summary": data['base_url'] + "/" + data['project_overview'],
    "project_batch_details": data['base_url'] + "/" + data['project_details'],
    "batch_summary": data['base_url'] + "/" + data['batch_summary'],
    "job_result": data['base_url'] + "/" + data['job_result']
}


urls = json2obj(json.dumps(apis))
