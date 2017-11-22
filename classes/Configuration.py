from abc import ABCMeta, abstractmethod

class Configuration:
    __metaclass__ = ABCMeta

    def __init__(self, SourceFile = None):
        self.SourceFile = SourceFile

    @abstractmethod
    def CheckForChanges(self):
        return False

    @abstractmethod
    def Update(self):
        return False
