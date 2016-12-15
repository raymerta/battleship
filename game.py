#!/usr/bin/env python

import pika
import common
import json


#get list of servers for pushing content
def getMQGamesList():
	games = []
	servers = json.loads(common.getAllServers())

	for server in servers: 
		games.append("game-%s" % server['serverUrl'])

	return games

def getMQServerList():
	games = []
	servers = json.loads(common.getAllServers())

	for server in servers: 
		games.append("server-%s" % server['serverUrl'])

	return games

def updateSession():
	sessions = {}
	servers = json.loads(common.getAllServers())

	for server in servers:
		sessionName = ("game-%s") % server['serverUrl']
		serverId = int(server['serverId'])

		sessions[sessionName] = common.getSessionServer(serverId)

	return sessions

serverContent = ''
sessionContent = updateSession()

# rabbitmq credentials
mq_creds  = pika.PlainCredentials(username = "guest", password = "guest")

# rabbitmq parameters
mq_params = pika.ConnectionParameters(host = "localhost", credentials = mq_creds, virtual_host = "/")

# amq
mq_exchange = "amq.topic"
mq_servers = "servers"
mq_games = getMQGamesList()
mq_serverListener = getMQServerList()
mq_queue = "sessions"

# connection object
mq_conn = pika.BlockingConnection(mq_params)

# This is one channel inside the connection
mq_chan = mq_conn.channel()
mq_chan.queue_declare(queue = mq_queue)

for key in mq_games:
	mq_chan.queue_bind(
		exchange = mq_exchange,
		queue = mq_queue,
   		routing_key = key)

for key in mq_serverListener:
	mq_chan.queue_bind(
		exchange = mq_exchange,
		queue = mq_queue,
   		routing_key = key)

def callback(ch, method, properties, body):
    print("%r:%r" % (method.routing_key, body))
    destination = method.routing_key.split("-")[0]

    sessions = updateSession()

    for key in mq_games: 
    	if (sessions[key] != sessionContent[key]):
    		print key
    		sessionContent[key] = sessions[key]
    		mq_chan.basic_publish(
				exchange    = mq_exchange,
				routing_key = key,
    			body        = sessionContent[key])

    ## TODO REFACTOR ALL REDUNDANT HTTP POST

  #   if (destination == "server"):
  #   	username = body.strip().split(";")[0]
		# serverId = body.strip().split(";")[1]
		# serverUrl = body.strip().split(";")[2]
		# tiles = body.strip().split(";")[3]
		# player = body.strip().split(";")[4]

		# gameCreated = common.createGameRoom(tiles, player, serverId, username)

		# if (gameCreated > 0):
		# 	content = 'http://localhost:10001/game/%s/%s/%s' % (serverUrl, username, gameCreated)
		# 	mq_chan.basic_publish(
		# 	exchange    = mq_exchange,
		# 	routing_key = mq_servers,
  #   		body        = serverContent)


mq_chan.basic_consume(callback,
        queue=mq_queue,
		no_ack=True)

mq_chan.start_consuming()




