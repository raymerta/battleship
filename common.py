#!/usr/bin/env python
	
import json

def getAllServers():
	fsource = 'server.json'
	f = open(fsource, 'r')
	content = f.read()
	f.close()

	return content

def getAllSessions():
	fsource = 'sessions.json'
	f = open(fsource, 'r')
	content = f.read()
	f.close()

	return content	

def getSessionServer(serverId):
	content = getAllSessions()

	if (content != ""):
		games = json.loads(content)
		display = []

		for game in games:
			if (int(game['serverId']) == int(serverId)):
				display.append(game)
		return json.dumps(display)
	else:
		return ''

	