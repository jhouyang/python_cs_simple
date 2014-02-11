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
    @staticmethod
    def send_response(sock, msg):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.RESP, len(msg), msg)
        sock.sendall(send_msg)

    @staticmethod
    def send_info(sock, msg):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.INFO, len(msg), msg)
        sock.sendall(send_msg)

    @staticmethod
    def send_error(sock, msg):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.ERROR, len(msg), msg)
        sock.sendall(send_msg)
        
    @staticmethod
    def send_exec(sock, msg):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.EXEC, len(msg), msg)
        sock.sendall(send_msg)

    @staticmethod
    def send_close(sock, msg = ''):
        send_msg = struct.pack('>4si%ds' % len(msg), ProtoCol.CLOSE, len(msg), msg)
        if not msg:
            send_msg = struct.pack('>4si', ProtoCol.SUCCESS, 0)
        sock.sendall(send_msg)
   
    @staticmethod
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
    stdout = RedirStdIO(sys.stdout)
    sys.stdout = stdout
    stderr = RedirStdIO(sys.stderr)
    sys.stderr = stderr
    try:
        exec(msg)
        if stderr.buff:
            ProtoCol.send_error(sock, stderr.buff)
        elif stdout.buff:
            ProtoCol.send_response(sock, stdout.buff)
        else:
            ProtoCol.send_success(sock)
    except Exception, e:
        ProtoCol.send_error(sock, e)
    finally:
        
        stdout.reset(sys.stdout)
        stderr.reset(sys.stderr)

class RedirStdIO(object):
    ''' redirect stdout and stderr
    '''
    def __init__(self, std_io):
        '''init function
        '''
        self._buff = ''
        self._console = std_io
        
    def write(self, out_str):
        '''write stdout
        '''
        self._buff += output_stream
   
    @property    
    def buff(self):
        '''get out message
        '''
        return self._buff
        
    
    def flush(self):
        '''flush all
        '''
        self._buff = ''
        
    def reset(self, std_io):
        '''reset stdout and stderr
        '''
        std_io = self._console
        
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
    
