import sys
from abc import ABCMeta, abstractmethod
from Configuration import SourceConfiguration
from sqlalchemy import create_engine

class DataSource:
    __metaclass__ = ABCMeta

    def __init__(self, configuration = None):
        self.configuration = configuration

    @abstractmethod
    def configure(self):
        return False

    @abstractmethod
    def read(self):
        return False

    @abstractmethod
    def write(self):
        return False




class DataBaseSource(DataSource):

    def __init__(self, configuration = None):
        self.Configuration = configuration
        self.Engine = None
        self.Connection = None


    def configure(self):
        #retrieve configuration dictionary
        ConfigDict = self.Configuration.SourceMetaData["DataSource"]

        #get connection string
        ConnString = ConfigDict["Connection"];

        #build connection string
        ConnString = ConnString.format(ConfigDict["Username"], ConfigDict["Password"], ConfigDict["InitialCatalog"]["Name"])

        #generate connection and bind to class
        self.Engine = create_engine(ConnString)
        self.Connection = self.Engine.connect()

        return False


    def read(self, SQLQuery):
        QueryResponse = self.Connection.execute(SQLQuery)
        return QueryResponse


    def write(self):
        return False
