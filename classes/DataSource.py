import sys
from abc import ABCMeta, abstractmethod
from Configuration import SourceConfiguration
from DataContainers import DataStream, Measurement
from sqlalchemy import create_engine
import pyodbc
import urllib

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

def Connect(User,Pass,Db):
    ConnStr ="DRIVER={FreeTDS};Server=ASGARD-LOKI;Database="+ Db +";UID="+ User +";PWD="+ Pass +";TDS_Version=8.0;Port=1433;"
    print(ConnStr)
    pyodbc.connect(ConnStr)


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

    def TDSconfigure(self):

        # Extract User, Pass, and Db Name from DOM
        ConfigDOM = self.Configuration.SourceMetaData
        User = ConfigDOM.getElementsByTagName("Username")[0].firstChild.nodeValue
        Pass = ConfigDOM.getElementsByTagName("Password")[0].firstChild.nodeValue
        Db = ConfigDOM.getElementsByTagName("Name")[0].firstChild.nodeValue

        # Form TDS connection string
        quoted = urllib.parse.quote_plus("DRIVER={FreeTDS};Server=asgard-loki.rd.unr.edu;Database="+ Db +";UID="+ User +";PWD="+ Pass +";TDS_Version=8.0;Port=1433;")
        self.Engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(quoted))
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
        DataStreams = []
        ReturnableRows = []

        #get the names of all datastreams to be Tested
        DataStreamsList = DOM.getElementsByTagName("Stream")
        for elem in DataStreamsList:
            TestableDataStreamIDs.append(elem.firstChild.nodeValue)


        #Query All 10 minute datastreams
        with open(QuerySource) as Q:
            Query = Q.read()
            ReturnableRows = self.read(Query)

        #Filer streams by the ID associated with tests
        for Row in ReturnableRows:
            if str(Row['Stream']) in TestableDataStreamIDs:
                DataStreams.append( DataStream([], dict(Row)) )

        return DataStreams


    def fetchMeasurements(self, DataStreamsList, QuerySource):
        #variables
        Query = ""
        ReturnedRows = None

        #Query Measurements associated with a particular datastream
        for Stream in DataStreamsList:
            with open(QuerySource) as Q:
                Query = Q.read()
                Query = Query.format(Stream.MetaData["Stream"])
                ReturnedRows = self.read(Query)

                for Row in ReturnedRows:
                    Stream.insertMeasurement(Measurement(Row["Value"], Row["Measurement Time Stamp"], Row["L1 Flag"], Row["Stream"]))


        return DataStreamsList

    def write(self):
        return False
