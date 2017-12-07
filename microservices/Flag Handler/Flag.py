import sys
sys.path.append("../../classes")
from Configuration import SourceConfiguration
from DataSource import DataBaseSource
from flask import Flask, jsonify, json, request
from flask_cors import cross_origin
import pyodbc

app = Flask(__name__)

# Service Functionality
@app.route('/Flag/L1')
@cross_origin()
def L1Flags():

    # Try
    try:
        config = SourceConfiguration("../config/datasource.config")
        DataSource = DataBaseSource(config)
        DataSource.TDSconfigure()
        Flags = []
        with open("../SQLQueries/L1Flags.sql") as r:
            Query = r.read()
            Flags = DataSource.read(Query)

        for Row in Flags:
            print(Row)
        return "Working"


    # Except
    except Exception as e:
        print(str(e))
        return False, str(e)

# Run Main
if __name__ == '__main__':
    # Set to False when deploying
    app.debug = True
    app.run(host='127.0.0.1', port=8084)
