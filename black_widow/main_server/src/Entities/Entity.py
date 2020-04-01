import abc

class Entity(abc.ABC):
    @abc.abstractmethod
    def dictionary(self):
        pass

    @abc.abstractmethod
    def objectFromDictionary(self, dict):
        pass