from chatthreadedserver import ChatThreadedServer
from chatrequesthandler import ChatRequestHandler

import sys
import pynotify

if __name__ == '__main__':
	server = ChatThreadedServer(('localhost', 8080), ChatRequestHandler)

	if not pynotify.init("Timekpr notification"):
		sys.exit(1)

	try:
		print "Server starting.  Now waiting."
		server.serve_forever()
	except:
		server.shutdown()
		print "Shutting down... waiting for all clients to close."
