#!/usr/bin/env python

import subprocess
import xml.etree.ElementTree as ET
import sys

#variables
ServiceName = ""
Directory = "service_directory.xml"
PID = ""

tree = root = None

#get input from the user
if(len(sys.argv) > 1):
	ServiceName = sys.argv[1]

#parse the xml file to get the data about the xml file we want to start up
tree = ET.parse(Directory)
root =  tree.getroot()

#find the service we are requesting to run up
for child in root.findall('service'):
	if (child.find('name').text == ServiceName):
		PID = child.find('pid').text

#kill the service
KillCommand = 'kill {}'.format(PID)
p = subprocess.Popen(['sudo', 'bash', '-c', KillCommand])



#erase the pid
for child in root.findall('service'):
	if (child.find('name').text == ServiceName):
		child.find('pid').text = ""

tree.write(Directory)

print("Service was sucessfully killed")


