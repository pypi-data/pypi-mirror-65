from playment.utilities import JSON2Obj, Decodable, to_dict
from collections import namedtuple
from playment.base.sensors.sensor_data import SensorData
import unittest
import json


class TestJson2Obj(unittest.TestCase):
    def test_json2obj(self):
        test_data = JSON2Obj(obj=URL(), data=json.dumps({"url": "yo_2"})).json2obj()
        self.assertEqual(test_data.url, URL().url)

    def test_json2obj_2(self):
        test_data = JSON2Obj(obj=URL(), data=json.dumps({"url": "yo_1"})).json2obj()
        self.assertEqual(test_data.url, URL().url)

    def test_todict(self):
        test_data = to_dict(SensorData())
        self.assertDictEqual(test_data, {"sensor_data": {"sensor_meta": [], "frames": []}, "metadata": None})

    def test_todict_fail(self):
        self.assertRaises(AssertionError, to_dict, 'sensor')


class URL(Decodable):
    def __init__(self):
        self.url = "yo_1"

    def json_object_hook(self, d):
        return namedtuple(self.__class__.__name__, d.keys())(*d.values())



