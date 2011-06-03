import sys

from twisted.internet import gtk2reactor
gtk2reactor.install()
import twisted.internet.reactor
from twistedclient import TwistedClient
from gui.guimain import GUI

if __name__ == "__main__":
    print "starting gui"
    gui = GUI()
    gui.start()

    client = TwistedClient()
    gui.client = client
    client.run()