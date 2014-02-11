#!/usr/bin/env python

'''This is the client file
'''

import sys
import socket
from protocol import ProtoCol, read_info

def connect(host, port):
    '''connect to (host, port)
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      sock.connect((host, int(port)))
    except socket.error, e:
      print e
      sys.exit(-1)
      
    return sock
  

def main():
    '''main function of client
    '''
    arg = sys.argv[1:]
    if len(arg) != 2:
        print 'Please input valid host and port number'
        sys.exit(-1)
        
    sock = connect(arg[0], arg[1])
    print 'connect to %s:%s' % (arg[0], arg[1])
    
    while True:
        msg = raw_input(">>> ")
        
        if msg == 'exit':
            ProtoCol.send_close(sock)
        else:
            ProtoCol.send_exec(sock, msg)
        
        msg_type, msg_str = read_info(sock)
        print msg_type, msg_str
    
if __name__ == '__main__':
    main()
