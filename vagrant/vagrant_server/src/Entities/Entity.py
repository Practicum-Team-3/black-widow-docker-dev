import abc

class Entity(abc.ABC):
    @abc.abstractmethod
    def dictionary(self):
        """
        Converts an entity object to a dictionary.
        """
        pass

    @abc.abstractmethod
    def objectFromDictionary(self, dict):
        """
        Creates an object from a dictionary.
        :param dict: Dictionary containing the object information
        """
        pass