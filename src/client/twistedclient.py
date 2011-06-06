'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import pynotify

import utils.settings
import gui.guiutils

import re

import uuid 

from  protocol.protocolstates import ProtocolState 

class RateItClient(Protocol):
    def __init__(self):
        self.curState=ProtocolState.CO_NO
        self.id=None
        
    def sendMessage(self, msg):
        if self.connected:
            self.transport.write("%s:%s" % (self.id, msg))
            
    def dataReceived(self, data):
        data = data.rstrip()
        
        if self.curState == ProtocolState.CH_IN:
            gui.guiutils.GuiUtils.showNotification(data)
        elif self.curState == ProtocolState.CO_OK:
            self.transport.write(str(self.id))
            self.curState = ProtocolState.AUTH_OK
        elif self.curState == ProtocolState.AUTH_OK:
            # pass on channel to join
            self.sendMessage("stabi")
            self.curState = ProtocolState.CH_SENT
        elif self.curState == ProtocolState.CH_SENT:
            self.sendMessage(utils.settings.a.name + " joined RateIt!\r\n")
            self.curState = ProtocolState.CH_IN
        
    def connectionMade(self):
        self.curState=ProtocolState.CO_OK
        if self.id == None:
            self.id = uuid.uuid1()
        self.transport.write("UID: " + str(self.id))
        
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
        
