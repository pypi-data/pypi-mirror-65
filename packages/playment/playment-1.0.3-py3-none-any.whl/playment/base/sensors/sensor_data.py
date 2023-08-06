from playment.base.data import Data
from playment.base.sensors.sensor_fusion_data import SensorFusionData
from playment.base.sensors.sensor import Sensor
from playment.base.sensors.frame import Frame


class SensorData(Data):
    def __init__(self, sensor_fusion_data: SensorFusionData = SensorFusionData(), metadata=None):
        self.sensor_data = sensor_fusion_data
        self.metadata = metadata

    def add_sensor(self, sensor: Sensor):
        self.sensor_data.add_sensor(sensor)

    def add_frame(self, frame: Frame):
        self.sensor_data.add_frame(frame)

    def valid(self):
        try:
            assert len(self.sensor_data.sensor_meta) > 0
            return True
        except AssertionError:
            return False
