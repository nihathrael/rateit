from threading import *
from Queue import Queue

class MessageRoom(Thread):
    """This class simulates a room full of people, where messages
shout()ed out will broadcast to everyone else in the room.

TODO: add more documentation!
"""
    def __init__(self):
        Thread.__init__(self)
        self._message_queue = Queue()
        self._listeners = []
        self._listeners_lock = RLock()
        self._shutdown = 0
        self._events = Queue()


    def shout(self, msg):
        """Shout out a message to all listeners."""
        self._message_queue.put(msg)
        self._events.put("message added")


    def addListener(self, listener):
        """Adds a callable 'listener' to our list of active listeners."""
        self._listeners_lock.acquire()
        try:
            self._listeners.append(listener)
        finally:
            self._listeners_lock.release()


    def removeListener(self, listener):
        """Removes a callable 'listener' from our list of active listeners."""
        self._listeners_lock.acquire()
        try:
            self._listeners.remove(listener)
        finally:
            self._listeners_lock.release()


    def run(self):
        """Runs forever, listening to both shutdown and message shouting."""
        while 1:
            self._waitForShutdownOrNewMessages()
            if self._shutdown:
                break
            if self._message_queue.qsize():
                self._broadcastNewMessage()


    def shutdown(self):
        """Shutdown the chatroom."""
        self._shutdown = 1
        self._events.put("shutdown requested")


    def _waitForShutdownOrNewMessages(self):
        return self._events.get()


    def _broadcastNewMessage(self):
        try:
            msg = self._message_queue.get_nowait()
        except Empty:
            return
        self._listeners_lock.acquire()
        try:
            listeners_copy = self._listeners[:]
        finally:
            self._listeners_lock.release()
        for listener in listeners_copy:
            self._tryToSendMessageToListener(msg, listener)


    def _tryToSendMessageToListener(self, msg, listener):
        try:
            ## Fixme: we should somehow a timeout here.  If a message
            ## can't get through within a certain period of time, we
            ## should assume the listener is just delinquent, and toss
            ## them out of the listeners list.  Very rough, but
            ## necessary if we don't want to deadlock waiting for any
            ## particular listener.
            listener(msg)
        except:
            self.removeListener(listener)
