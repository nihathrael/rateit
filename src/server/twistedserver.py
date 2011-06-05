'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from  protocol.protocolstates import ProtocolState 

import uuid 

class LightWeightProtocol(Protocol):
    def __init__(self):
        self.curState=ProtocolState.CO_NO
        self.channel=None
        self.id=None
          
    def connectionMade(self):
        self.curState=ProtocolState.CO_OK
        self.id = uuid.uuid4()
        self.transport.write("ID: " + str(self.id))
        print "And another successful connection established"
        
    def checkId(self, message):
        # UUID never has : as a character, so first : must be 
        (sid, a, text) = message.partition(':')
        if sid == str(self.id):
            return text
        else:
            return False
            
    def connectionLost(self, reason):
        # remove from channel and disconnect, reset state machine
        self.factory.channels[self.channel].remove(self)
        if self.factory.channels[self.channel].count <= 0:
            del self.factory.channels[self.channel]
        self.curState=ProtocolState.CO_NO
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
        
        message = self.checkId(data)
        if message == False:
            return
        
        if self.curState == ProtocolState.CO_OK:
            self.joinChannel(data)
            self.curState=ProtocolState.CH_IN
            self.transport.write("Joined channel " + data)
        elif self.curState == ProtocolState.CH_IN:
            # notify all observers of incoming event
            self.factory.notifyObservers(message, self.channel)

class RateServerFactory(Factory):
    protocol = LightWeightProtocol
    
    def __init__(self):
        self.channels = {}
        
    def notifyObservers(self, data, channel):
        for aClient in self.channels[channel]:
            aClient.transport.write(data)
