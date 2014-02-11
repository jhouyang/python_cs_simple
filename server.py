#!/usr/bin/env python

import sys
import socket
from protocol import handle_conn

def try_port(sock, start_port, host = ''):
    try:
        sock.bind((host, start_port))
        print 'socket bind on port : ', start_port
    except socket.error, msg:
        if int(msg[0]) == 48: # address already in use
            try_port(sock, start_port + 1, host)
        else:
            print 'Bind failed. Error code' + str(msg[0]) + 'Message' \
                    + msg[1]
            sys.exit(-1)

def get_start_port(port):
    try:
        port = int(port)
    except ValueError:
        print 'Please input valid port'
        sys.exit(-1)

    if port < 1024 or port >= 65535:
        print 'Please input valid port ([1024-65535))'
        sys.exit(-1)

    return port
    
def main():
    # take the first arg as port
    arg = sys.argv[1:]
    if not arg:
        print 'Please input port number'
        sys.exit(-1)

    # get port number
    port = get_start_port(arg[0])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'socket created.'
    try_port(sock, port)
    sock.listen(5)
    print 'socket listenning'

    while True:
        connection, address = sock.accept()
        while True:
            try:
                connection.settimeout(60) 
                handle_conn(connection)

            except socket.timeout:
                print 'time out'
                connection.close()
                break;

if __name__ == '__main__':
    main()

