import sys
sys.path.append("../classes")

from sqlalchemy import create_engine
from Configuration import SourceConfiguration, TestConfiguration
from DataSource import DataBaseSource
from DataContainers import Measurement, DataStream, DataBundle

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

#Get configuration and set up data source
config = SourceConfiguration("config/datasource.config")
DataSource = DataBaseSource(config)
DataSource.configure()


DataStreams = DataSource.fetchDataStreams(DataStreamQuerySource)

DataStreams = DataSource.fetchMeasurements(DataStreams, MeasurementQuerySource)

TestConfig = TestConfiguration("config/tests.config")

"""
Query Measurements associated with a partiuclar data stream

for x in ResultRows:
	if x["PropertyName"] == 'Temperature' and x["DataTypeName"] == 'Average':
		DataStreams.append(x)

with open(MeasurementQuerySource) as MQS:
	Query = MQS.read()
	for Stream in DataStreams:
		result = DataSource.read(Query.format(Stream["Stream"]))
		for row in result:
			Measurements.append(Measurement(row['Value'], row['Measurement Time Stamp'], row['L1 Flag'], row['Stream']))
		Stream["Measurements"] = Measurements
		Measurements = []
"""
