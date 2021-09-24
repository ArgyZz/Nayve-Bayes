import os.path
import sys
import matplotlib.pyplot as plt 
from data import *
from os import walk, path


class NayveBayes:


    def __init__(self):
        self.data = LoadData() #Data element
        self.negVec = self.data.getVector('train','neg') #Negative Vector.
        self.posVec = self.data.getVector('train','pos') #Possitive Vector.
        self.words=self.countWords() # Number of words in the Dictionary
        self.negNum , self.posNum = self.countPosNeg() # Number of Negative and possitive rewiews in the training process
        self.negSum , self.posSum = self.countWordsPerVector() #Number of words in each category
        self.totalNegWords , self.totalPosWords = self.summer() #Sum of all the neg and pos words
        self.negPossibilities , self.posPossibilities = self.calcPossibilityOfWords() # P(X|C=1) , P(X|C=0
        self.Ppossitive , self.Pnegative = self.calcPossibility() # P(C=1) , P(C=0) (1=possitive, 0=negative)
        


#Graph____________________________________________________________#

    """def Curves(self):
        heh = []
        N=25000
        presentage = (10/100)
        pre = N*presentage
        temp=0
        for i in range(1,10):
            trainDataNeg=[]
            trainDataPos=[]
            testDataNeg=[]
            testDataPos=[]
            temp = int(pre*i)
            half = int(temp/2)
            
            for j in range(half+1):
                
                trainDataNeg.append(self.negVec[j])
                trainDataPos.append(self.posVec[j])
                
            rest = int(((N/2)-half))
            
            for k in range(half, rest+1):
                testDataNeg.append(self.negVec[k])
                testDataPos.append(self.posVec[k])
            
        #WordsPerVector negSum PosSum
            negSum=[]
            posSum=[]
            for k in range(self.words):
                summ = 0
                for j in range(half):
                    summ = self.negVec[j][k] + summ
                negSum.append(summ)

            for k in range(self.words):
                summ = 0
                for j in range(half):
                    summ = self.posVec[j][k] + summ
                posSum.append(summ)
            #Summer
            totalNeg=0
            totalPos=0
            for k in range(len(negSum)):
                totalNeg = totalNeg + self.negSum[k]
                totalPos = totalPos + self.posSum[k]

            #Possibilities
            negPossibilities=[]
            posPossibilities=[]
            for k in range(self.words):
                negPossibilities.append(self.negSum[k]/totalNeg)
                posPossibilities.append(self.posSum[k]/totalPos)
        
           #Test_______________________________________________

            #FinalCalc 
            for j in testDataNeg:
                kappaNeg=1
                kappaPos = 1 
                final_neg=[]
                final_pos=[]
                countNeg=0
                countPos=0
                for k in range(self.words):
                    kappaPos =(kappaPos*(self.Power(posPossibilities[k],j[k])))
                    kappaNeg = (kappaNeg*(self.Power(negPossibilities[k],j[k])))
                final_pos.append(kappaPos*self.Ppossitive)
                final_neg.append(kappaNeg*self.Pnegative)
            for j in range(len(final_pos)):
                if(final_neg[j]>final_pos[j]):
                    countNeg +=1             
            for j in testDataPos:
                kappaPos=1
                kappaNeg=1
                for k in range(self.words):
                    kappaNeg = (kappaNeg*(self.Power(negPossibilities[k],j[k])))
                    kappaPos =(kappaPos*(self.Power(posPossibilities[k],j[k])))
                final_pos.append(kappaPos*self.Ppossitive)
                final_neg.append(kappaNeg*self.Pnegative)
            for j in range(len(final_pos)):
                if(final_neg[j]<final_pos[j]):
                    countPos +=1
            summary = countNeg+countPos
            accuracy = (summary/rest)
            heh.append(accuracy)
        return heh"""

    def makeGraph(self):
        heh = [0.6226666666666667, 0.5251, 0.3940571428571429, 0.23413333333333333, 0.00016, 0.0006, 0.0013333333333333333, 0.0028, 0.0072]
        train = [1,1,1,1,1,1,1,1,1]
        plt.plot(heh,label ="Dev")
        plt.plot(train , label = "Train")
        plt.title("Train/Dev Accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Train Data%")
        plt.show()
        
            
            
          
        
                
            










