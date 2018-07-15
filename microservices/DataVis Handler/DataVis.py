import sys
sys.path.append("../../classes")
from Configuration import SourceConfiguration
from DataSource import DataBaseSource
from flask import Flask, jsonify, json, request
from flask_cors import cross_origin
from collections import Counter
from sqlalchemy.sql import text
import pyodbc

app = Flask(__name__)
app.url_map.strict_slashes = False

# Service Functionality
@app.route('/DataVis/Datastreams')
@cross_origin()
def GetDataStreams():

    # Try
    try:
        # Connection Section
        config = SourceConfiguration("../config/datasource.config")
        DataSource = DataBaseSource(config)
        DataSource.TDSconfigure()

        # Retrieving Data
        DS = []
        with open("../SQLQueries/CompleteDetailedDataStreamQuery.sql") as r:
            Query = r.read()
            Query = text(Query)
            DS = DataSource.Connection.execute(Query)

        Row = DS.fetchone()

        DataStreams = []
        while Row is not None:
            DataStream = {}
            DataStream['Stream ID'] = Row[0]
            DataStream['Deployment ID'] = Row[1]
            DataStream['Category ID'] = Row[2]
            DataStream['Property ID'] = Row[3]
            DataStream['Property Name'] = Row[4]
            DataStream['Unit ID'] = Row[5]
            DataStream['Unit Name'] = Row[6]
            DataStream['Type ID'] = Row[7]
            DataStream['Data Type Name'] = Row[8]
            DataStream['Data Interval'] = Row[9]
            DataStream['Started'] = Row[10]
            DataStream['Ended'] = Row[11]
            DataStream['Deployment Name'] = Row[12]
            DataStream['Deployment ID'] = Row[13].lower()

            DataStreams.append(DataStream)
            Row = DS.fetchone()

        return jsonify(DataStreams)

    # Except
    except Exception as e:
        print(str(e))
        return False, str(e)





# Service Functionality
@app.route('/DataVis/Measurements/<DatastreamID>/<Interval>')
@cross_origin()
def GetMeasurementsByStream(DatastreamID,Interval=100):

    # Try
    try:
        # Connection Section
        config = SourceConfiguration("../config/datasource.config")
        DataSource = DataBaseSource(config)
        DataSource.TDSconfigure()

        # Retrieving Data
        Measurements = []
        with open("../SQLQueries/MeasurementsByDatastream.sql") as r:
            Query = r.read()
            Query = text(Query)
            Measurements = DataSource.Connection.execute(Query,x=DatastreamID,y=Interval)

        # Processing Data
        StructuredData = {}
        Row = Measurements.fetchone()
        StructuredData['Datastream ID'] = Row[0]
        StructuredData['Deployment ID'] = Row[1]
        StructuredData['Deployment Name'] = Row[2]
        StructuredData['Measurements'] = []

        # Processing Each Measurement
        while Row is not None:
            Measurement = {}
            Measurement['Time Stamp'] = Row[4]
            Measurement['Value'] = str(Row[3])
            Measurement['Flag Type'] = Row[5]
            StructuredData['Measurements'].append(Measurement)
            Row = Measurements.fetchone()


        #Serialize
        return jsonify(StructuredData)

    # Except
    except Exception as e:
        print(str(e))
        return False, str(e)

# Run Main
if __name__ == '__main__':
	# Set to False when deploying
	app.debug = False
	app.run(host='127.0.0.1', port=8093)
