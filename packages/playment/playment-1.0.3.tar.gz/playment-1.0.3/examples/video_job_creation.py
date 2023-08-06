import playment

client = playment.Client("x-client-key")

frames = [
    "https://example.com/image_url_1",
    "https://example.com/image_url_2",
    "https://example.com/image_url_3"
]


"""
Create sensor_data variable
"""
sensor_data = playment.SensorData()


"""
Defining Sensor: Contain details of sensor
:param _id: This is the sensor's id.
:param name: Name of the sensor.
:param primary_view: Only one of the sensor can have primary_view as true.
:param state(optional): If you want this sensor not to be annotated, provide state as non_editable. Default is editable.
"""
sensor = playment.Sensor(_id="right", name="right", primary_view=True)

"""
Adding Sensor
"""
sensor_data.add_sensor(sensor=sensor)

"""
Preparing Frame Data
"""
for i in range(len(frames)):
    # Preparing a sensor frame object with with sensor frame url and sensor_id
    sensor_frame_object = playment.SensorFrameObject(frames[i], sensor.id)
    # Preparing a frame with every sensor frame object
    frame = playment.Frame(str(i), [sensor_frame_object])
    # Adding the frame in sensor data
    sensor_data.add_frame(frame=frame)


"""
Creating a job with sensor data
:param reference_id: This will be unique for every job in a given project.
:param tag: This will be provided by Playment and will only take one type of data. For e.g. ImageData or SensorData.
:param data: This is the data you are sending to Playment.
:param batch_id: This is an optional argument which will associate the job to the given batch if its left as none,
              the job will be associated with the default batch. It is recommended to create a batch for a set of flus.
:param priority_weight(optional): Range of priority weight is [1,10] and integers only. 10 is the highest priority.
                                  Default is 5.
"""
try:
    job = client.create_job(reference_id="54", tag='sensor_fusion',
                            data=sensor_data, project_id="project_id")

except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
