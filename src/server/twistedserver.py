'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

# this resembles a C-style enum for our state machine
class ProtocolState:
    CO_NO=0
    CO_OK=1
    CH_SENT=2
    CH_IN=3

'''
The LightWeightProtocol works according to the following specification.
1. Server CO_NO (unconnected), client CO_NO
2. Client connects
3.a on connection server: server is in CO_OK; server sends invitation to channel
3.b on connection client: client is in CO_OK
4. client replies with channel name, client in CH_SEND
5. server acknowledges channel with reply, server in CH_IN
6. client receives reply, client in CH_IN
Nb. This essentially represent a three-way handshake.
'''
class LightWeightProtocol(Protocol):
    def __init__(self):
        self.curState=ProtocolState.CO_NO
        self.channel=None
          
    def connectionMade(self):
        self.curState=ProtocolState.CO_OK
        self.transport.write("Connect OK, say channel")
        print "And another successful connection established"
            
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
        if self.curState == ProtocolState.CO_NO:
            # disregard any incoming commands while not properly connected
            # (should never happen usually)
            pass
        elif self.curState == ProtocolState.CO_OK:
            self.joinChannel(data)
            self.curState=ProtocolState.CH_IN
            self.transport.write("Joined channel " + data)
        if self.curState == ProtocolState.CH_IN:
            # notify all observers of incoming event
            self.factory.notifyObservers(data.rstrip(), self.channel)

class RateServerFactory(Factory):
    protocol = LightWeightProtocol
    
    def __init__(self):
        self.channels = {}
        
    def notifyObservers(self, data, channel):
        for aClient in self.channels[channel]:
            aClient.transport.write(data)
