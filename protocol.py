#!/usr/bin/env python

'''Define protocol about how to send and recv message
between server and client.
   And the protocol should be (big end):
   messages : type, size of data, data 
   size     : 4,    unkown      , unkown
   type     : string, int,        string
'''
import sys
import struct

class ProtoCol(object):
    '''define some types and send message
    '''
    SUCCESS, ERROR, INFO, RESP, CLOSE, EXEC = ('succ', 'erro', 'info', 'resp', 'clos', 'exec')
    @classmethod
    def send_response(sock, msg):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.RESP, len(msg), msg)
        sock.sendall(send_msg)

    @classmethod
    def send_info(sock, msg):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.INFO, len(msg), msg)
        sock.sendall(send_msg)

    @classmethod
    def send_error(sock, msg):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.ERROR, len(msg), msg)
        sock.sendall(send_msg)

    @classmethod
    def send_close(sock, msg):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.CLOSE, len(msg), msg)
        sock.sendall(send_msg)
   
    @classmethod
    def send_success(sock, msg = ''):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.SUCCESS, len(msg), msg)
        if not msg:
            send_msg = struct.pack('>4si', ProtoCol.SUCCESS, 0)
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
    redirect = Redirection()
    try:
        exec(msg)
        if redicect.my_err:
            ProtoCol.send_error(sock, redicect.my_err)
        elif redicect.my_out:
            ProtoCol.send_response(sock, redicect.my_out)
        else:
            ProtoCol.send_success(sock)
    except Exception, e:
        ProtoCol.send_error(sock, e)
    finally:
        redirect.reset()

class Redirection(object):
    ''' redirect stdout and stderr
    '''
    def __init__(self):
        '''init function
        '''
        self._out = ''
        self._err = ''
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        
    def write(self, out_str):
        '''write stdout
        '''
        self._out += output_stream
   
    def write_err(self, err_str):
        '''write stderr
        '''
        self._err += err_str
    
    @property    
    def my_out(self):
        '''get out message
        '''
        return self._out
        
    @property
    def my_err(self):
        '''get error message
        '''
        return self._err
    
    def flush(self):
        '''flush all
        '''
        self._out = ''
        self._err = ''
        
    def reset(self):
        '''reset stdout and stderr
        '''
        sys.stdout = self._stdout
        sys.stderr = self._stderr
        
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
    
