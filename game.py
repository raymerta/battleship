#!/usr/bin/env python

import pika
import common
import json

#get list of servers for pushing content
def getMQGamesList():
	games = {}
	servers = json.loads(common.getAllServers())

	for server in servers: 
		games.append("game-%s" % server['serverUrl'])

	return games

# rabbitmq credentials
mq_creds  = pika.PlainCredentials(username = "guest", password = "guest")

# rabbitmq parameters
mq_params = pika.ConnectionParameters(host = "localhost", credentials = mq_creds, virtual_host = "/")

# amq
mq_exchange = "amq.topic"
mq_servers = "servers"
mq_games = getMQGamesList()

# connection object
mq_conn = pika.BlockingConnection(mq_params)

# This is one channel inside the connection
mq_chan = mq_conn.channel()

serverContent = ''

while True:
	servers = common.getAllServers()

	if (serverContent != servers):
		print "new content"

		serverContent = servers;
		mq_games = getMQGamesList()

		mq_chan.basic_publish(
			exchange    = mq_exchange,
			routing_key = mq_servers,
    		body        = serverContent)



