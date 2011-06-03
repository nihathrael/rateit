'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet import gtk2reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
import pynotify
import threading


class Greeter(Protocol):
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\n" % msg)
    def dataReceived(self, data):
        print data
        self.showNotification(data)
    def connectionMade(self):
        self.transport.write("Hello server, I am the client!\r\n")

    def showNotification(self, text):
        print "Text received:", text
        n = pynotify.Notification(text)
        n.set_urgency(pynotify.URGENCY_CRITICAL)
        n.set_timeout(15000) # 10 seconds
        n.set_category("device")
    
        if not n.show():
            print "Failed to send notification"

class ChatClient(threading.Thread):
    def __init__(self):
        super(ChatClient, self).__init__()
        pynotify.init("RateIt! Notifications")
        self.factory = Factory()
        self.factory.protocol = Greeter
        
    def connect(self, url):
        host, port = url.split(":")
        point = TCP4ClientEndpoint(gtk2reactor, host, int(port))
        self.d = point.connect(self.factory)
        
    # works via delegation
    def send(self, msg):
        self.factory.protocol.sendMessage(self, msg)
        