from playment.response import PlaymentResponse


class ExceptionCodes:
    FS_0001 = "Duplicate Reference Id, Note: For each unique job/sequence you must use unique reference id"
    FS_0002 = "reference_id is missing"
    FS_0003 = "Data URL invalid or duplicate frame_id detected in case of sequential data or Invalid string for\n" \
              " frame_id detected in case of sequential data."
    FS_0004 = "Data missing"
    FS_0005 = "tag missing"
    FS_0006 = "Job Unit not found"
    FS_0007 = "Image Urls not found"
    GE_0001 = "Malformed JSON/Invalid UUID passed"
    GE_0002 = "Parameter missing"
    unauthorized_request = "client-key is invalid. Please contact the administrator"
    resource_error = "project_id not found"
    BATCH_CREATION = """Add: batch names in a project are unique,
                        pq: duplicate key value violates unique constraint 'batches_project_id_name_unique'"""


class PlaymentException(Exception):
    def __init__(self, res: PlaymentResponse):

        self.code = res.error['code']
        self.message = getattr(ExceptionCodes, self.code) if hasattr(ExceptionCodes, self.code)\
                                                                    else res.error['message']
        self.data = res.data
