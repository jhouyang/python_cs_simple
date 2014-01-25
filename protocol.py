#!/usr/bin/env python

'''Define protocol about how to send and recv message
between server and client.
   And the protocol should be (big end):
   messages : type, size of data, data 
   size     : 4,    unkown      , unkown
   type     : string, int,        string
'''
import struct

class ProtoCol(object):
    '''define some types and send message
    '''
    ERROR, INFO, RESP, CLOSE = ('err ', 'inf ', 'res ', 'clo ')
    @classmethod
    def send_response(sock, msg):
        send_msg = struct.pack('>4si%ds', ProtoCol.RESP, len(msg), msg)
        sock.sendall(send_msg)

    @classmethod
    def send_info(sock, msg):
        send_msg = struct.pack('>4si%ds', ProtoCol.INFO, len(msg), msg)
        sock.sendall(send_msg)

    @classmethod
    def send_error(sock, msg):
        send_msg = struct.pack('>4si%ds', ProtoCol.ERROR, len(msg), msg)
        sock.sendall(send_msg)

    @classmethod
    def send_close(sock, msg):
        send_msg = struct.pack('>4si%ds', ProtoCol.CLOSE, len(msg), msg)
        sock.sendall(send_msg)


