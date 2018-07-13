import sys
sys.path.append("../classes")
from Configuration import SourceConfiguration, TestConfiguration
from DataSource import DataBaseSource
from DataContainers import Measurement, DataStream, DataBundle
from Testing import Tester
from flask import Flask, jsonify, json, request
from flask_cors import cross_origin,CORS
from collections import Counter
from sqlalchemy.sql import text
from threading import Thread, Lock
import queue
import pyodbc
import time

CACHE_FILE = 'DemoCache.json' #global constant

#variables
Final = {}
Status = {'Status':'Not Running'}
Lock = Lock()

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/Demo/*": {"origins": "*"}})

def ReportProgress(Status):

    Lock.acquire()

    with open(CACHE_FILE, 'w') as file:
        file.write(json.dumps(Status))

    Lock.release()

def RunDemo():
    # Variable
    Num = 0
    DataStreamQuerySource = "SQLQueries/DetailedDataStreamQuery.sql"
    MeasurementQuerySource= "SQLQueries/measurementQuery.sql"
    TesterGroup = []


    # Connection Section
    config = SourceConfiguration("config/datasource.config")
    Final["Source Config XML"] = config.XMLString

    #print(config.XMLString)

    DataSource = DataBaseSource(config)
    DataSource.TDSconfigure()

    DataStreams = DataSource.fetchDataStreams(DataStreamQuerySource)

    #Fetching Streams
    Status['Status'] = "Fetching Streams"
    ReportProgress(Status)

    Final["Data Streams"] = []
    for Stream in DataStreams:
         Final["Data Streams"].append(Stream.MetaData);

         #print(Stream.MetaData)

    Status['Status'] = "Fetching Measurements"
    ReportProgress(Status)

    DataStreams = DataSource.fetchMeasurements(DataStreams, MeasurementQuerySource)


    Final["Measurements"] = {}
    for Stream in DataStreams:
        Final["Measurements"][Stream.StreamID] = len(Stream.Measurements)

        #print( "Number of Measurements from DataStream ", Stream.StreamID, " :", len(Stream.Measurements) )

    Status['Status'] = "Building Tests"
    ReportProgress(Status)

    TestConfig = TestConfiguration("config/tests.config")
    Final["Test Configuration"] = TestConfig.XMLString
    for Stream in DataStreams:
        TesterGroup.append( Tester( TestConfig.TestParameters[str(Stream.StreamID)] , Stream ) )

    begin = time.time()

    Status['Status'] = "Running Tests"

    for TNdx, TesterObj in enumerate(TesterGroup):
        Status["DataStream"] = TNdx + 1
        Status["Total"] = len(TesterGroup)
        ReportProgress(Status)

        TesterObj.RunTests()

    end = time.time()

    #For Final Reporting of Demo Status
    Final["Testing Time"] = round((end - begin), 2)


    Status['Status'] = "Loading Flags"

    for DNdx, TesterObj in enumerate(TesterGroup):
        Status["DataStream"] = DNdx + 1
        Status["Total"] = len(TesterGroup)
        ReportProgress(Status)

        Num += 1
        Final[str(Num)] = DataSource.writeFlagsToDataStream(TesterObj.DataStream.StreamID, TesterObj.DataStream.Measurements)

    #Serialize
    Status['Status'] = 'Complete'
    ReportProgress(Status)



#q = queue.Queue()



# Service Functionality
@app.route('/Demo/Config')
@cross_origin()
def Get():

    thread = Thread(target=RunDemo)

    #Try
    try:
        Status['Status'] = "Started"
        ReportProgress(Status)

        #start RunDemo in own thread
        thread.start()

        return jsonify(Status)

    # Except
    except Exception as e:
        print(str(e))
        line = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        print(line)
        return False, str(e), line


@app.route('/Demo/Check')
@cross_origin()
def Check():
    # Try
    try:
        Lock.acquire()
        with open(CACHE_FILE, 'r') as file:
            Status = file.read();
        Lock.release()

        Status = json.loads(Status)

        return jsonify(Status)

    # Except
    except Exception as e:
        print(str(e))
        line = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        print(line)
        return False, str(e), line


# Service Functionality
@app.route('/Demo/Run')
@cross_origin()
def Run():

    # Try
    try:
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
	app.run(host='127.0.0.1', port=8069, threaded=True)
