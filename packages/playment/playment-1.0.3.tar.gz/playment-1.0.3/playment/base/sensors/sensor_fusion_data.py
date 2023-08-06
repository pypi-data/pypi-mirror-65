from playment.base.sensors.frame import Frame
from playment.base.sensors.sensor import Sensor
from typing import List


class SensorFusionData:
    def __init__(self, frames: List[Frame] = [], sensor: List[Sensor] = []):
        self.frames = frames
        self.sensor_meta = sensor

    def add_sensor(self, sensor: Sensor):
        self.sensor_meta.append(sensor)

    def add_frame(self, frame: Frame):
        self.frames.append(frame)
