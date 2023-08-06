import playment

client = playment.Client("x-client-key")

"""
Prepare Image Data
"""
image_url = "https://example.com/image_url"
image_data = playment.ImageData(image_url=image_url)

"""
Image Data job creation
"""
try:
    job = client.create_job(reference_id="55", tag='image',
                            data=image_data, project_id="project_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
