from chatthreadedserver import ChatThreadedServer
from chatrequesthandler import ChatRequestHandler

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1])
    server = ChatThreadedServer(('localhost', port), ChatRequestHandler)

    try:
        print "Server starting.  Now waiting."
        server.serve_forever()
    except:
        server.shutdown()
        print "Shutting down... waiting for all clients to close."