'''
Created on 05.06.2011

@author: moritz
'''

'''
The LightWeightProtocol works according to the following specification.
1. Server CO_NO (unconnected), client CO_NO
2. Client connects
3.a on connection server: server is in CO_OK; server sends UID to client
    From now on, all messages by client have to be superceeded by correct
    uid, otherwise they will just be disregarded by the server
3.b on connection client: client is in CO_OK
4. client receives and saves UID, replies with channel name, client in CH_SEND
5. server acknowledges channel with reply, server in CH_IN
6. client receives reply, client in CH_IN
Nb. This essentially represent a three-way handshake.
'''

# this resembles a C-style enum for our state machine
class ProtocolState:
    CO_NO=0
    CO_OK=1
    CH_SENT=2
    CH_IN=3
