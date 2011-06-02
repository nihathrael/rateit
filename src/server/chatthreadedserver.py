from SocketServer import TCPServer, ThreadingMixIn

from messageroom import MessageRoom
from chatrequesthandler import ChatRequestHandler
class ChatThreadedServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = 1

    def __init__(self, server_address, request_handler_class):
        TCPServer.__init__(self, server_address, request_handler_class)
        self._chat_room = MessageRoom()
        self._chat_room.setDaemon(1)
        self._chat_room.start()

    def shutdown(self):
        self._chat_room.shutdown()