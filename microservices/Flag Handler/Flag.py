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

# Retrieve All L1 Flags and their breakdown
@app.route('/Flag/L1')
@cross_origin()
def L1Flags():

    # Try
    try:
        # Connection Section        
        config = SourceConfiguration("../config/datasource.config")
        DataSource = DataBaseSource(config)
        DataSource.TDSconfigure()

        # Retrieving Data
        Flags = []
        with open("../SQLQueries/L1Flags.sql") as r:
            Query = r.read()
            Flags = DataSource.read(Query)

        # Processing Data
        UniqueFlags = {}
        for v, w, x, y, z in Flags:
            UniqueFlags[str(x)] = UniqueFlags.get(x, 0) + 1

        # Calculating Total
        Keys = list(UniqueFlags.keys())
        UniqueFlags['Total'] = 0
        for Key in Keys:
            UniqueFlags['Total'] = UniqueFlags['Total'] + UniqueFlags[Key]

        #Serialize
        return jsonify(UniqueFlags)

    # Except
    except Exception as e:
        print(str(e))
        return False, str(e)

# Retrieve All Flagged Datastreams and Measurements
@app.route('/Flag/L1/<FlagID>')
@cross_origin()
def L1FlagsRefined(FlagID):

    # Try
    try:
        # Connection Section        
        config = SourceConfiguration("../config/datasource.config")
        DataSource = DataBaseSource(config)
        DataSource.TDSconfigure()

        # Retrieving Data
        Measurements = []
        with open("../SQLQueries/DatastreamMeasurementsByFlag.sql") as r:
            Query = r.read()
            Query = text(Query)
            Measurements = DataSource.Connection.execute(Query,x=FlagID)

        # Processing Data
        StructuredData = {}
        StructuredData['L1 Flag'] = FlagID
        Row = Measurements.fetchone()
        StructuredData['Flag Name'] = Row[6]
        StructuredData['Flag Description'] = Row[7]
        
        # Building the Datastreams section
        while Row is not None:
            if str(Row[0]) not in StructuredData:
                StructuredData[str(Row[0])] = {}
                StructuredData[str(Row[0])]["Deployment ID"] = Row[1]
                StructuredData[str(Row[0])]["Deployment Name"] = Row[2]
                StructuredData[str(Row[0])]["Measurements"] = []
            
            # Building the Measurements section
            MeasurementEntry = {}
            MeasurementEntry['Time Stamp'] = str(Row[4])
            MeasurementEntry['Value'] = str(Row[3])
            StructuredData[str(Row[0])]["Measurements"].append(MeasurementEntry)
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
    app.run(host='127.0.0.1', port=8094)
