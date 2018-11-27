
class CalculateGrade:


    def homeWork (self):
        print '=====Grade Calculation====='
        print 'Enter the Marks as Obtained'
        i = 1
        self.homework = 0
        while (i < 8):
            self.homework1 = raw_input('Homework %s : '%(i,) )
            self.homework = int(self.homework) + int(self.homework1)
            i+=1
            

        print self.homework
        self.marks = (self.homework)/30)*100
        print 'HW marks:', self.marks
        self.Labs()

    def Labs(self):
        i = 1
        self.Labs = 0
        while (i < 10):
            self.Lab1 = raw_input('Lab %s : '%(i,) )
            self.Lab = int(self.Lab) + int(self.Lab1)
            i+=1
            

        print self.Lab
        self.marks = (int(self.Lab)/30)*100
        print 'Lab marks:', self.marks
        
            
if __name__== '__main__':
    temp = CalculateGrade()
    temp.homeWork()
