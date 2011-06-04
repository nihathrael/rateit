'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import pynotify

import utils.settings
import gui.notification

class RateItClient(Protocol):
    def sendMessage(self, msg):
        if self.connected:
            self.transport.write("%s\n" % msg)
            
    def dataReceived(self, data):
        gui.notification.showNotification(data)
        
    def connectionMade(self):
        self.transport.write(utils.settings.a.name + " joined RateIt!\r\n")
    
            
# An implementation of a factory is needed as we need to store a reference 
# to the actual RateItClient object, otherwise we won't be able to delegate 
# method calls to it
class RateItFactory(ReconnectingClientFactory):
    protocol = RateItClient
    
    def __init__(self):
        self.obj = self.protocol()
    
    def buildProtocol(self, addr):
        self.obj = ReconnectingClientFactory.buildProtocol(self, addr)
        return self.obj
    
    # works via delegation
    def send(self, msg):
        self.obj.sendMessage(msg)
        
    def loseConnection(self):
        self.obj.transport.loseConnection()
                

class TwistedClient():
    def __init__(self):
        pynotify.init("RateIt Notifications")
        self.factory = RateItFactory()

    def connect(self, url):
        host, port = url.split(":")
        reactor.connectTCP(host, int(port), self.factory)
    
    # works via delegation        
    def send(self, msg):
        self.factory.send(msg)
                
    def quit(self):
        self.factory.loseConnection()
        
