import requests
from playment.response import PlaymentResponse
from playment.exception import PlaymentException
from playment.utilities import to_dict
import time


class Head:
    playment_key = "x-client-key"


def is_retryable(code: int) -> bool:
    if code in [408, 429, 443, 444] or code >= 500:
        return True
    return False


def is_post(method) -> bool:
    if method == "POST":
        return True
    return False


def retry(url: str, headers: dict, method: str, data=None, limit: int = 3, count: int = 1):
    print("retrying for {} time".format(str(count)))

    if is_post(method=method):
        response = requests.post(url, headers=headers, json=data)
        if is_retryable(response.status_code) and count <= limit:
            count += 1
            time.sleep(0.5*count)
            response = retry(url=url, headers=headers, method=method, data=data, limit=limit, count=count)
        return response

    else:
        response = requests.get(url, headers=headers)
        if is_retryable(response.status_code) and count <= limit:
            count += 1
            time.sleep(0.5*count)
            response = retry(url, headers=headers, method=method, limit=limit, count=count)
        return response


class Requests:
    def __init__(self, value: str):
        self.headers = dict(zip([Head.playment_key], [value]))

    def post(self, url: str, data=None, limit: int = 3, headers: dict = None) -> PlaymentResponse:
        if headers is None:
            headers = self.headers
        else:
            headers.update(self.headers)

        if data is not None:
            data = to_dict(obj=data)

        res = requests.post(url, headers=headers, json=data)
        if is_retryable(res.status_code):
            res = retry(url=url, headers=headers, data=data, method=res.request.method, limit=limit)
        response = PlaymentResponse(res)
        if response.success is False:
            raise PlaymentException(response)
        return response

    def get(self, url: str, limit: int = 3, headers=None) -> PlaymentResponse:
        if headers is None:
            headers = self.headers
        else:
            headers.update(self.headers)
        res = requests.get(url, headers=self.headers)
        if is_retryable(res.status_code):
            res = retry(url=url, headers=headers, method=res.request.method, limit=limit)
        response = PlaymentResponse(res)
        if response.success is False:
            raise PlaymentException(response)
        return response
