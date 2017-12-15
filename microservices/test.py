import sys
sys.path.append("../classes")

from sqlalchemy import create_engine
from Configuration import SourceConfiguration, TestConfiguration
from DataSource import DataBaseSource
from DataContainers import Measurement, DataStream, DataBundle
from Testing import Tester

#variables
config = None
DataSource = None
ResultRows = []
Result = None
DataStreamQuerySource = "SQLQueries/DetailedDataStreamQuery.sql"
MeasurementQuerySource= "SQLQueries/measurementQuery.sql"
Query = ""
DataStreams = []
Measurements = []
TesterGroup = []

#Get configuration and set up data source
config = SourceConfiguration("config/datasource.config")
DataSource = DataBaseSource(config)
#DataSource.configure()
DataSource.TDSconfigure()

#DataStream and measurement retrieval
DataStreams = DataSource.fetchDataStreams(DataStreamQuerySource)
DataStreams = DataSource.fetchMeasurements(DataStreams, MeasurementQuerySource)


#Test Configuration
TestConfig = TestConfiguration("config/tests.config")
for Stream in DataStreams:
    TesterGroup.append( Tester( TestConfig.TestParameters[str(Stream.StreamID)] , Stream ) )


#testing
for TesterObj in TesterGroup:
    TesterObj.RunTests()


#return (show flagged data that goes back into db)
for TesterObj in TesterGroup:
    DataSource.writeFlagsToDataStream(TesterObj.DataStream.StreamID, TesterObj.DataStream.Measurements)
