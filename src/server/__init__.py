from twistedserver import RateServerFactory

from twisted.internet import reactor

if __name__ == '__main__':
		reactor.listenTCP(8080, RateServerFactory())
		reactor.run()
