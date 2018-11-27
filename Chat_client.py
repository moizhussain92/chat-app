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
        self.Ip = '127.0.0.1'
        self.listenPort = 15000
        self.bindSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bindSock.bind((self.Ip, self.listenPort))
        self.bindSock.listen(5)

    def connectToServer(self):
        self. query = self.server_socket.send('Hi, This is client 1')
        while True:
            self.size = 4096*100
            self. data = self.server_socket.recv(self.size)
            print 'Received: ', str(self.data)
            if self.data.find('Are you are new or a returning user?') >= 0:
                self.userStatus()
            elif self.data.find('Give your new Username and Password') >= 0:
                self.Reg()
            elif self.data.find('Give your Username and Password') >= 0:
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
        print 'Received credentials: ', str(self.receiveInfo).lstrip()

        if self.receiveInfo.find('Error') >= 0:
            self.askClientInfo(userName)
        else:
            self.connectPort = self.receiveInfo.lstrip()
            #self.establishConnection(self.connectPort)
            print self.connectPort
            self.establishConnection(self.connectPort, self.userName)

    def establishConnection(self, connectPort, userName):
        self.connectSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectSock.connect(('127.0.0.1', int(self.connectPort)))
        self.connectSock.send ('%s Connected' %(self.userName,))
        self.r = self.connectSock.recv(4096)
        if self.r.find('Start') >= 0:
            self.name = self.r.split(' ',2)[1].lstrip()
            while self.r != 'Quitnow':

                if self.r.find('filecoming--') >= 0:
                    self.connectSock.send('OK')
                    self.fileReceive1(self.r, self.userName)
                if str(self.r).find('filerequest--') >= 0:
                    self.fileTransfer1(self.r, self.userName)

                self.sending = raw_input('You: ')
                self.connectSock.send(self.sending)
                self.r1 = self.connectSock.recv(4096)
                print '%s: ' %(str(self.name),), str(self.r1)
                if str(self.sending) == 'Quitnow':
                    self.deReg(self.userName)
                    break
            else:
                self.deReg(self.userName)



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
            self.userWish(self.userName)
            '''self.wish = raw_input('Enter C to connect and Q to Quit: ')
            if str(self.wish) == 'Q':
                self.portSend()
                self.deReg(self.userName)
            elif str(self.wish) == 'C':
                self.askList(self.userName)
            else:
                print 'Error. Enter a valid command.'
            #self.deReg(self.userName)'''
            #return'''

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
            self.userWish(self.userName)

    def userWish(self,userName):
            self.wish = raw_input('Enter C to connect, L to listen and Q to Quit: ')
            if str(self.wish) == 'Q':
                self.portSend()
                self.deReg(self.userName)
            elif str(self.wish) == 'C':
                self.askList(self.userName)
            elif str(self.wish) == 'L':
                self.listenConn(self.userName)
            else:
                print 'Error. Enter a valid command.'
                self.userWish(self.userName)
                #self.askList(self.userName)


    def deReg(self, userName):
        print 'To deReg: ', str(self.userName)
        self.wish = raw_input('Do you want to quit? [Y/N]: ')
        if self.wish == 'N':
            print 'OK'
            '''sys.exit(10)'''
        elif self.wish != 'Y':
            print 'Enter a valid command'
            self.deReg(self.userName)
        else:
            self.toSend = 'Quit ' + str(self.userName)
            self.server_socket.send(self.toSend)
            sys.exit(10)

    def listenConn(self, userName):
        self.server_socket.send('listening to client')
        self.portSend()
        print 'Listen entered'
        self.data, address = self.bindSock.accept()
        print address
        self.receivedData = self.data.recv(4096)
        #print self.receivedData
        if self.receivedData.find('Connected') >= 0:
            self.name = self.receivedData.split(' ',2)[0].rstrip()
            self.data.send('Start %s' %(self.userName,))
            while self.receivedData != 'Quitnow':
                self.r = self.data.recv(4096)
                if self.r.find('filecoming') >= 0:
                    self.data.send('OK')
                    self.fileReceive(self.r, self.userName)
                elif str(self.r).find('filerequest--') >= 0:
                    self.fileTransfer(self.r, self.userName)

                print '%s: ' %(str(self.name),), str(self.r)


                self.sending = raw_input('You: ')
                self.data.send(str(self.sending))
                if str(self.sending) == 'Quitnow':
                    self.deReg(self.userName)
                    self.data.send(str(self.sending))
                    break
            else:
                self.deReg(self.userName)

    def fileReceive(self, r, userName):
        self.filename = self.r.split('--',2)[1].lstrip(), str('-A')
        self.seen = self.data.recv(4096*100)
        self.file = open (self.filename, 'ab+')
        self.file.write(str(self.seen))
        self.file.close()


    def fileTransfer(self, r, userName):
        self.fileName = self.r.split('--', 2)[1]
        self.file = open(self.fileName, 'rb').read()
        self.data.send('filecoming-- %s' %(self.fileName,))
        self.data.recv(4096)
        self.data.send(self.file)

    def fileReceive1(self, r, userName):
        self.filename = self.r.split('--',2)[1].lstrip(), str('-A')
        self.seen = self.connectSock.recv(4096*100)
        self.file = open (self.filename, 'ab+')
        self.file.write(str(self.seen))
        self.file.close()


    def fileTransfer1(self, r, userName):
        self.fileName = self.r.split('--', 2)[1]
        self.file = open(self.fileName, 'rb').read()
        self.data.send('filecoming-- %s' %(self.filename,))
        self.connectSock.recv(4096)
        self.connectSock.send(self.file)

    '''def quit(self, userName):
        self.intake = raw_input('Do you want to be de-registered? [Y/N]: ')
        if self.intake == 'Y':
            self.deReg(self.userName)
        elif self.intake == 'N':
            print 'OK, you are not deregistered. You can access the server by logging in again as a returning user'
        else:
            print 'Please enter a valid command'
            self.quit(self.userName)'''


if __name__== '__main__':
    temp = generateRequest()
    temp.connectToServer()
