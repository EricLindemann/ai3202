import sys




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



def conditional(myDict,using,listofAbb):
    print 'using = ', using, ' listofAbb =', listofAbb
    if listofAbb == None or len(listofAbb) == 0: #calc marginal
        return myDict[using][0]

    if len(listofAbb) == 1: #conditioned on one parameter 
        if myDict[using][1] == None and myDict[listofAbb[0]][1] == None: #S and P
            return myDict[using][0]

        elif using == 'S' or using == 'P' or using == '~P' or using == '~S':#deprecated
            if listofAbb[0] == 'CPS' or listofAbb[0] == '~CPS' or  listofAbb[0] == 'C~PS' or listofAbb[0] == '~C~PS' or listofAbb[0] == 'CP~S' or  listofAbb[0] == '~CP~S' or listofAbb[0] == 'C~P~S' or listofAbb[0] == '~C~P~S': #S conditioned on CPS
                tempList = []
                tempList.append(using)
                return condtional(myDict,listofAbb,tempList)*myDict[using][0] /myDict[listofAbb[0]][0]

            elif listofAbb[0] == 'XC' or listofAbb[0] == 'X~C' or listofAbb[0] == '~XC' or listofAbb[0] == '~X~C' or listofAbb[0] == 'DC' or listofAbb[0] == '~DC' or   listofAbb[0] == 'D~C' or listofAbb[0] == '~D~C':
                return condtional(myDict,using,'CPS')*condtional(myDict,'CPS',listofAbb) + conditional(myDict,using,'~CPS')*conditional(myDict,'~CPS',listofAbb)
       
        elif using == 'CPS' or using == '~CPS' or using == 'C~PS' or using  == '~C~PS' or using == 'CP~S' or using == '~CP~S' or using == 'C~P~S' or using == '~C~P~S': 
            if listofAbb[0] == 'P' or listofAbb[0] == '~P':
                list1 = listofAbb.append('S')
                list2 = listofAbb.append('~S')
                return conditional(myDict,using,list1)*myDict['S'][0] + conditional(myDict,using,list2)*myDict['~S'][0]

            elif listofAbb[0] == 'S' or listofAbb[0] == '~S':
                list1 = listofAbb.append('P')
                list2 = listofAbb.append('~P')
                return conditional(myDict,using,list1)*myDict['P'][0] + condtional(myDict,using,list2)*myDict['~P'][0]
            
            elif listofAbb[0] == 'XC' or listofAbb[0] == 'X~C' or listofAbb[0] == '~XC' or listofAbb[0] == '~X~C' or listofAbb[0] == 'DC' or listofAbb[0] == '~DC' or   listofAbb[0] == 'D~C' or listofAbb[0] == '~D~C':
                tempList = []
                tempList.append(using)
                return conditional(myDict,listofAbb[0], tempList)*myDict[listofAbb[0]][0]/myDict[using][0]
         
        elif  using == 'XC' or using == 'X~C' or using == '~XC' or using == '~X~C' or using == 'DC' or using == '~DC' or using == 'D~C' or using == '~D~C':
            if listofAbb[0] == 'CPS' or listofAbb[0] == '~CPS' or  listofAbb[0] == 'C~PS' or listofAbb[0] == '~C~PS' or listofAbb[0] == 'CP~S' or  listofAbb[0] == '~CP~S' or listofAbb[0] == 'C~P~S' or listofAbb[0] == '~C~P~S':         
                return myDict[using][0]
            else:
                tempList = []
                tempList.append('CPS')
                tempNegatedList = []
                tempNegatedList.append('~CPS')
                print "listofAbb before entering is: ", listofAbb
                return conditional(myDict,using,tempList)*conditional(myDict,'CPS',listofAbb) + conditional(myDict,using,tempNegatedList) * conditional(myDict,'~CPS',listofAbb) #same for S,P or D,X




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
elif probType == 'g': #conditional
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


