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

#find the service we are requesting to run up
for child in root.findall('service'):
	if (child.find('name').text == ServiceName):
		Path = child.find('path').text
		Port = child.find('port').text
		ExeFile = child.find('exe').text

print(Path)

#start the service
StartCommand = 'uwsgi --socket 127.0.0.1:{0} --chdir {1} --protocol http --callable app --file {2}'.format(Port, Path, ExeFile)
p = subprocess.Popen(['sudo', 'bash', '-c', StartCommand])



#store the pid
for child in root.findall('service'):
	if (child.find('name').text == ServiceName):
		child.find('pid').text = str(p.pid)

tree.write(Directory)

#print(output)


