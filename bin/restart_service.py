#!/usr/bin/env python

import subprocess
import xml.etree.ElementTree as ET
import sys

#variables
Port = ""
ExeFile = ""
Path = ""
ServiceName = ""
pid = ""
Directory = "service_directory.xml"

tree = root = None

#get input from the user
if(len(sys.argv) > 1):
	ServiceName = sys.argv[1]

#parse the xml file to get the data about the xml file we want to start up
tree = ET.parse(Directory)
root =  tree.getroot()

print("Restarting. . .")

#find the service we are requesting to run up
for child in root.findall('service'):
	if (child.find('name').text == ServiceName):
		pid = child.find('pid').text
		Path = child.find('path').text
		Port = child.find('port').text
		ExeFile = child.find('exe').text

#if process is already running then kill it
if( pid != ""):
	KillCommand = 'kill {}'.format(pid)
	p = subprocess.Popen(['sudo', 'bash', '-c', KillCommand])

#build start command from needed port, path to the python file containing the service code, and the file itself contiainig the code
# subprocess.Popen automatically runs processes in the background
StartCommand = 'uwsgi --socket 127.0.0.1:{0} --chdir {1} --protocol http --callable app --file {2}'.format(Port, Path, ExeFile)
p = subprocess.Popen(['sudo', 'bash', '-c', StartCommand])



#store the pid
for child in root.findall('service'):
	if (child.find('name').text == ServiceName):
		child.find('pid').text = str(p.pid)

tree.write(Directory)

#print(output)


