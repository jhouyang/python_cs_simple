#!/usr/bin/env python

'''This is the client file
'''

import socket

def connect(host, port):
    '''connect to (host, port)
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      sock.connect((host, port))
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
    
if __name__ == '__main__':
    main()
