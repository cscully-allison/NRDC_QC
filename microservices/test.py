import sys
sys.path.append("../classes")

from sqlalchemy import create_engine
from Configuration import SourceConfiguration
from DataSource import DataBaseSource

#variables
config = None
DataSource = None
ResultRows = []
Result = None
DataStreamQuerySource = "SQLQueries/DetailedDataStreamQuery.sql"
Query = ""
Measurements = None

#Get configuration and set up data source
config = SourceConfiguration("config/datasource.config")
DataSource = DataBaseSource(config)
DataSource.configure()

with open(DataStreamQuerySource) as DSQ:
	Query = DSQ.read()
	result = DataSource.read(Query


for row in result:
	ResultRows.append(dict(row))

for x in ResultRows:
	if x["PropertyName"] == 'Temperature' and x["DataTypeName"] == 'Average':
		result = DataSource.read(Query)
