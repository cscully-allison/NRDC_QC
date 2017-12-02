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
        ConfigDOM = self.Configuration.SourceMetaData

        #get connection string
        ConnString = ConfigDOM.getElementsByTagName("Connection")[0].firstChild.nodeValue;

        #build connection string
        ConnString = ConnString.format(ConfigDOM.getElementsByTagName("Username")[0].firstChild.nodeValue, ConfigDOM.getElementsByTagName("Password")[0].firstChild.nodeValue, ConfigDOM.getElementsByTagName("Name")[0].firstChild.nodeValue)

        #generate connection and bind to class
        self.Engine = create_engine(ConnString)
        self.Connection = self.Engine.connect()



    def read(self, SQLQuery):
        QueryResponse = self.Connection.execute(SQLQuery)
        return QueryResponse

    """
        Retrieves all data streams that have associated tests.
        I currently have all the sql code in a file and it filters
        from what's returned by that.
        todo: More programatic query building
    """
    def fetchDataStreams(self, QuerySource):
        #variables
        Query = ""
        result = None #A SQLAlchemy row proxy object
        DOM = self.Configuration.SourceMetaData
        DataStreamsList = None
        TestableDataStreamIDs = []
        ReturnableRows = []

        #get the names of all datastreams to be Tested
        DataStreamsList = DOM.getElementsByTagName("Stream")

        for elem in DataStreamsList:
            TestableDataStreamIDs.append(elem.firstChild.nodeValue)

        print( TestableDataStreamIDs )

        #with open(QuerySource) as Q:
        #	Query = Q.read()
        #	result = DataSource.read(Query)

        return



    def fetchMeasurements(self):
        return

    def write(self):
        return False
