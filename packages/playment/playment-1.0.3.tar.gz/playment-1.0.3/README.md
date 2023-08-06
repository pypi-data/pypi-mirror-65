## Installation
You don't need this source code unless you want to modify the package. If you just want to use the package, just run:

```pip install --upgrade playment```

Install from source with:

```python setup.py install```

Requirements:

``Python 3.5+``

## Documentation
Please visit the docs.playment.io to know more about Playment APIs.

## Usage
```
import playment
client = playment.Client(client_key="your x-client-key")
```
It is a secret key required to call Playment APIs. The secret x-client-key ensures that only you are able to access your projects.
The x-client-key can be accessed from the settings page of your dashboard.



#### Get Project Summary
```
try:
    project_summary = client.get_project_summary(project_id=project_id)
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
```


#### Get Project's Batches Summary
This will provide all the batches and their summary
```
try:
    project_batch_summary = client.get_project_batches_summary(project_id=project_id)
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
```


#### Get Batch Summary
This will provide you summary of batch with its jobs and viewer links.
```
try:
    batch_summary = client.get_batch_summary(project_id=project_id,
                                             batch_id=batch_id)
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
```


#### Creating a Batch
This will return a batch object with batch_id
:param name: Name for the batch. E.g. John
:param label: Label for the batch. E.g. Doe
:param description: Description for the batch. E.g. Alias for unknown.
```
try:
    batch = client.create_batch(name="test_99", label="test_99", description="label",
                                project_id=project_id)
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
```


#### Creating a Single-Image Based Job 
```

"""
Prepare Image Data
"""
image_url = "https://example.com/image_url_1"
image_data = playment.ImageData(image_url=image_url)

"""
Image Data job creation
"""
try:
    job = client.create_job(reference_id="55", tag='image',
                            data=image_data, project_id="project_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)

```


#### Creating a Sensor Based Job with Multiple Images with only camera sensor.
```

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
    # Preparing a sensor frame object with sensor frame url and sensor_id
    sensor_frame_object = playment.SensorFrameObject(frames[i], sensor.id)
    # Preparing a frame with every sensor
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

```

