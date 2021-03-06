#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import os
import sys
import random
import time
import json
import common

serverAddress = ('localhost', 10001)

from PDU import PDU

# setting up response header

serverList = {}

responseHeaders = {}

responseHeaders[200] =\
"""HTTP/1.0 200 OK
Server: ws30
Content-type: %s

%s
"""

responseHeaders[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: %s

%s
"""

responseHeaders[422] =\
"""HTTP/1.0 422 Unprocessable Entity
Server: ws30
Content-type: %s

%s
"""

# setting mime types
mimeTypes = {
	'.jpg': 'image/jpg',
	'.gif': 'image/gif',
	'.png': 'image/png',
	'.html': 'text/html',
	'.pdf': 'application/pdf',
	'.css': 'text/css',
	'.js': 'application/javascript'}

# getMime
def getMime(uri):
	return mimeTypes.get(os.path.splitext(uri)[1], 'text/plain')

# ===================================================================
# networking section
# ===================================================================

# socketServer handling
def socketServer(serverAddress):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(serverAddress)
    sock.listen(5)
    return sock

# handling routing
def routingHandler(pduResult, conn, addr):

	# remove beginning /
	addr = pduResult.uri.split('/')
	print >> sys.stderr, "printing addr 1:"
	print >> sys.stderr, addr[1]

	content = ''
	fsource = ''
	component = ''
	mime = 'text/html'


	# refactor this is have time

	# home page
	if (addr[1] == ''):
		fsource = 'index.html'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()

		component = (200, content, mime)
		sendResponse(conn, component)

	elif (addr[1] == 'server'):
		fsource = 'user.html'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()

		component = (200, content, mime)
		sendResponse(conn, component)

	elif (addr[1] == 'session'):
		fsource = 'session.html'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()

		component = (200, content, mime)
		sendResponse(conn, component)

	elif (addr[1] == 'game'):
		fsource = 'game.html'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()

		component = (200, content, mime)
		sendResponse(conn, component)

	##########

	elif (addr[1] == '_insertname'):

		## DELETE LINE BELOW
		print >> sys.stderr, 'server is starting on %s port %s' % serverAddress

		username = pduResult.content.strip().split(";")[0]
		serverId = pduResult.content.strip().split(";")[1]
		serverUrl = pduResult.content.strip().split(";")[2]
		isDuplicate = findDuplicateName(username, serverId)

		if (isDuplicate == False):
			content = 'http://localhost:10001/session/%s/%s' % (serverUrl, username)
			component = (200, content, "text/plain")
			sendResponse(conn, component)
		else:
			content = "Given username is already in use."
			component = (422, content, "text/plain")
			sendResponse(conn, component)

	elif (addr[1] == '_updateEndWinningCondition'):
		username = pduResult.content.strip().split(";")[0]
		roomId = pduResult.content.strip().split(";")[1]

		content = updateEndWinningCondition(username, roomId)

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	elif (addr[1] == '_updateHitPosition'):
		username = pduResult.content.strip().split(";")[0]
		roomId = pduResult.content.strip().split(";")[1]
		pos = pduResult.content.strip().split(";")[1]

		content = updateHitPosition(roomId, username, pos)

		component = (200, content, "text/plain")
		sendResponse(conn, component)


	elif (addr[1] == '_updateStatusUser'):
		username = pduResult.content.strip().split(";")[1]
		status = pduResult.content.strip().split(";")[0]
		roomId = pduResult.content.strip().split(";")[2]

		content = updateStatusUser(status, username, roomId)

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	elif (addr[1] == '_getGameStatus'):
		print >> sys.stderr, "server is called for Game Status"
		roomId = addr[2]
		content = getGameStatus(roomId)

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	elif (addr[1] == '_getUsernamePosition'):
		roomId = addr[2]
		username = addr[3]
		content = json.dumps(getGameUsernamePosition(roomId, username))

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	elif (addr[1] == '_createGame'):
		username = pduResult.content.strip().split(";")[0]
		serverId = pduResult.content.strip().split(";")[1]
		serverUrl = pduResult.content.strip().split(";")[2]
		tiles = pduResult.content.strip().split(";")[3]
		player = pduResult.content.strip().split(";")[4]

		gameCreated = common.createGameRoom(tiles, player, serverId, username)

		if (gameCreated > 0):
			content = 'http://localhost:10001/game/%s/%s/%s' % (serverUrl, username, gameCreated)
			component = (200, content, "text/plain")
			sendResponse(conn, component)

	elif (addr[1] == '_joinGame'):
		username = pduResult.content.strip().split(";")[1]
		gameId = pduResult.content.strip().split(";")[0]

		content = joinGame(gameId, username)

		component = (200, content, "text/plain")
		sendResponse(conn, component)


	elif (addr[1] == '_saveGamePosition'):
		data = pduResult.content.strip()
		content = saveGamePosition(json.loads(data))

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	elif (addr[1] == '_getGameRooms'):
		content = common.getSessionServer(addr[2])

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	elif (addr[1] == '_getservername'):
		content = getServerName(addr[2])

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	elif (addr[1] == '_getGameInfo'):
		content = json.dumps(getGameInfo(addr[2]))

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	elif (addr[1] == '_servers'):
		content = common.getAllServers()

		component = (200, content, "text/plain")
		sendResponse(conn, component)

	else:
		fsource = '404.html'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()
		component = (404, content, mime)
		sendResponse(conn, component)

# handling response, combining content
def sendResponse(conn, component):
	template = responseHeaders[component[0]]
	data = template % (component[2], component[1])

	#print >> sys.stderr, data

	conn.sendall(data)

# parse request
def parseRequest(conn):
	data = conn.recv(4096)

	if not data:
		print >> sys.stderr, 'Bad request: no data'
		return ''

	line = data[0:data.find("\r")]

	#print line
	#header format = data[0:data.find("\r\n\r\n")]
	# print >> sys.stderr, "==================================================================="
	# print >> sys.stderr, PDU(data)
	# print >> sys.stderr, "==================================================================="

	return PDU(data)

def handler(conn, addr):
	print >> sys.stderr, 'ENTER Handler'
	# parsing uri request
	pduResult = parseRequest(conn)

	# handling URI and print suitable pages
	routingHandler(pduResult, conn, addr)

	conn.close()

# ===================================================================
# game related function here
# ===================================================================
def findDuplicateName(username, serverId):
	content = getAllUsers() # all users

	if (content != ""):
		thereIsADuplicate = False
		userInfo = json.loads(content) # all users
		users = []
		for info in userInfo: # for user in all users
			if (int(info["serverId"]) == int(serverId)):
				users = info["users"]

		if (users == []):

			newUserAndServer = {"serverId" : serverId, "users": [{"username": username, "userCreated" : int(time.time()) }] }
			userInfo.append(newUserAndServer)


		else:
			for user in users:
				if (user["username"] == username):
					thereIsADuplicate = True

			if (thereIsADuplicate == False):
				newUser = {"username": username, "userCreated" : int(time.time()) }
				for info in userInfo:
					if (int(info["serverId"]) == int(serverId)):
						users.append(newUser)


		content = json.dumps(userInfo)
		fsource = 'users.json'
		f = open(fsource, 'w')
		f.write(content)
		f.close()

		return thereIsADuplicate

	else:
		#empty json file, proceed to create initial content
		data = [{"serverId" : serverId, "users": [{"username": username, "userCreated" : int(time.time()) }] }]
		content = json.dumps(data)

		fsource = 'users.json'
		f = open(fsource, 'w')
		f.write(content)
		f.close()

		return False

	print >> sys.stderr, 'RETURNING NONE'

def updateEndWinningCondition(username, roomId):
	print >> sys.stderr, "updateEndWinningCondition ENTERED"
	sessions = json.loads(common.getAllSessions())
	print >> sys.stderr, "sessions LOADED"
	for session in sessions:
		if (int(session['gameRoomId']) == int(roomId)):
			print >> sys.stderr, "gameRoomId is found to equal roomID"
			session["isEnded"] = True
			print >> sys.stderr, "setting 1"
			session["isPlaying"] = False
			print >> sys.stderr, "setting 2"
			for user in session['users']:
				if (user['username'] == username):
					user['isWinning'] = True
					print >> sys.stderr, "evaluation 3"

	sessionData = json.dumps(sessions)
	fsource = 'sessions.json'
	f = open(fsource, 'w')
	f.write(sessionData)
	f.close()

	return True

def updateHitPosition(roomId, username, pos):

	#TODO create record to keep map position in where the user getting hit

	fsource = 'hits.json'
	f = open(fsource, 'r')
	content = f.read()
	f.close()

	allPlayersAllHits = []

	if content == '':
		allPlayersAllHits.append({'username': username, 'gameRoomId': roomId, 'hits': [{{"postion": pos}}]})
	else:
		allPlayersAllHits = json.loads(content)
		playerFiredOnPreviously = False
		for player in allPlayersAllHits:
			if player["username"] == username and int(player["gameRoomId"]) == int(roomId):
				player["hits"].append({"postion": pos})
				playerFiredOnPreviously = True

		if playerFiredOnPreviously == False:
			allPlayersAllHits.append({'username': username, 'gameRoomId': roomId, 'hits': [{{"postion": pos}}]})

	hitsData = json.dumps(allPlayersAllHits)
	fsource = 'hits.json'
	f = open(fsource, 'w')
	f.write(hitsData)
	f.close()

	return True


def getHitPosition(roomId):

	#TODO return all users and position where they got hit

	fsource = 'hits.json'
	f = open(fsource, 'r')
	content = f.read()
	f.close()

	allPlayersInRoom = []

	if content != '':
		allPlayers = json.loads(content)
		for player in allPlayers:
			if int(player["gameRoomId"]) == int(roomId):
				allPlayersInRoom.append(player)


	return allPlayersInRoom

def updateUserTurn(username, roomId):

	sessions = json.loads(common.getAllSessions())
	for session in sessions:
		if session["gameRoomId"] == roomId:
			for user in session["users"]:
				if user["username"] == username:
					user["isTurn"] = True
				else:
					user["isTurn"] = False

	sessionData = json.dumps(sessions)
	fsource = 'sessions.json'
	f = open(fsource, 'w')
	f.write(sessionData)
	f.close()

	return True

def updateDefeatedUser(username, roomId):

	#TODO, in sessions.json change isDefeated of this username to true

	return True

def joinGame(gameId, username):
	game = getGameInfo(gameId)
	sessions = common.getAllSessions()
	if (len(game["users"]) < game["numPlayers"]):
		userJoiningGame = {"username": username, "isWinning": False, "isTurn": False, "isDefeated": False, "isPlaying": False}
		games = json.loads(sessions)
		for game in games:
			if (int(game['gameRoomId']) == int(gameId)):
				game["users"].append(userJoiningGame)
		dataObject = json.dumps(games)
		fsource = 'sessions.json'
		f = open(fsource, 'w')
		f.write(dataObject)
		f.close()
		print >> sys.stderr, "player space available"
		return True
	else:
		print >> sys.stderr, "player space unavailable"
		return False

def updateStatusUser(status, username, roomId):

	sessions = json.loads(common.getAllSessions())
	usernameFoundAndChanged = False
	for session in sessions:
		if (int(session['gameRoomId']) == int(roomId)):
			for user in session['users']:
				if (user['username'] == username):
					user['isPlaying'] = True
					usernameFoundAndChanged = True

	sessionData = json.dumps(sessions)
	fsource = 'sessions.json'
	f = open(fsource, 'w')
	f.write(sessionData)
	f.close()

	if (usernameFoundAndChanged):
		print >> sys.stderr, "User\'s status is updated."
		return True
	else:
		print >> sys.stderr, "User\'s status failure."
		return False


def getGameStatus(roomId):
	print >> sys.stderr, "getGameStatus called"
	game = getGameInfo(roomId)
	if (len(game["users"]) != int(game["numPlayers"])):
		print >> sys.stderr, "max players not started"
		return False
	for user in game["users"]:
		if (user["isPlaying"] == False):
			print >> sys.stderr, "there is a user who is not playing"
			return False

	print >> sys.stderr, "game is ready"

	games = json.loads(common.getAllSessions())
	for g in games:
		if (int(g['gameRoomId']) == int(roomId)):
			g["isPlaying"] = True

	gameData = json.dumps(games)
	fsource = 'sessions.json'
	f = open(fsource, 'w')
	f.write(gameData)
	f.close()

	return True


def saveGamePosition(obj):
	game = getGamePosition(obj['gameId'])
	content = getAllGamePosition()

	if (content != ''):
		games = json.loads(content)
		if (game != None):

			print >> sys.stderr, "game.json add more users"

			data = { "username" : obj['username'], "position" : obj['ships'] }
			game['users'].append(data)

			for room in games:
				if (int(room['gameRoomId']) == int(obj['gameId'])):
					room['users'] = game['users']

			dataObject = json.dumps(games)

			fsource = 'game.json'
			f = open(fsource, 'w')
			f.write(dataObject)
			f.close()

		else:

			print >> sys.stderr, "game.json room id is not exist"

			data = {"gameRoomId" : obj['gameId'], "users" : [{ "username" : obj['username'], "position" : obj['ships'] }] }
			games.append(data)

			dataObject = json.dumps(games)

			fsource = 'game.json'
			f = open(fsource, 'w')
			f.write(dataObject)
			f.close()

	else :
		print >> sys.stderr, "game.json is empty, so creating it"

		data = [{"gameRoomId" : obj['gameId'], "users" : [{ "username" : obj['username'], "position" : obj['ships'] }] }]
		dataObject = json.dumps(data)

		fsource = 'game.json'
		f = open(fsource, 'w')
		f.write(dataObject)
		f.close()

	return True

def getGameInfo(roomId):
	print roomId
	games = json.loads(common.getAllSessions())
	for game in games:
		if (int(game['gameRoomId']) == int(roomId)):
			return game

def getServerName(url):
	servers = json.loads(common.getAllServers())

	for server in servers:
		if (server['serverUrl'] == url):
			return json.dumps(server)

def getGameUsernamePosition(gameId, username):
	content = getGamePosition(gameId)
	for user in content['users']:
		if user['username'] == username:
			print >> sys.stderr, 'returning user\'s ship positions:'
			print >> sys.stderr, str(user['position'])
			return user['position']

	return None

def getGamePosition(gameId):
	content = getAllGamePosition()

	if (content != ''):
		data = json.loads(content)

		for datum in data:
			if (int(datum['gameRoomId']) == int(gameId)):
				return datum
		return None
	else:
		return None

def getAllGamePosition():
	fsource = 'game.json'
	f = open(fsource, 'r')
	content = f.read()
	f.close()

	return content

def getAllUsers():
	fsource = 'users.json'
	f = open(fsource, 'r')
	content = f.read()
	f.close()

	return content

# ===================================================================
# main application here
# ===================================================================
def main():

	server = socketServer(serverAddress)
	print >> sys.stderr, 'server is starting on %s port %s' % serverAddress

	#connected
	try:
		while True:
			conn, addr = server.accept()

			# king connected client ip address
			print >> sys.stderr, 'client connected with ip :  %s' % str(addr)

			#start threading
			thrd = threading.Thread(target=handler, args=(conn, addr))

			try:
				thrd.start()
			except:
				print >> sys.stderr, 'exit thread'
				thrd.exit()

	# handling keyboard interrupt
	except KeyboardInterrupt:
		print >> sys.stderr, 'keyboardInterrupt exception'


	server.close()


if __name__ == '__main__':
    main()
