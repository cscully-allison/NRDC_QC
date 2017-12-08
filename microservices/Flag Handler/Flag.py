import sys
sys.path.append("../../classes")
from Configuration import SourceConfiguration
from DataSource import DataBaseSource
from flask import Flask, jsonify, json, request
from flask_cors import cross_origin
from collections import Counter
import pyodbc
import json

app = Flask(__name__)

def JSONDumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


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
            UniqueFlags[x] = UniqueFlags.get(x, 0) + 1

        # Calculating Total
        Keys = list(UniqueFlags.keys())
        UniqueFlags['Total'] = 0
        for Key in Keys:
            UniqueFlags['Total'] = UniqueFlags['Total'] + UniqueFlags[Key]

        #Serialize
        return json.dumps(UniqueFlags, default=JSONDumper, indent=1)

    # Except
    except Exception as e:
        print(str(e))
        return False, str(e)

# Run Main
if __name__ == '__main__':
    # Set to False when deploying
    app.debug = False
    app.run(host='127.0.0.1', port=8094)
