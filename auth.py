import os
import socket

class authentication:
    global myFile
    myFile = {}
    def __init__(self):
        self.answer = raw_input('Are you a new user? [Y/N]: ')
        
        if str(self.answer).find('Y') >= 0:
            self.storeInfo()
        elif str(self.answer).find('N') >= 0:
            self.checkInfo()
        else:
            print 'Enter valid response'
            return 0

    def storeInfo(self):
        self.username = raw_input('Enter your username: ')
        self.password = raw_input('Enter your Password: ')
        myFile[self.username] = self.password
        self.new = open('store.txt', 'a')
        self.new.write(str(myFile))
        self.new.close()
        return 0

    def checkInfo(self):
        print 'Checking....'
        self.username = raw_input('Enter your username: ')
        self.password = raw_input('Enter your Password: ')
        print 'aaa'
        self.check = open('store.txt', 'rb')
        self.check1 = self.check.read()
        if str(self.check1).find(str(self.username)) >= 0:
            print 'entered'
            if str(self.check1).find(str(self.password)) >= 0:
                print 'You are good'
                self.check.close()
                break
            else:
                for count in range(3):
                    print 'Try again'
                    if raw_input('Enter your Password: ')== self.password:
                        return 0

                print 'You are blocked'
        else:
            sys.exit(10)
            print 'Nothing'
                   
                
if __name__== '__main__':
    temp = authentication()
    
