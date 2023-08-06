from playment.base.sensors.sensorframeobject import SensorFrameObject
from typing import List


class Frame:
    def __init__(self, frame_id: str = None, sensors: List[SensorFrameObject] = []):
        self.frame_id = frame_id
        self.sensors = sensors

    def add_sensor(self, sensor: SensorFrameObject):
        assert type(sensor) is SensorFrameObject
        self.sensors.append(sensor)
