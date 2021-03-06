import socket
import sys
import select
import time
import os

class mainServer:

     def __init__ (self):
          if os.path.isfile('PA4_logFile.txt'):
               os.remove('PA4_logFile.txt')
          if os.path.isfile('regEntry.txt'):
               openfile = open('regEntry.txt', 'rb')
               readfile = openfile.read()
               openfile.close()
               if str(readfile) == '{}':
                    os.remove('regEntry.txt')
          if os.path.isfile('clientList.txt'):
               openfile = open('clientList.txt', 'rb')
               readfile = openfile.read()
               openfile.close()
               if str(readfile) == '{}':
                    os.remove('clientList.txt')

          self.host = ''
          self.port = 9090
          self.backlog = 5

          self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.s.bind((self.host,self.port))
          self.s.listen(self.backlog)

     def clientConnection(self):
          input = [self.s,sys.stdin]

          while True:
              inputready,outputready,exceptready = select.select(input,[],[])
              for self.client_socket in inputready:
                  if self.client_socket == self.s:
                    self.client, address = self.s.accept()
                    self.clientPort = address[1]
                    self.clientIp  = address[0]
                    self.Logging(self.clientPort, self.clientIp)
                    self. query = self.client.send('Hi, This is server\n')
                    input.append(self.client)
                  else:
                    print 'rerer'
                    self.client_socket.send('Are you are new or a returning user?')
                    self.data = self.client_socket.recv(4096*100)
                    print 'Received: ', str(self.data)
                    self.checkFlag = self.checkStatus(address)

                    if self.data.find('Give me the client list') >= 0:
                        print 'mila'
                        self.clientList(self.data, address, self.listenData)

                    if self.data.find('listening to client') >= 0:
                        print 'from client: ', str(self.data)

                    if self.data.find('Quit') >= 0:
                        self.check = self.data.split(' ',2)
                        self.usName = self.check[1]
                        self.deReg(self.usName,address)
                    if self.checkFlag == 0:
                        break

     def checkStatus(self,address):
          self.data = self.client_socket.recv(4096*100)
          try:
               if self.data.find('N') >= 0:
                    self.storeInfo(self.data,address)
                    return 0
               elif self.data.find('R') >= 0:
                    self.f = self.authenticate(self.data,address)
                    if self.f == 0:
                         return 0

                    else:
                         return 1

          except KeyError:
               print self.client_socket.send('Enter a valid command')
               self.checkStatus(address)

     def authenticate(self, data, address):
          self.client = {}
          self.client_socket.send('Give your Username and Password')
          print 'Auth entered'
          self.data = self.client_socket.recv(4096*100)
          if self.data.find('||||')>=0:
             self.store = self.data.split('||||',2)
             self.blockName = self.store[0]
             self.flag = self.blockCheck(self.blockName, address)
             print 'flag: ', self.flag
             if self.flag == 0:
                  return
             elif self.flag == 1:

                  self.client[self.store[0]] = self.store[1]
                  print 'Auth: ' , self.client
                  self.auth = {}
                  self.clientAuth = open('regEntry.txt', 'a+')
                  self.clientAuth1 = self.clientAuth.read()
                  self.clientAuth.close()
                  if self.clientAuth1:
                      self.auth = eval(self.clientAuth1)
                  else:
                      self.auth = {}
                  print str(self.auth)
                  while True:
                      print str(self.auth)
                      if str(self.auth).find(self.store[0]) >= 0:
                          for i in range(0, 3):
                              if self.auth[self.store[0]] != self.store[1]:
                                  passError = 'Bad Password: Attempt - %d\n' %(i+1, )
                                  print i
                                  if i == 2:
                                      self.usName = self.store[0]
                                      self.blockClient(self.usName)
                                      self.deReg(self.usName,address)
                                      self.client_socket.send('You are blocked')
                                      print'Blocked'
                                      return 0
                                  else:
                                      self.client_socket.send(passError)
                                      passw = self.client_socket.recv(4096)
                                      print passw
                                      self.store[1] = passw.rstrip()
                              elif self.auth[self.store[0]] == self.store[1]:
                                  self.blockName = self.store[0]
                                  self.blockCheck(self.blockName, address)
                                  self.client_socket.send('You are authenticated')
                                  self.usName = self.store[0]

                                  self.listenData = self.client_socket.recv(4096*100)
                                  print self.listenData
                                  if self.listenData.find('listening to client') >= 0:
                                      return
                                  else:
                                    self.clientList(self.data, address, self.listenData)
                                    print 'return hoja'
                                    return 1
                          break
                      else:
                          usError = 'Invalid Username. Please enter a valid username\n'
                          self.client_socket.send(usError)
                          user = self.client_socket.recv(4096)
                          self.store = user.split('||||',2)

                          print 'store: ', str(self.store)

     def blockClient(self, usName):
          self.block = open('clientsBlocked.txt', 'a')
          self.toWrite = usName + '\n'
          print 'block: ', self.toWrite
          self.blockwrite = self.block.write(self.toWrite)
          self.block.close()
          return

     def blockCheck(self, blockName, address):
          self.block = open('clientsBlocked.txt', 'ab+')
          self.blockwrite = self.block.read()
          self.block.close()
          if self.blockwrite.find(self.blockName) >= 0:
               print 'Block found'
               self.client_socket.send('You have been Blocked already.')
               return 0
          else:
               return 1


     def storeInfo(self, data, address):
          self.client_socket.send('Give your new Username and Password')
          self.data = self.client_socket.recv(4096*100)
          print self.data
          regDict = {}

          if self.data.find('||||')>=0:
               self.store = self.data.split('||||',2)
               self.blockName = self.store[0]
               self.flag = self.blockCheck(self.blockName, address)
               if self.flag == 0:
                    return
               elif self.flag == 1:
                    self.reg = open('regEntry.txt', 'ab+')
                    self.reg1 = self.reg.read()

                    if self.reg1:
                         regDict = eval(self.reg1)
                    else:
                         regDict = {}

                    self.reg.close()
                    regDict[self.store[0]] = self.store[1]
                    self.regEnter = open('regEntry.txt', 'w')
                    self.regEnter.write(str(regDict))
                    self.regEnter.close()
                    self.client_socket.send('You are Registered')
                    self.usName = self.store[0]

                    self.listenData = self.client_socket.recv(4096*100)
                    print self.listenData

                    if self.listenData.find('listening to client') >= 0:
                        self.listen = self.client_socket.recv(4096)
                        print 'listen: ', str(self.listen)
                        self.makeClientList(self.usName, address, self.listen)
                        return
                    else:
                        self.clientList(self.usName, address, self.listenData)
                        return

     def makeClientList(self, usName, address, listen):
          self.parsed = self.listen.strip('[]').split(',',2)
          self.Ip = str(self.parsed[0]).strip("'")
          self.listenPort = str(self.parsed[1]).lstrip()
          self.listenPort1 = int(self.listenPort)
          self.newParsed =(self.Ip, self.listenPort1)
          print 'newParse: ' , self.newParsed
          client_List = {}
          self.cList = open('clientList.txt', 'ab+')
          self.c_List = self.cList.read()
          if self.c_List:
               client_List = eval(self.c_List)
          else:
               client_List = {}
          client_List[self.usName] = self.newParsed
          print 'clientList : ', client_List.keys()
          self.cList = open('clientList.txt', 'w')
          self.c_List = self.cList.write(str(client_List))
          self.cList.close()


     def clientList(self, usName, address, listenData):

          print 'writewite'

          self.parsed = self.listenData.strip('[]').split(',',2)
          self.Ip = str(self.parsed[0]).strip("'")
          self.listenPort = str(self.parsed[1]).lstrip()
          self.listenPort1 = int(self.listenPort)
          self.newParsed =(self.Ip, self.listenPort1)
          print 'newParse: ' , self.newParsed
          client_List = {}
          self.cList = open('clientList.txt', 'ab+')
          self.c_List = self.cList.read()
          if self.c_List:
               client_List = eval(self.c_List)
          else:
               client_List = {}
          client_List[self.usName] = self.newParsed
          print 'clientList : ', client_List.keys()
          self.cList = open('clientList.txt', 'w')
          self.c_List = self.cList.write(str(client_List))
          self.cList.close()
          self.sendList(self.usName, client_List)

     def sendList(self, usName, client_List):
          self.data = self.client_socket.recv(4096*100)
          if self.data.find('Give me the client list') >= 0:

               self.client_socket.send(str(client_List.keys()))

               self.List = open('clientList.txt', 'rb')
               self.List1 = self.List.read()
               self.List.close()
               print 'FileList: ', str(self.List1)
          else:
               return
          self.sendClientInfo(self.usName, client_List)


     def sendClientInfo(self, usName, client_List):
          self.data = self.client_socket.recv(4096*100)
          if self.data.find('GET_CLIENT_INFO') >=0:
               print 'To: ', str(self.data)
               print 'data: ' + str(self.data)
               print 'usName: ' + str(self.usName)
               print 'client_List: ' , client_List
               self.referencedClient = self.data.split(' ', 2)[1].lstrip()
               print 'To Connect: ' , str(self.referencedClient)
               if str(self.referencedClient) == str(self.usName):
                    self.error = 'Error. You cannot connect to yourself.'
                    self.client_socket.send(self.error)
                    self.sendClientInfo(self.usName, client_List)
               elif str(self.referencedClient) not in client_List:
                    self.error = 'Error. Client not found in the list.'
                    self.client_socket.send(self.error)
                    self.sendClientInfo(self.usName, client_List)
               else:
                    self.clientAddress = client_List[self.referencedClient]
                    print 'Address: ' , str(self.clientAddress)
                    self.new = str(self.clientAddress).split(',', 2)
                    self.clientPort = self.new[1].strip(')').lstrip()
                    self.client_socket.send(str(self.clientPort))


     def deReg(self, usName, address):
          print 'deReg Entered'
          deReg_list = {}
          deReg_client = {}
          self.deRegList = open ('clientList.txt', 'ab+')
          self.deRegClist = self.deRegList.read()
          if self.deRegList:
               deReg_list = eval(self.deRegClist)
          else:
               deReg_list = {}
          self.deRegList.close()
          del deReg_list[self.usName]
          print 'Keys :' , deReg_list.keys()
          self.cList = open('clientList.txt', 'w')
          self.cList.write(str(deReg_list))
          self.cList.close()

          self.reg = open('regEntry.txt', 'ab+')
          self.reg1 = self.reg.read()
          if self.reg1:
               deReg_client = eval(self.reg1)
          else:
               deReg_client = {}
          self.reg.close()
          del deReg_client[self.usName]
          print 'regKeys: ', deReg_client.keys()
          self.regEnter = open('regEntry.txt', 'w')
          self.regEnter.write(str(deReg_client))
          self.regEnter.close()

     def Logging(self, clientPort, clientIp):
          self.timeStampLog = time.strftime('%c')
          self.log = str(self.clientIp) + ' ' + str(self.clientPort)
          self.log += ' ' + str(self.timeStampLog) + '\n'
          self.logFile = open('PA4_logFile.txt', 'a').write(self.log)



if __name__== '__main__':
    temp = mainServer()
    temp.clientConnection()
