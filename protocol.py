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
        send_msg = struct.pack('>4si%ds'%len(msg), ProtoCol.RESP, msg)
        sock.sendall(send_msg)

    @classmethod
    def send_info(sock, msg):
        send_msg = struct.pack('>4si%ds'%len(msg), ProtoCol.INFO, msg)
        sock.sendall(send_msg)

    @classmethod
    def send_error(sock, msg):
        send_msg = struct.pack('>4si%ds'%len(msg), ProtoCol.ERROR, msg)
        sock.sendall(send_msg)

    @classmethod
    def send_close(sock, msg):
        send_msg = struct.pack('>4si%ds'%len(msg), ProtoCol.CLOSE, msg)
        sock.sendall(send_msg)


def handle_conn(sock):
    '''deserialize data,
    return tuple of type, string data
    '''
    pass

def read_info(sock):
    '''read sock data,
    return (type, data)
    '''
    init_size = 1024
    msg_raw = sock.recv(init_size)
    msg_str = struct.unpack('>4si%ds', msg_raw)


