import socket
import os
import sys
import time
class PacketSender(object):
    '''
    Send pack to specific host:port
    '''
    def __init__(self, hostname, port):
        
        self.hostname = hostname
        self.port = port

    def send(self, pack_path):
        #TODO: better have logging here
        try:    
            sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to creat socket. Error code:', str(msg[0]), 
            print 'Error message:', msg[1]
            return -1

        success = False
        attemps = 0
        while attemps < 10 and not success:
            try:
                # Connect to remote server
                sender.connect((self.hostname, self.port))
#                print 'Socket Connected to ', self.hostname, ' on port ', self.port, 'attemps is :', attemps
                success = True
            except:
                attemps += 1
                time.sleep(20)
                if attemps == 10:
                    print 'try connecting to %s on port %s failed' %(self.hostname, self.port)
                    return -2
        # try:
        #     # Connect to remote server
        #     sender.connect((self.hostname, self.port))
        #     print 'Socket Connected to ', self.hostname, ' on port ', self.port
        # except socket.error:
        #     print 'try connecting to %s on %s failed' %(self.hostname, self.port)
        #     return -2
        # Send some data to remote server | socket.sendall(string[, flags]) 
        try:    
            with open(pack_path, 'rb') as pack:
                sender.sendall(pack.read())
        except socket.error, arg:
            (errno, err_msg) = arg
            print 'Send fail.: %s, err msg is : %s , errno is : %d ' %(socket.error, err_msg, errno)
            return  -3

        sender.close()
        return 0
