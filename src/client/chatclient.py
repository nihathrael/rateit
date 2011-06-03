import socket
import sys
import select
import cPickle
import socket
import struct

import utils.settings

marshall = cPickle.dumps
unmarshall = cPickle.loads

BUFSIZ = 1024

class ChatClient(object):
    """ A simple command line chat client using select """

    def __init__(self):
        super(ChatClient, self).__init__()
        # Quit flag
        self.flag = False
        self.connected = False
        # Initial prompt
        self.prompt = ">"

    def connect(self, url):
        host, port = url.split(":")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, int(port)))
            print 'Connected to chat server@%d' % int(port)
            self.prompt = '[' + '@' + utils.settings.a.name + ']> '
            self.connected = True
        except socket.error, e:
            print 'Could not connect to chat server @%d' % int(port)
            
    # Tear down connection
    def disconnect(self):
        self.sock.close()
        self.connected = False

    def run(self):
        print "run"
        while not self.flag:
            if self.connected:
                try:
                    sys.stdout.write(self.prompt)
                    sys.stdout.flush()

                    # Wait for input from stdin & socket
                    print "Before select"
                    inputready, outputready,exceptrdy = select.select([0, self.sock], [],[])
                    print "after select"

                    for i in inputready:
                        if i == 0:
                            data = sys.stdin.readline().strip()
                            if data: self.send(data)
                        elif i == self.sock:
                            data = self.receive()
                            if not data:
                                print 'Shutting down.'
                                self.flag = True
                                break
                            else:
                                sys.stdout.write(data + '\n')
                                sys.stdout.flush()

                except:
                    print 'Interrupted.'
                    self.sock.close()
                    break
        print "endrun"
        
    # Terminate thread
    def quit(self):
        if self.connected:
            self.disconnect()
        self.flag = True

    def send(self, text):
        if self.connected:
            print "send"
            sockFile = self.sock.makefile()
            sockFile.write(text + "\n")
            sockFile.flush()

    def receive(self):
        if self.connected:
            print "receive"
            sockFile = self.sock.makefile()
            buf = sockFile.readline()
            print "buf"
            return buf
