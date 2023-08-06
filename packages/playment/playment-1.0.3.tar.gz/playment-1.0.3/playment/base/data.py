import abc


class Data(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'valid') and
                callable(subclass.valid))

    @abc.abstractmethod
    def valid(self):
        raise NotImplementedError
