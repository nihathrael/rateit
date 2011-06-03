import sys

from chatclient import ChatClient
from  trayicon.gtktrayicon import GUI

if __name__ == "__main__":
    print "starting gui"
    gui = GUI()
    gui.start()

    client = ChatClient()
    gui.client = client
    client.run()