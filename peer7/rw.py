# This is rw.py file
import os
import sys
import json
 
def readList(name):
	f = open(name, 'r')
	r_list = f.read()
	f.close()
	if r_list == "":
		rlist = []
	else:
		#parse it by Json
		rlist = json.loads(r_list)
	return rlist

def readDict(name):
	f = open(name, 'r')
	r_dict = f.read()
	f.close()
	if r_dict == "":
		rdict = {
			'original': {},
			'download': {}
		}
	else:
		#parse it by Json
		rdict = json.loads(r_dict)
	return rdict

def readFile(path):
	f = open(path, 'r')
	content = f.read()
	f.close()
	return content

def write(name, content):
	f = open(name, 'w+')
	f.write(json.dumps(content))
	f.close()

def writeFile(name, content):
	f = open(name, 'w+')
	f.write(content)
	f.close()