#TRAIN_______________________________________________________________TRAIN

    def countWords(self): # Counts the word in the dictionary.
        f = open(self.data.link()+"\\"+"dictionary.txt", "r")
        count=0
        for k in f.readlines():
            count=count+1
        f.close()
        return count


    def countPosNeg(self): # Calculates Number of negative and possitive rewiews.
        path = self.data.link() + "\\"+"train"
        negPath = path+"\\"+"neg"
        posPath = path+"\\"+"pos"
        negNum = len([f for f in os.listdir(negPath)if os.path.isfile(os.path.join(negPath, f))])
        posNum = len([f for f in os.listdir(posPath)if os.path.isfile(os.path.join(posPath, f))])
        return negNum , posNum


    def calcPossibility(self): # Calculates P(pos)and P(Neg).
        Ppos= self.posNum/(self.posNum+self.negNum)
        Pneg= self.negNum/(self.posNum+self.negNum)
        return Ppos , Pneg


    def countWordsPerVector(self): #Returns the sum of every word for each type of review.
        negSum=[]
        posSum=[]
        for i in range(self.words):
            summ = 0
            for j in range(self.negNum):
                summ = self.negVec[j][i] + summ
            negSum.append(summ)

        for i in range(self.words):
            summ = 0
            for j in range(self.posNum):
                summ = self.posVec[j][i] + summ
            posSum.append(summ)
        return negSum , posSum



    def calcPossibilityOfWords(self): # Returns P(X|C=1) , P(X|C=0)
        negPossibilities=[]
        posPossibilities=[]
        for i in range(self.words):
            negPossibilities.append(self.negSum[i]/self.totalNegWords)
            posPossibilities.append(self.posSum[i]/self.totalPosWords)
        return negPossibilities , posPossibilities

    def summer(self):
        totalNeg=0
        totalPos=0
        for i in range(len(self.negSum)):
            totalNeg = totalNeg + self.negSum[i]
            totalPos = totalPos + self.posSum[i]
        return totalNeg , totalPos

#_________________________________________________________________

#TEST_____________________________________________________________TEST


    def getFilesVector(self,file,ctype): #Returns the vector of given file(Counting the words).
        kappa=self.data.read_test()+"\\" +ctype +"\\" + file
        ls=[]
        vector = []
        if (path.exists(kappa)):
            ls = open(kappa,'r',encoding ="utf-8")
            dc = open(self.data.link()+"\\"+"dictionary.txt", "r" , encoding="utf-8")
            line = dc.readline().strip()
            kappa = ls.readline()
            kappa_list=kappa.split(" ")
            while line:
                count = 0
                if line in kappa:
                    for i in kappa_list:
                        i = i.strip(".")
                        i = i.strip(",")
                        i = i.lower()
                        if(line==i):
                            count=count+1
                    vector.append(count)
                else:
                    vector.append(0)
                line = dc.readline().strip()
            dc.close()
            ls.close()
            return vector
        else:
            print("Error: File doesn't exist.")
            sys.exit(0)








    def getFilesVector2(self,file,ctype): #Return the vector of giver file(Not counting words)
        kappa=self.data.read_test()+"\\" +ctype +"\\" + file
        ls=[]
        vector = []
        if (path.exists(kappa)):
            ls.extend(self.data.read_file(kappa))
            dc = open(self.data.link()+"\\"+"dictionary.txt", "r" , encoding="utf-8")
            line = dc.readline().strip()
            while line:
                if line in ls:
                    vector.append(1)
                else:
                    vector.append(0)
                line = dc.readline().strip()
            dc.close()
            return vector
        else:
             print("Error: File doesn't exist.")
             sys.exit(0)




    def finalCalc(self,file,ctype): #Returns P(X1\C)*P(X2\C).......... for C=1 and C=0
        vector=self.getFilesVector(file,ctype)
        kappaNeg=1
        kappaPos=1
        for i in range(self.words):
            kappaNeg = (kappaNeg*(self.Power(self.negPossibilities[i],vector[i]))*1000)
            kappaPos =(kappaPos*(self.Power(self.posPossibilities[i],vector[i]))*1000)
        final_neg = kappaNeg*self.Pnegative
        final_pos = kappaPos*self.Ppossitive
        if(final_neg>final_pos):
            return 0
        elif(final_neg<final_pos):
            return 1



    def Power(self,element,N): #Element to the power of N
        kappa=element**N
        return kappa





    def TestResult(self,ctype):
        if ctype != 'neg' and ctype != 'pos':
            return
        path =self.data.read_test()+"\\"+ctype
        count=0
        f=[]
        for(dirpath,folders,files) in walk(path):
            f.extend(files)
        for j in f:
            temp = self.finalCalc(j,ctype)
            if (temp==0 and ctype == "neg"):
                count = count + 1
            elif(temp==1 and ctype == "pos"):
                count = count + 1
        return count



    def accuracy(self):
        neg = self.TestResult("neg")
        pos = self.TestResult("pos")
        summary = neg + pos
        accuracyScore = summary/25000
        return accuracyScore


    

#Main______________________________________________________________#
kappa=NayveBayes()
while True:
    x= input("Would you like to check a review or check the algorithms accuracy?(Type file for checking a file or accuracy):  ")
    x = x.lower()
    if(x=="file"):
        file = input("Input name file: ")
        ctype = input("(And type for the path)")
        result=kappa.finalCalc(file,ctype)
        if (result==0):
            print("The review is Negative!")
        else:
            print("The review is Possitive!")
    elif(x=="accuracy"):
        accuracyScore = kappa.accuracy()
        print("Accuracy rate: "+ str(int(accuracyScore*100)) + "%")

    else:
        print("Wrong Input. Terminating.....")
        sys.exit(0)
        
