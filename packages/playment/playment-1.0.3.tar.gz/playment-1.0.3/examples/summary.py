import playment

client = playment.Client("x-client-key")

"""
Get project summary
"""
try:
    project_summary = client.get_project_summary(project_id="project_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)

"""
Get batch summary
"""
try:
    batch_summary = client.get_batch_summary(project_id="project_id",
                                             batch_id="batch_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)

"""
Get project's batches summary
"""
try:
    project_batch_summary = client.get_project_batches_summary(project_id="project_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