#### Creating a Sensor Based Job with Multiple Images/PCDs.
```
"""
Collect sensor_poses for cameras w.r.t lidar in your suitable format
"""
sensor_poses = {
    "lidar": {
        "heading": {"w": 1, "x": 0,
                    "y": 0, "z": 0},
        "position": {"x": 0, "y": 0, "z": 0}
    },
    "camera_1": {
        "heading": {"w": -0.4512317755370607, "x": 0.5520064554320538,
                    "y": -0.5425287998749007, "z": 0.444231087625815},
        "position": {"x": 0, "y": 0, "z": 0}
    },
    "camera_2": {
        "heading": {"w": -0.7029770474706961, "x": 0.6997847239102162,
                    "y": 0.10452563699437759, "z": -0.07210410614207517},
        "position": {"x": 0, "y": 0, "z": 0}
    }
}

"""
Collect frames for every sensor.
"""
lidar_frames = [
    "https://example.com/pcd_url_1",
    "https://example.com/pcd_url_2"
]

camera_1_frames = [
    "https://example.com/image_url_1",
    "https://example.com/image_url_2"
]

camera_2_frames = [
    "https://example.com/image_url_3",
    "https://example.com/image_url_4"
]

"""
Initialize sensor_data
"""
sensor_data = playment.SensorData()

"""
Defining Sensor: This will contain detail about sensor's attributes.
:param _id: This is the sensor's id.
:param name: Name of the sensor.
:param primary_view: Only one of the sensor can have primary_view as true.
:param state(optional): If you want this sensor not to be annotated, provide state as non_editable. Default is editable.
:param modality: This is the type of sensor.
:param intrinsics: In case of a camera modality sensor we will need the sensor intrinsics. 
                This field should ideally become part of the sensor configuration, and not be sent as part of each Job.
                "cx": principal point x value
                "cy": principal point y value
                "fx": focal length in x axis
                "fy": focal length in y axis
                "k1": 1st radial distortion coefficient
                "k2": 2nd radial distortion coefficient
                "k3": 3rd radial distortion coefficient
                "k4": 4th radial distortion coefficient
                "p1": 1st tangential distortion coefficient
                "p2": 2nd tangential distortion coefficient
                "skew": camera skew coefficient
                "scale_factor": The factor by which the image has been downscaled (=2 if original image is twice as
                                large as the downscaled image)
"""

"""
Preparing Lidar Sensor
"""
lidar_sensor = playment.Sensor(_id="lidar", name="lidar", primary_view=True, modality="lidar")
sensor_data.add_sensor(lidar_sensor)

"""
Preparing Camera Sensor for camera_1
"""
camera_1_intrinsics = playment.Intrinsics(
    cx=1024.56301417, cy=592.004009216, fx=1050.21459961, fy=1051.06384277,
    k1=0, k2=0, k3=0, k4=0, p1=0, p2=0, skew=0, scale_factor=1
)
camera_1 = playment.Sensor(_id="camera_1", name="camera_1", primary_view=False,
                           modality="camera", intrinsics=camera_1_intrinsics)
sensor_data.add_sensor(camera_1)

"""
Preparing Camera Sensor for camera_2
"""
camera_2_intrinsics = playment.Intrinsics(
    cx=1013.0894433, cy=596.331393608, fx=2209.12548828, fy=2209.49682617,
    k1=0, k2=0, k3=0, k4=0, p1=0, p2=0, skew=0, scale_factor=1
)
camera_2 = playment.Sensor(_id="camera_2", name="camera_2", primary_view=True, modality="camera")
camera_2.add_intrinsics(camera_2_intrinsics)
sensor_data.add_sensor(camera_2)

"""
Preparing frame data
"""

for i in range(len(lidar_frames)):
    # Preparing a sensor frame object with sensor frame url and sensor_id
    lidar_sensor = playment.SensorFrameObject(data_url=lidar_frames[i], sensor_id="lidar")
    lidar_heading = playment.Heading(
        w=sensor_poses['lidar']['heading']['w'],
        x=sensor_poses['lidar']['heading']['x'],
        y=sensor_poses['lidar']['heading']['y'],
        z=sensor_poses['lidar']['heading']['z']
    )
    lidar_position = playment.Position(
        x=sensor_poses['lidar']['position']['x'],
        y=sensor_poses['lidar']['position']["y"],
        z=sensor_poses['lidar']['position']["z"]
    )

    lidar_sensor_pose = playment.SensorPose(heading=lidar_heading, position=lidar_position)
    lidar_sensor.add_sensor_pose(lidar_sensor_pose)

    camera_1_sensor = playment.SensorFrameObject(data_url=camera_1_frames[i], sensor_id="camera_1")
    camera_1_heading = playment.Heading(
        w=sensor_poses['camera_1']['heading']['w'],
        x=sensor_poses['camera_1']['heading']['x'],
        y=sensor_poses['camera_1']['heading']['y'],
        z=sensor_poses['camera_1']['heading']['z']
    )
    camera_1_position = playment.Position(
        x=sensor_poses['camera_1']['position']['x'],
        y=sensor_poses['camera_1']['position']["y"],
        z=sensor_poses['camera_1']['position']["z"]
    )

    camera_1_sensor_pose = playment.SensorPose(heading=camera_1_heading, position=camera_1_position)
    camera_1_sensor.add_sensor_pose(camera_1_sensor_pose)

    camera_2_sensor = playment.SensorFrameObject(data_url=camera_2_frames[i], sensor_id="camera_2")
    camera_2_heading = playment.Heading(
        w=sensor_poses['camera_2']['heading']['w'],
        x=sensor_poses['camera_2']['heading']['x'],
        y=sensor_poses['camera_2']['heading']['y'],
        z=sensor_poses['camera_2']['heading']['z']
    )
    camera_2_position = playment.Position(
        x=sensor_poses['camera_2']['position']['x'],
        y=sensor_poses['camera_2']['position']["y"],
        z=sensor_poses['camera_2']['position']["z"]
    )

    camera_2_sensor_pose = playment.SensorPose(heading=camera_2_heading, position=camera_2_position)
    camera_2_sensor.add_sensor_pose(camera_2_sensor_pose)

    # Preparing a frame with every sensor
    frame = playment.Frame(frame_id=str(i), sensors=[lidar_sensor, camera_1_sensor, camera_2_sensor])
    # Adding the frame in sensor data
    sensor_data.add_frame(frame)


"""
Sensor Data job creation
"""
try:
    job = client.create_job(reference_id="54", tag='sensor_fusion',
                            data=sensor_data, project_id="project_id")

except playment.PlaymentException as e:
    print(e.code, e.message, e.data)

```

#### Creating a Job with metadata
metadata: You can send any type of data in metadata which can be useful in the task or record of any other data related to that job. 

```
image_url = "https://example.com/image_url"
metadata = {
    "reference_image_1":"https://example.com/reference_image_url_1",
    "reference_image_2":"https://example.com/reference_image_url_2"
}
image_data = playment.ImageData(image_url=image_url, metadata=metadata)

try:
    job = client.create_job(reference_id="55", tag='image',
                            data=image_data, project_id="project_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)

```

#### Create Jobs with High Priority and associating them with a batch
```
image_url = "https://example.com/image_url"
image_data = playment.ImageData(image_url=image_url)

try:
    job = client.create_job(reference_id="55", tag='image',
                            data=image_data, project_id="project_id",
                            priority_weight=10, batch_id="batch_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
```

#### Get Job Result
```
try:
    job_result = client.get_job_result(project_id="project_id",
                                       job_id="job_id")
except playment.exception.PlaymentException as e:
    print(e.code, e.message, e.data)
```