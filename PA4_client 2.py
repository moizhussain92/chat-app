import socket
import os
import time

class generateRequest:

    def __init__ (self):
        self.timeStamp = 0
        self.host = 'localhost'
        self.Port = 9090
        self. server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self. server_socket.connect((self.host, self.Port))

    def connectToServer(self):
            self.size = 4096*100
            self. query = self.server_socket.send('Hi, This is client 2\n')
            self. data = self.server_socket.recv(self.size)
            self. userName = raw_input('Enter your Username: ')
            self. password = raw_input('Enter your Password: ')
            self.userInfo = self.userName + '||||' + self.password
            print self.userInfo
            self.server_socket.send(self.userInfo)
            
            print self.data

if __name__== '__main__':
    temp = generateRequest()
    temp.connectToServer()
