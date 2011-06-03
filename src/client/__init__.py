import sys

# this is a hook to allow for GTK support
from twisted.internet import gtk2reactor
gtk2reactor.install()
import twisted.internet.reactor
from twistedclient import TwistedClient
from gui.guimain import GUI

if __name__ == "__main__":

    client = TwistedClient()
    print "starting gui"
    gui = GUI()
    gui.client = client
    twisted.internet.reactor.run()
    gui.run()