import SocketServer
import pynotify
import sys

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
				self.showNotification(formatted_msg)
				server._chat_room.shout(formatted_msg)

	def showNotification(self, text):
		print "Text received:", text
		n = pynotify.Notification(text)
		n.set_urgency(pynotify.URGENCY_CRITICAL)
		n.set_timeout(15000) # 10 seconds
		n.set_category("device")

		if not n.show():
			print "Failed to send notification"
			sys.exit(1)

	def sendWelcome(self):
		print "welcome.."
		self.wfile.write("Welcome!\n")

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