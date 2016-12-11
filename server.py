import socket
import threading
import os
import sys
import random
import time

serverAddress = ('localhost', 10001)

from PDU import PDU

# setting up response header
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

	print >> sys.stderr, data

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
	print pduResult.content
	#print >> sys.stderr, 'URI accessed : %s' % pduResult.uri

	# handling URI and print suitable pages
	routingHandler(pduResult, conn, addr)

	conn.close()


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
