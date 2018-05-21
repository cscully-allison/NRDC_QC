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
TablesQuery = "SQLQueries/TablesMetadata.sql"
DataStreamQuerySource = "SQLQueries/DetailedDataStreamQuery.sql"
MeasurementQuerySource= "SQLQueries/measurementQuery.sql"
Query = ""
DataStreams = []
Measurements = []
TesterGroup = []

#Get configuration and set up data source
config = SourceConfiguration("config/datasource.config")
#print(config.XMLString)
DataSource = DataBaseSource(config)
#DataSource.configure()
DataSource.TDSconfigure()


# with open(TablesQuery) as Q:
#     Query = Q.read()
#     print(Query)
# Tables = DataSource.read(Query)

for table in Tables:
    print("Table ", table)

#DataStream and measurement retrieval
DataStreams = DataSource.fetchDataStreams(DataStreamQuerySource)
for Stream in DataStreams:
    print("Data indentifying stream", Stream.StreamID, ":" , Stream.MetaData)

DataStreams = DataSource.fetchMeasurements(DataStreams, MeasurementQuerySource)
for Stream in DataStreams:
    print("Number of Measurements Queried for ", Stream.StreamID , ":", len( Stream.Measurements ) )


#Test Configuration
TestConfig = TestConfiguration("config/tests.config")
print(TestConfig.XMLString)


for Stream in DataStreams:
    TesterGroup.append( Tester( TestConfig.TestParameters[str(Stream.StreamID)] , Stream ) )


#testing
for TesterObj in TesterGroup:
    print("Running tests for Measurements in DataStream: ", TesterObj.DataStream.StreamID)
    TesterObj.RunTests()


#return (show flagged data that goes back into db)
for TesterObj in TesterGroup:
    DataSource.writeFlagsToDataStream(TesterObj.DataStream.StreamID, TesterObj.DataStream.Measurements)
