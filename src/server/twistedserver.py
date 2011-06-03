'''
Created on 03.06.2011

@author: moritz
'''
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class Echo(Protocol):    
    def connectionMade(self):
        self.factory.clients.append(self)
        
        if len(self.factory.clients) > 15:
            self.transport.write("Too many connections, try later") 
            self.transport.loseConnection()
            
        print "And another successful connection established(tm)"
            
    def connectionLost(self, reason):
        Protocol.connectionLost(self, reason=reason)
        self.factory.clients.remove(self)
            
    def dataReceived(self, data):
        #delegate call to notify all observers of incoming event
        self.factory.notifyObservers(data.rstrip())

class RateServerFactory(Factory):
    protocol = Echo
    
    def __init__(self):
        self.clients = []
        
    def notifyObservers(self, data):
        for aClient in self.clients:
            aClient.transport.write(data)
    
reactor.listenTCP(8080, RateServerFactory())
reactor.run()