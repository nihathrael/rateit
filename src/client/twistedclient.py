'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
import pynotify

class RateItClient(Protocol):
    def sendMessage(self, msg):
        self.transport.write("%s\n" % msg)
    def dataReceived(self, data):
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
            
class EchoFactory(ClientFactory):
    protocol = RateItClient
    
    def __init__(self):
        self.obj = self.protocol()
    
    def buildProtocol(self, addr):
        self.obj = ClientFactory.buildProtocol(self, addr)
        return self.obj
    
    # works via delegation
    def send(self, msg):
        self.obj.sendMessage(msg)
        
                

class TwistedClient():
    def __init__(self):
        pynotify.init("RateIt! Notifications")
        self.factory = EchoFactory()

    def connect(self, url):
        host, port = url.split(":")
        reactor.connectTCP(host, int(port), self.factory)
    
    # works via delegation        
    def send(self, msg):
        self.factory.send(msg)
                
    def quit(self):
        pass
        