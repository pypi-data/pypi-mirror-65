import json
import abc


class Decodable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
                hasattr(subclass, 'json_object_hook') and
                callable(subclass.json_object_hook)
        )

    @abc.abstractmethod
    def json_object_hook(self, d):
        raise NotImplementedError


class JSON2Obj:
    def __init__(self, obj: Decodable, data: str):
        self.obj = obj
        self.data = data

    def json2obj(self):
        return json.loads(self.data, object_hook=self.obj.json_object_hook)


def to_dict(obj):
    return json.loads(
        json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o)))
    )
