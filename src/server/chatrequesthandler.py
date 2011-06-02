import SocketServer
class ChatRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.sendWelcome()
        server = self.server
        while 1:
            ## fixme: add notification of server shutdown
            line = self.rfile.readline()
            if not line:
                break
            if line.rstrip().startswith('/quit'):
                break
            if line.rstrip():
                formatted_msg = "[%s]: %s\n" % \
                                (self.client_address, line.rstrip())
                server._chat_room.shout(formatted_msg)


    def sendWelcome(self):
        self.wfile.write("""
Welcome %s!
Type '/quit' to quit

""" %  str(self.client_address))

    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.server._chat_room.addListener(self._writeMsg)
        print "%s connected." % (self.client_address,)


    def finish(self):
        self.server._chat_room.removeListener(self._writeMsg)
        SocketServer.StreamRequestHandler.finish(self)
        print "%s disconnected." % (self.client_address,)


    def _writeMsg(self, msg):
        self.wfile.write(msg)
