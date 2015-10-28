import sys

def conditional(myDict,using,listofAbb):
    if len(listofAbb) == 1: #conditioned on one parameter 
        if myDict[using][1] == None and myDict[listofAbb[0]][1] == None:
            return myDict[using][0]



def joint(myDict, listofAbb):
    acc = 1
    for ele in listofAbb:

        acc = acc * myDict[ele][0]
    return acc
       
        

def marginal(myDict,using):
    if using == 'P':
        return myDict['P'][0]
    elif using == '~P':
        return myDict['~P'][0]
    elif using == 'S':
        return myDict['S'][0]
    elif using == '~S':
        return myDict['~S'][0]
    elif using == 'C':
        return myDict['CPS'][0]*myDict['P'][0]*myDict['S'][0]+myDict['C~PS'][0]*myDict['~P'][0]*myDict['S'][0]+myDict['CP~S'][0]*myDict['P'][0]*myDict['~S'][0]+myDict['C~P~S'][0]*myDict['~P'][0]*myDict['~S'][0]
    elif using == '~C':
        return 1 - marginal(myDict,'C')
    elif using == 'X':
        return myDict['XC'][0]*marginal(myDict,'C') + myDict['X~C'][0]*marginal(myDict,'~C')
    elif using == '~X':
        return 1 - marginal(myDict,'X')
    elif using == 'D':
        return myDict['DC'][0]*marginal(myDict,'C') + myDict['D~C'][0]*marginal(myDict,'~C')
    elif using == '~D':
        return 1 - marginal(myDict,'D')



myDict = {}
myDict['P'] = [.9,None]
myDict['~P'] = [.1,None]
myDict['S'] = [.3,None]
myDict['~S'] = [.7,None]
myDict['CPS'] = [.03,['P','S']]
myDict['C~PS'] = [.05,['P','S']]
myDict['CP~S'] = [.001,['P','S']]
myDict['C~P~S'] = [.02,['P','S']]
myDict['~CPS'] = [.97,['P','S']]
myDict['~C~PS'] = [.95,['P','S']]
myDict['~CP~S'] = [.999,['P','S']]
myDict['~C~P~S'] = [.98,['P','S']]
myDict['XC'] = [.9,['C']]
myDict['X~C'] = [.2,['C']]
myDict['DC'] = [.65,['C']]
myDict['D~C'] = [.3,['C']]
myDict['~XC'] = [.1,['C']]
myDict['~X~C'] = [.8,['C']]
myDict['~DC'] = [.35,['C']]
myDict['~D~C'] = [.7,['C']]

probType = sys.argv[1]
changes = sys.argv[2]
if changes != 'None':
    for ele in changes.split(","):
        myDict[ele[:1]][0] = float(ele[1:])
if probType == 'm': #marginal
    print marginal(myDict,sys.argv[3])
elif probType == 'j': #joint
    print joint(myDict,sys.argv[3].split(","))
elif probType == 'c': #conditional
    conditionals = sys.argv[3].split(",")
    isFirst = True
    listofAbb = []
    for ele in conditionals:
        if isFirst:
            using = ele
            isFirst = False
        else:
            listofAbb.append(ele)
    print conditional(myDict,using,listofAbb)


