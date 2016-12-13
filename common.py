#!/usr/bin/env python
	
def getAllServers():
	fsource = 'server.json'
	f = open(fsource, 'r')
	content = f.read()
	f.close()

	

	return content

