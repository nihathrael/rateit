import socket
import sys
import select
import cPickle
import socket
import struct
from receiverthread import ReceiverThread

marshall = cPickle.dumps
unmarshall = cPickle.loads

BUFSIZ = 1024

class ChatClient(object):
    """ A simple command line chat client using select """

    def __init__(self, name, host='localhost', port=8080):
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

        self.cmdloop()

    def cmdloop(self):
        while not self.flag:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin & socket
                inputready, outputready,exceptrdy = select.select([0, self.sock], [],[])

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

            except KeyboardInterrupt:
                print 'Interrupted.'
                self.sock.close()
                break

    def send(self, text):
        sockFile = self.sock.makefile()
        sockFile.write(text + "\n")
        sockFile.flush()

    def receive(self):
        sockFile = self.sock.makefile()
        buf = sockFile.readline()
        return buf
