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
    ERROR, INFO, RESP, CLOSE, EXEC = ('erro', 'info', 'resp', 'clos', 'exec')
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
    while True:
       msg_type, msg = read_info(sock)
       if not msg_type:
          ProtoCol.send_error(sock, 'invalid input.')
       elif msg_type == ProtoCol.CLOSE:
          sock.close()
          return False
       elif msg_type == ProtoCol.EXEC:
          handle_exec(sock, msg)
       else: #TODO: other type
             continue
          

def handle_exec(sock, msg):
    '''handle exec message, need to redirect std IO,
    get output and send response
    '''
    pass
 
def read_info(sock):
    '''read sock data,
    return (type, data)
    '''
    
    # deserialize data head
    head_len = 8
    head_raw = sock.recv(head_len)
    try:
        msg_str = struct.unpack('>4si', head_raw)
    except struct.error:
        return None, None
        
    msg_type = msg_str[0]
    msg_len = msg_str[1]
    
    # deserialize data
    msg_raw = sock.recv(msg_len)
    try:
        msg_str = struct.unpack('>%ds' % msg_len, msg_raw)
    except struct.error:
        return None, None
   
    return msg_type, msg_str
    
