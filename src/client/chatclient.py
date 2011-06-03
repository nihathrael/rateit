import socket
import sys
import select
import cPickle
import socket
import struct
from threading import Thread

marshall = cPickle.dumps
unmarshall = cPickle.loads

BUFSIZ = 1024

class ChatClient(Thread):
    """ A simple command line chat client using select """

    def __init__(self, name, host='localhost', port=8080):
        super(ChatClient, self).__init__()
        self.name = name
        # Quit flag
        self.flag = False
        self.port = int(port)
        self.host = host
        # Initial prompt
        self.prompt='[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']> '
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print 'Connected to chat server@%d' % self.port
            self.prompt = '[' + '@' + self.name + ']> '
        except socket.error, e:
            print 'Could not connect to chat server @%d' % self.port
            sys.exit(1)

    def run(self):
        print "run"
        while not self.flag:
            print "while..."
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

    def send(self, text):
        print "send"
        sockFile = self.sock.makefile()
        sockFile.write(text + "\n")
        sockFile.flush()

    def receive(self):
        print "receive"
        sockFile = self.sock.makefile()
        buf = sockFile.readline()
        print "buf"
        return buf
