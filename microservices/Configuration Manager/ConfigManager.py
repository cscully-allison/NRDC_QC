import sys
sys.path.append("..")
sys.path.append("../../classes/")
sys.path.append("../config/")
from Configuration import TestConfiguration, SourceConfiguration
from DataSource import DataBaseSource
from flask import Flask, jsonify, json, request
from flask_cors import cross_origin
from sqlalchemy.sql import text
import pyodbc


def getDataStreamMetadata(DataSource, TestParams):
	
	TestMDBundle = []

	with open("../SQLQueries/DSMetaData.sql") as r:
		Query = r.read()
		Query = text(Query)
		DataStreams = DataSource.Connection.execute(Query)

	Row = DataStreams.fetchone()


	while Row is not None:
		for key in TestParams:
			if Row[0] == int(key):	
				TestMDBundle.append({"ID":Row[0], "Site":Row[1], "Deployment": Row[2], "Data Interval": Row[3], "Data Type": Row[4]})
		Row = DataStreams.fetchone()

	return TestMDBundle	
		
	


app = Flask(__name__)

# Service Functionality
@app.route('/Config/')
@cross_origin()
def getTestConfigurations():

	# Try
	try:
		#variables
		ReturnedData = {}

		# Connection Section        
		config = SourceConfiguration("../config/datasource.config")
		DataSource = DataBaseSource(config)
		DataSource.TDSconfigure()
		
		TC = TestConfiguration("../config/tests.config")	
			
		TestMetaData = getDataStreamMetadata(DataSource, TC.TestParameters)

		ReturnedData["Data"] = TC.TestParameters
		ReturnedData["MetaData"] = TestMetaData

		ReturnedTests = jsonify(ReturnedData)


		return(ReturnedTests)

	# Except
	except Exception as e:
		print(str(e))
		return False, str(e)

# Run Main
if __name__ == '__main__':
	# Set to False when deploying
	app.debug = True
	app.run(host='127.0.0.1', port=8081)
