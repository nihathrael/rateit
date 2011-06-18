'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from  protocol.protocolstates import ProtocolState 

import re

class LightWeightProtocol(Protocol):
    def __init__(self):
        self.curState=ProtocolState.CO_NO
        self.channel=None
        self.id=None
          
    def connectionMade(self):
        self.curState=ProtocolState.CO_OK
        self.transport.write("Connect ok")
        print "And another successful connection established"
        
    def extractData(self, message):    
        (sid, a, data) = message.partition(':')
        return data
    
    def isValidId(self, message):
        # UUID never has : as a character, so first : must be delimiter
        (sid, a, text) = message.partition(':')
        if sid == str(self.id):
            return True
        else:
            return False
            
    def connectionLost(self, reason):
        # remove from channel and disconnect, reset state machine
        if self in self.factory.channels[self.channel]: 
            self.factory.channels[self.channel].remove(self)
        if self.factory.channels[self.channel].count <= 0:
            del self.factory.channels[self.channel]
        self.curState=ProtocolState.CO_NO
        self.factory.notifyObservers("A dude left the channel", self.channel)
        Protocol.connectionLost(self, reason=reason)
            
    def joinChannel(self, channelName):
        if channelName in self.factory.channels:
            # channel already exists, join existing channel
            self.factory.channels[channelName].append(self)
            self.channel = channelName
        else:
            # channel does not exist, create new channel and join it
            self.factory.channels[channelName] = []
            self.joinChannel(channelName)
            
    def dataReceived(self, data):
        data = data.rstrip()
        
        if self.curState == ProtocolState.CO_NO:
            # disregard any incoming commands while not properly connected
            # (should never happen usually)
            return        
        elif self.curState == ProtocolState.CO_OK:
            parser = re.compile("UID: (.*)")
            match = parser.match(data)
            self.id = match.group(1)
            # TODO: check for id more closely
            if self.id != '':
                self.curState = ProtocolState.AUTH_OK
                self.transport.write("AUTH OK, CHANNEL?")
                return
            else:
                self.transport.loseConnection()
                return
        
        # from now on, a handshaken UID is known to client and server
        # all communication must be preceeded by this UID
        if not self.isValidId(data):
            self.transport.loseConnection()
            return
        data = self.extractData(data)
        
        if self.curState == ProtocolState.AUTH_OK:
            self.joinChannel(data)
            self.curState=ProtocolState.CH_IN
            self.transport.write("Joined channel " + data)
        elif self.curState == ProtocolState.CH_IN:
            # notify all observers of incoming event
            self.factory.notifyObservers(data, self.channel)

class RateServerFactory(Factory):
    protocol = LightWeightProtocol
    
    def __init__(self):
        self.channels = {}
        
    def notifyObservers(self, data, channel):
        for aClient in self.channels[channel]:
            aClient.transport.write(data)
