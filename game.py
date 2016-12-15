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

def updateSession():
	sessions = {}
	servers = json.loads(common.getAllServers())

	for server in servers:
		sessionName = ("game-%s") % server['serverUrl']
		serverId = int(server['serverId'])

		sessions[sessionName] = common.getSessionServer(serverId)

	return sessions

# rabbitmq credentials
mq_creds  = pika.PlainCredentials(username = "guest", password = "guest")

# rabbitmq parameters
mq_params = pika.ConnectionParameters(host = "localhost", credentials = mq_creds, virtual_host = "/")

# amq
mq_exchange = "amq.topic"
mq_servers = "servers"
mq_games = getMQGamesList()
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

def callback(ch, method, properties, body):
    print("%r:%r" % (method.routing_key, body))

mq_chan.basic_consume(callback,
        queue=mq_queue,
		no_ack=True)

mq_chan.start_consuming()

serverContent = ''
sessionContent = updateSession()

# while True:
# 	servers = common.getAllServers()

# 	if (serverContent != servers):
# 		print "new content"

# 		serverContent = servers
# 		mq_games = getMQGamesList()

# 		mq_chan.basic_publish(
# 			exchange    = mq_exchange,
# 			routing_key = mq_servers,
#     		body        = serverContent)

# 	#stupid way to update session
# 	sessions = updateSession()
# 	for key in mq_games: 
# 		if (sessions[key] != sessionContent[key]):
# 			print key

# 			sessionContent[key] = sessions[key]
# 			mq_chan.basic_publish(
# 				exchange    = mq_exchange,
# 				routing_key = key,
#     			body        = sessionContent[key])


