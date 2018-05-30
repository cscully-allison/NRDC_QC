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

@app.route('/Config/GetTests')
@cross_origin
def getTests():

	try:
		testconfig = new TestConfiguration("config/tests.config")
                testmdjson = jsonify( testconfig.TestParameters)

		return testmdjson

	except Exception as e:
		print (str(e))
		return False, str(e)

# Run Main
if __name__ == '__main__':
	# Set to False when deploying
	app.debug = True
	app.run(host='127.0.0.1', port=8081)
