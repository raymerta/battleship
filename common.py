#!/usr/bin/env python
	
import random
import time
import json

gameRoomName = ['Atlantic Ocean', 'Arctic Ocean', 'Indian Ocean', 'Pacific Ocean', 'Norwegian Sea', 'North Sea', 'Aegean Sea', 'Southern Ocean', 'Arabian Sea', 'East China Sea']

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

def createGameRoom(tiles, player, serverId, username):
	content = getAllSessions()

	# generate random game room name
	roomType = random.randint(0, (len(gameRoomName) - 1))
	roomName = gameRoomName[roomType]

	if (content != ""):
		sessions = json.loads(content)
		roomId = len(sessions) + 1

		data = {"serverId" : serverId, "numPlayers" : player, "size" : tiles, "creator": username , "roomName": roomName, "roomCreated": int(time.time()), "isPlaying": False, "isEnded" : False , "gameRoomId" : roomId, "users": [{"username": username, "isTurn" : False, "isDefeated" : False, "isWinning" : False, "isPlaying" : False}] }
		sessions.append(data)

		dataObject = json.dumps(sessions)

		fsource = 'sessions.json'
		f = open(fsource, 'w')
		f.write(dataObject)
		f.close()

		return roomId

	else:
		#empty json file, proceed to create initial content
		data = [{"serverId" : serverId, "numPlayers" : player, "size" : tiles, "creator": username , "roomName": roomName, "roomCreated": int(time.time()), "isPlaying": False, "isEnded" : False , "gameRoomId" : 1, "users": [{"username": username, "isTurn" : False, "isDefeated" : False, "isWinning" : False, "isPlaying" : False}] }]
		dataObject = json.dumps(data)

		fsource = 'sessions.json'
		f = open(fsource, 'w')
		f.write(dataObject)
		f.close()

		#return user ID number
		return 1