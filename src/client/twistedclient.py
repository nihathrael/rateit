'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
import pynotify

import utils.settings
import gui.guiutils


from  protocol.protocolstates import ProtocolState 

class RateItClient(Protocol):
    def __init__(self):
        self.curState=ProtocolState.CO_NO
        self.id=utils.settings.a.id
        
    def sendMessage(self, msg):
        if self.connected:
            self.transport.write("%s:%s" % (self.id, msg))
            
    def dataReceived(self, data):
        data = data.rstrip()
        
        if self.curState == ProtocolState.CH_IN:
            gui.guiutils.GuiUtils.showNotification(data)
        elif self.curState == ProtocolState.CO_OK:
            self.transport.write("UID: " + str(self.id))
            self.curState = ProtocolState.AUTH_OK
        elif self.curState == ProtocolState.AUTH_OK:
            # pass on channel to join
            self.sendMessage(utils.settings.a.channel)
            self.curState = ProtocolState.CH_SENT
        elif self.curState == ProtocolState.CH_SENT:
            self.sendMessage(utils.settings.a.name + " joined RateIt!\r\n")
            self.curState = ProtocolState.CH_IN
        
    def connectionMade(self):
        self.curState=ProtocolState.CO_OK

        
    def connectionLost(self, reason):
        Protocol.connectionLost(self, reason=reason)
        self.curState=ProtocolState.CO_NO
    
            
# An implementation of a factory is needed as we need to store a reference 
# to the actual RateItClient object, otherwise we won't be able to delegate 
# method calls to it
class RateItFactory(ClientFactory):
    protocol = RateItClient
    
    def __init__(self):
        self.obj = self.protocol()
    
    def buildProtocol(self, addr):
        self.obj = ClientFactory.buildProtocol(self, addr)
        return self.obj
    
    # works via delegation
    def send(self, msg):
        self.obj.sendMessage(msg)
        
    def loseConnection(self):
        if self.obj.transport:
            self.obj.transport.loseConnection()
                

class TwistedClient():
    def __init__(self):
        pynotify.init("RateIt Notifications")
        self.factory = RateItFactory()

    def connect(self):
        host, port = utils.settings.a.server.split(":")
        reactor.connectTCP(host, int(port), self.factory)
    
    # works via delegation        
    def send(self, msg):
        self.factory.send(msg)
                
    def quit(self):
        self.factory.loseConnection()
        
