import playment

client = playment.Client("x-client-key")

"""
Prepare Image Data
:param metadata: You can send any type of data in metadata which can be useful in the task or record
                 of any other data related to that job.
"""
image_url = "https://example.com/image_url"
metadata = {
    "reference_image_1": "https://example.com/reference_image_url_1",
    "reference_image_2": "https://example.com/reference_image_url_2"
}
image_data = playment.ImageData(image_url=image_url, metadata=metadata)

"""
Image Data job creation
:param batch_id: This is an optional argument which will associate the job to the given batch if its left as none,
              the job will be associated with the default batch. It is recommended to create a batch for a set of flus.
:param priority_weight(optional): Range of priority weight is [1,10] and integers only. 10 is the highest priority.
                                  Default is 5.
"""
try:
    job = client.create_job(reference_id="55", tag='image',
                            data=image_data, project_id="project_id",
                            priority_weight=10, batch_id="batch_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
