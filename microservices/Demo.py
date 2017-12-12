import sys
sys.path.append("../classes")
from Configuration import SourceConfiguration, TestConfiguration
from DataSource import DataBaseSource
from DataContainers import Measurement, DataStream, DataBundle
from Testing import Tester
from flask import Flask, jsonify, json, request
from flask_cors import cross_origin
from collections import Counter
from sqlalchemy.sql import text
import pyodbc

app = Flask(__name__)
app.url_map.strict_slashes = False

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

# Service Functionality
@app.route('/Demo/')
@cross_origin()
def Get():

    # Try
    try:       
        # Variables
        Final = {}
        Num = 0
        # Connection Section        
        config = SourceConfiguration("config/datasource.config")
        DataSource = DataBaseSource(config)
        DataSource.TDSconfigure()

        DataStreams = DataSource.fetchDataStreams(DataStreamQuerySource)

        DataStreams = DataSource.fetchMeasurements(DataStreams, MeasurementQuerySource)

        TestConfig = TestConfiguration("config/tests.config")

        for Stream in DataStreams:
            TesterGroup.append( Tester( TestConfig.TestParameters[str(Stream.StreamID)] , Stream ) )

        for TesterObj in TesterGroup:
            TesterObj.RunTests()

        for TesterObj in TesterGroup:
            Num +=1
            Final[str(Num)] = DataSource.writeFlagsToDataStream(TesterObj.DataStream.StreamID, TesterObj.DataStream.Measurements)
        
        #Serialize
        return jsonify(Final)

    # Except
    except Exception as e:
        print(str(e))
        line = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        print(line)
        return False, str(e), line

# Run Main
if __name__ == '__main__':
	# Set to False when deploying
	app.debug = False
	app.run(host='127.0.0.1', port=8069)
