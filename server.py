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
# TODO Handling local CSS and Javascript file

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

# handling routing TODO
def routingHandler(pduResult, conn, addr):

	# remove beginning /
	addr = pduResult.uri.split('/')

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



	elif (addr[1] == '_createGame'):
		username = pduResult.content.strip().split(";")[0]
		serverId = pduResult.content.strip().split(";")[1]
		serverUrl = pduResult.content.strip().split(";")[2]
		tiles = pduResult.content.strip().split(";")[3]
		player = pduResult.content.strip().split(";")[4]

		gameCreated = createGameRoom(tiles, player, serverId, username)

		if (gameCreated > 0):
			content = 'http://localhost:10001/game/%s/%s/%s' % (serverUrl, username, gameCreated)
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
		content = getGameInfo(addr[2])

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
	# parsing uri request
	pduResult = parseRequest(conn)

	# handling URI and print suitable pages
	routingHandler(pduResult, conn, addr)

	conn.close()

# ===================================================================
# game related function here
# ===================================================================

# todo fix this part
def findDuplicateName(username, serverId):
	content = getAllUsers()

	if (content != ""):
		thereIsADuplicate = False
		userInfo = json.loads(content)
		users = []
		for info in userInfo:
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

gameRoomName = ['Atlantic Ocean', 'Arctic Ocean', 'Indian Ocean', 'Pacific Ocean', 'Norwegian Sea', 'North Sea', 'Aegean Sea', 'Southern Ocean', 'Arabian Sea', 'East China Sea']

def createGameRoom(tiles, player, serverId, username):
	content = common.getAllSessions()

	# generate random game room name
	roomType = random.randint(0, (len(gameRoomName) - 1))
	roomName = gameRoomName[roomType]

	if (content != ""):
		sessions = json.loads(content)
		roomId = len(sessions) + 1

		data = {"serverId" : serverId, "numPlayers" : player, "size" : tiles, "creator": username , "roomName": roomName, "roomCreated": int(time.time()), "isPlaying": False, "isEnded" : False , "gameRoomId" : roomId, "users": [{"username": username, "isTurn" : False, "isDefeated" : False, "isWinning" : False, "isEditing" : True }] }
		sessions.append(data)

		dataObject = json.dumps(sessions)

		fsource = 'sessions.json'
		f = open(fsource, 'w')
		f.write(dataObject)
		f.close()

		return roomId

	else:
		#empty json file, proceed to create initial content
		data = [{"serverId" : serverId, "numPlayers" : player, "size" : tiles, "creator": username , "roomName": roomName, "roomCreated": int(time.time()), "isPlaying": False, "isEnded" : False , "gameRoomId" : 1, "users": [{"username": username, "isTurn" : False, "isDefeated" : False, "isWinning" : False, "isEditing" : True }] }]
		dataObject = json.dumps(data)

		fsource = 'sessions.json'
		f = open(fsource, 'w')
		f.write(dataObject)
		f.close()

		#return user ID number
		return 1

def getGameInfo(roomId):
	print roomId
	games = json.loads(common.getAllSessions())
	for game in games:
		print game
		if (int(game['gameRoomId']) == int(roomId)):
			print game
			return json.dumps(game)

def getServerName(url):
	servers = json.loads(common.getAllServers())

	for server in servers:
		if (server['serverUrl'] == url):
			return json.dumps(server)


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

			# checking connected client ip address
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
