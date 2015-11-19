#Eric Lindemann
#https://en.wikipedia.org/wiki/Viterbi_algorithm for reference on viterbi algorithm

import sys
import math

class HMM:
    def __init__(self):
        self.states = 'abcdefghijklmnopqrstuvwxyz_'
        self.resultsGotten = {}
        self.resultsTransition = {}
        self.total = 0
        self.counts = {}

    def pullData(self,setFile):
        f = open(setFile)
        dataExpected = []
        dataGotten = []
        
        self.resultsGotten = {} #should store for instance '{'a': {'a': COUNT, 'b':BOUNT, etc..}
        self.resultsTransition = {}

        countsGotten = {}
        countsTransition = {}
        countsLetter = {}

        for c in self.states:
            countsLetter[c] = 0
            countsGotten[c] = 0
            countsTransition[c] = 0
            for char in self.states:
                self.resultsGotten[c] = {char: 0}
                self.resultsTransition[c] = {char: 0}
            self.counts[c] = 0

        for line in f:
            self.total += 1
            dataExpected.append(line[0])
            dataGotten.append(line[2])
        
        for c in self.states:

            for i in range(0,len(dataExpected)-1):
                tempGotten = {}
                if (c == dataExpected[i]):
                    self.counts[c] += 1
                    countsLetter[c] += 1
                    countsGotten[dataGotten[i]] += 1
                    countsTransition[dataExpected[i+1]] += 1

            for char in self.states:
                self.resultsGotten[c][char] = countsGotten[char]
                self.resultsTransition[c][char] = countsTransition[char]
                countsGotten[char] = 0
                countsTransition[char] = 0

    def printData(self):
        fd = open('Output.txt','w')
        old_stdout = sys.stdout  
        sys.stdout = fd
        #print Emission Probabilites
        print '\nFor Emission Probabilities:'
        for char in self.states:
            for char2 in self.states:
                print 'P(',char,'|',char2,') = ', (1+self.resultsGotten[char][char2])/float(26+self.counts[char])

        #print Transition probabilities
        print '\nFor Transition Probabilities:'
        for char in self.states:
            for char2 in self.states:
                print 'P(',char,'|',char2,') = ', (1+self.resultsTransition[char][char2])/float(26+self.counts[char])
       
        print '\nFor Marginal/Initial Probablities:'
        for char in self.states:
            print 'P(',char,') = ', (1+self.counts[char])/float(26+self.total)
        sys.stdout = old_stdout
        fd.close()

    def getEmission(self):
        emissionProbabilities = {}
        for char in self.states:
            for char2 in self.states:
                emissionProbabilities[char] = {char2: 0}
        for char in self.states:
            for char2 in self.states:
                emissionProbabilities[char][char2] = (1+self.resultsGotten[char][char2])/float(26+self.counts[char])
        return emissionProbabilities


    def getTransition(self):
        transitionProbabilities = {}
        for char in self.states:
            for char2 in self.states:
                transitionProbabilities[char] = {char2: 0}

        for char in self.states:
            for char2 in self.states:
                transitionProbabilities[char][char2] = (1+self.resultsTransition[char][char2])/float(26+self.counts[char])
        return transitionProbabilities

    def getStart(self):

        startProbabilities = {}
        for char in self.states:
            startProbabilities[char] = (1+self.counts[char])/float(26+self.total)
        return startProbabilities

            

def viterbi(obs, startProbs, transProbs, emisProbs):
    states = 'abcdefghijklmnopqrstuvwxyz_'
    path = {}
    V = [{}]

    for char in states:
        
        V[0][char] = math.log10(startProbs[char]) + math.log10(emisProbs[char][obs[0]])
        path[char] = [char]
    
    t = 1
    while t <= len(obs)-1:
        V.append({})
        newpath ={}
        for char in states:
            (prob, state) = max((V[t-1][y0] + math.log10(transProbs[y0][char]) + math.log10(emisProbs[char][obs[t]]), y0) for y0 in states)
            V[t][char] = prob
            newpath[char] = path[state] + [char]

        t+=1
        path = newpath
    (prob, state) = max((V[len(obs)-1][y], y) for y in states)
    return (prob, path[state])


thisHMM = HMM()
setFile = sys.argv[1]
thisHMM.pullData(setFile)
observed = []
correct = []
f = open(setFile)
for line in f:    
    correct.append(line[0])
    observed.append(line[2])
V = viterbi(observed,thisHMM.getStart(),thisHMM.getTransition(),thisHMM.getEmission())
numCorrect = 0
Vtext =V[1]
print 'State Sequence:'
for element in Vtext:
    sys.stdout.write(element) 
    
for i in range(0,len(Vtext)):
    if Vtext[i] == correct[i]:
        numCorrect += 1


print '\n\nError Rate: ',1 - numCorrect/float(len(correct))
