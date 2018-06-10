#!/usr/bin/env python

import subprocess
import xml.etree.ElementTree as ET
import sys

#variables
Port = ""
ExeFile = ""
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

#Print the name of all services
for service in root.findall('service'):
	StartCommand = "./restart_service.py {0}".format(service.find('name').text)
	p = subprocess.call(['sudo', 'bash', '-c', StartCommand])
