import playment

client = playment.Client("x-client-key")

"""
Get Job Result Data
"""
try:
    job_result = client.get_job_result(project_id="project_id",
                                       job_id="project_id")
except playment.exception.PlaymentException as e:
    print(e.code, e.message, e.data)
