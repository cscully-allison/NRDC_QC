import sys
sys.path.append("..")
sys.path.append("../../classes")
from flask import Flask, jsonify, json, request
from flask_cors import cross_origin
import pyodbc
from Configuration import TestConfiguration

app = Flask(__name__)

# Service Functionality
@app.route('/Config/')
@cross_origin()
def index():

    # Try
    try:
        #top level calls should return api info maybe
        return("working")

    # Except
    except Exception as e:
        print(str(e))
        return False, str(e)


@app.route('/Config/GetTests/')
@cross_origin()
def getTests():

    try:
        testconfig = TestConfiguration("../config/tests.config")
        testmdjson = jsonify( testconfig.TestParameters)

        return testmdjson

    except Exception as e:
        print (str(e))
        return False, str(e)


@app.route('/Config/GetTests/<DataStreamID>')
@cross_origin()
def getTestsForDs(DataStreamID):
    TestsInDS = []
    
    try:
        TestConfig = TestConfiguration("../config/tests.config")

        for ds,tests in TestConfig.TestParameters.items():
            print(ds, DataStreamID)
            if ds == DataStreamID:
                TestsInDS = tests
        
        return jsonify(TestsInDS)

    except Exception as e:
        print (str(e))
        return False, str(e)


@app.route('/Config/ModifyTests/', methods=['POST'])
@cross_origin()
def loadTestData():
    try:
        modifiedTest = request.get_json()

        TestConfig = TestConfiguration("../config/tests.config")
        
        TestConfig.WriteChanges(modifiedTest)

        return jsonify({'requestPayload':request.get_json()})

    except Exception as e:
        print (str(e))
        return False, str(e)


# Run Main
if __name__ == '__main__':
    # Set to False when deploying
    app.debug = True
    app.run(host='127.0.0.1', port=8081)
