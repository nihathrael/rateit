'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import pynotify

import utils.settings
import gui.guiutils

# this resembles a C-style enum for our state machine
class ProtocolState:
    CO_NO=0
    CO_OK=1
    CH_SENT=2
    CH_IN=3

class RateItClient(Protocol):
    def __init__(self):
        self.curState=ProtocolState.CO_NO
        
    def sendMessage(self, msg):
        if self.connected:
            self.transport.write("%s\n" % msg)
            
    def dataReceived(self, data):
        if self.curState == ProtocolState.CH_IN:
            gui.guiutils.GuiUtils.showNotification(data)
        elif self.curState == ProtocolState.CO_OK:
            # pass on channel to join
            self.transport.write("stabi")
            self.curState = ProtocolState.CH_SENT
        elif self.curState == ProtocolState.CH_SENT:
            self.transport.write(utils.settings.a.name + " joined RateIt!\r\n")
            self.curState = ProtocolState.CH_IN
        
    def connectionMade(self):
        self.curState=ProtocolState.CO_OK
        
    def connectionLost(self, reason):
        Protocol.connectionLost(self, reason=reason)
        self.curState=ProtocolState.CO_NO
    
            
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
        
