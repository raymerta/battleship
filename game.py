#!/usr/bin/env python

import pika
import common
import json

# rabbitmq credentials
mq_creds  = pika.PlainCredentials(username = "guest", password = "guest")

mq_params = pika.ConnectionParameters(host = "localhost", credentials = mq_creds, virtual_host = "/")

# amq
mq_exchange = "amq.topic"
mq_servers = "servers"

# connection object
mq_conn = pika.BlockingConnection(mq_params)

# This is one channel inside the connection
mq_chan = mq_conn.channel()

content = ''

while True:
	servers = common.getAllServers()

	if (content != servers):
		print "new content"
		content = servers;
		mq_chan.basic_publish(
			exchange    = mq_exchange,
			routing_key = mq_servers,
    		body        = content)
