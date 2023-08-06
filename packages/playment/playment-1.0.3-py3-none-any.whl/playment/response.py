def response(res: dict):
    success = res['success']
    data = res['data'] if 'data' in res else None
    error = res['error'] if 'error' in res else None
    return success, data, error


def response_to_dict(res):
    return response(res.json())


class PlaymentResponse:
    def __init__(self, res):
        self.success, self.data, self.error = response_to_dict(res)
