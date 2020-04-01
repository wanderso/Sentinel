import abc
from typing import List

class SentinelTableEntry(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_description') and
                callable(subclass.get_description) and
                hasattr(subclass, 'get_name') and
                callable(subclass.get_name) and
                hasattr(subclass, 'add_observer') and
                callable(subclass.add_observer))

    @abc.abstractmethod
    def get_description(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_observer(self, observ):
        raise NotImplementedError


class SentinelTableContainer(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_traits') and
                callable(subclass.get_traits) and
                hasattr(subclass, 'get_name') and
                callable(subclass.get_name) and
                hasattr(subclass, 'add_observer') and
                callable(subclass.add_observer))

    @abc.abstractmethod
    def get_traits(self) -> List[SentinelTableEntry]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_observer(self, observ):
        raise NotImplementedError



