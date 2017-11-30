import sys
sys.path.append("../classes")

from sqlalchemy import create_engine
from Configuration import SourceConfiguration
from DataSource import DataBaseSource

config = SourceConfiguration("config/datasource.config")

DataSource = DataBaseSource(config)

DataSource.configure()
result = DataSource.read("select name from Data.[Data Streams]")

for x in result:
	print (x)




"""
engine = create_engine("mssql+pyodbc://cilstudent:cil!234@asgard-loki.rd.unr.edu/ProtoNRDC?driver=ODBC+Driver+13+for+SQL+Server")
connection = engine.connect()

result = connection.execute("select deployment, name from infrastructure.deployments")

for x in result:
	print x
"""
