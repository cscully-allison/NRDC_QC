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
DataSource.configure()


DataStreams = DataSource.fetchDataStreams(DataStreamQuerySource)

DataStreams = DataSource.fetchMeasurements(DataStreams, MeasurementQuerySource)

TestConfig = TestConfiguration("config/tests.config")

print(TestConfig.TestParameters)



for Stream in DataStreams:
    TesterGroup.append( Tester( TestConfig.TestParameters[str(Stream.StreamID)] , Stream ) )

for TesterObj in TesterGroup:
    TesterObj.RunTests()
    for ndx, M in enumerate(TesterObj.DataStream.Measurements):
        print(M.Value, M.TimeStamp, ", ", M.Flag)
