import socket
import os
import time
import sys


class generateRequest:

    def __init__ (self):
        self.timeStamp = 0
        self.host = 'localhost'
        self.Port = 9090
        self. server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self. server_socket.connect((self.host, self.Port))

    def connectToServer(self):
        self. query = self.server_socket.send('Hi, This is client 1')
        while True:
            self.size = 4096*100
            self. data = self.server_socket.recv(self.size)
            print 'Received: ', str(self.data)
            if self.data.find('Are you are new or a returning user?') >= 0:
                self.userStatus()         
            if self.data.find('Give your new Username and Password') >= 0:
                self.Reg()
            if self.data.find('Give your Username and Password') >= 0:
                self.auth()
            '''if self.data.find('You are Registered') >= 0:
                self.askList()'''
                
    def askList(self, userName):
        self.portSend()
        self.server_socket.send('Give me the client list')
        self.data = self.server_socket.recv(4096*100)
        print 'List: ', self.data
        self.askClientInfo(self.userName)

    def askClientInfo(self, userName):
        self.clientConnect = raw_input('Whom do you want to connect to?: ')
        self.connectRequest = 'GET_CLIENT_INFO' + ' ' + str(self.clientConnect)
        self.server_socket.send(str(self.connectRequest))
        self.receiveInfo = self.server_socket.recv(4096*100)
        print self.receiveInfo.lstrip()

        if self.receiveInfo.find('Error') >= 0:
            self.askClientInfo(userName)

    def portSend(self):
        self.listenAddress = []
        self.Ip = '127.0.0.1'
        self.listenPort = 15000
        self.listenAddress = [self.Ip, self.listenPort]
        self.server_socket.send(str(self.listenAddress))
        

    def userStatus(self):
        self.status = raw_input('Enter N for new user and R for returning user: ')
        if self.status == 'N':
            self.server_socket.send(str(self.status))
            return
        elif self.status == 'R':
            self.server_socket.send(str(self.status))
            return
        else:
            print 'Enter a valid Command'
            self.userStatus()
            
    def Reg (self):
        self. userName = raw_input('Enter your Username: ')
        self. password = raw_input('Enter your Password: ')
        self.userInfo = self.userName + '||||' + self.password
        print self.userInfo
        self.server_socket.send(self.userInfo)
        self.data = self.server_socket.recv(4096*100)
        print self.data
        if self.data.find('You have been Blocked already.') >= 0:
            sys.exit()
        else:
            self.wish = raw_input('Enter C to connect and Q to Quit: ')
            if str(self.wish) == 'Q':
                self.portSend()
                self.deReg(self.userName)
            elif str(self.wish) == 'C':
                self.askList(self.userName)
            else:
                print 'Error. Enter a valid command.'
            '''self.deReg(self.userName)'''
            return

    def auth (self):
        self. userName = raw_input('Enter your Username: ')
        self. password = raw_input('Enter your Password: ')
        self.userInfo = self.userName + '||||' + self.password
        print self.userInfo
        self.server_socket.send(self.userInfo)
        self.data = self.server_socket.recv(4096*100)
        print self.data
        if self.data.find('You have been Blocked already.') >= 0:
            sys.exit(10)
        while self.data.find('Invalid Username') >= 0:
            self.auth()

        while self.data.find('Bad Password') >= 0:
            self. password = raw_input('Enter your Password Again: ')
            self.server_socket.send(self.password)
            self.data = self.server_socket.recv(4096*100)
            print self.data
            
            if self.data.find('Bad Password') >= 0:
                continue
            elif self.data.find('You are blocked') >= 0:
                sys.exit(10)
        if self.data.find('You are authenticated') >= 0:
            print 'dededede'
            self.wish = raw_input('Enter C to connect and Q to Quit: ')
            if str(self.wish) == 'Q':
                self.portSend()
                self.deReg(self.userName)
            elif str(self.wish) == 'C':
                self.askList(self.userName)
            else:
                print 'Error. Enter a valid command.'
                self.askList(self.userName)
                '''self.deReg(self.userName)'''


    def deReg(self, userName):
        self.wish = raw_input('Do you want to quit? [Y/N]: ')
        if self.wish == 'N':
            print 'OK'
            sys.exit(10)
        elif self.wish != 'Y':
            print 'Enter a valid command'
            self.deReg(self.userName)
        else:            
            self.toSend = 'Quit ' + str(self.userName)
            self.server_socket.send(self.toSend)
            sys.exit(10)


if __name__== '__main__':
    temp = generateRequest()
    temp.connectToServer()
