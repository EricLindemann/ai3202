from Graph import Graph
import math
import sys


def readFile(graphDict,readInGraph):
    f = open(readInGraph, 'r')
    i = 0
    for line in f:
        line = line.strip()
        j = line.split(" ")
        graphDict[i] = j
        i = i+1
    return graphDict

def addVerticesToGraph(simpleGraph, graphDict):
    rows = len(graphDict.keys())
    columns = len(graphDict[0])
    vertexName = 0
    #adds vertices to graph
    for i in range (0,rows):
        for j in range (0,columns):
            graph.addVertex(vertexName)
            simpleGraph[vertexName] = graphDict[i][j]
            vertexName = vertexName + 1
    return simpleGraph

#adds edges to vertices in graph
def addEdgesToGraph(graph,simpleGraph):
    for i in range (0,80):
        if (i%10-1) >= 0: #node exists to left
            if int(simpleGraph[i-1]) == 0:
                graph.addEdge(i,i-1,0)
            elif int(simpleGraph[i-1]) == 1:
                graph.addEdge(i,i-1,-1)
            elif int(simpleGraph[i-1]) == 2:
                graph.addEdge(i,i-1,None)
            elif int(simpleGraph[i-1]) == 3:
                graph.addEdge(i,i-1,-2)
            else:
                graph.addEdge(i,i-1,1)

        if (i%10+1) <= 9: #node exists to right
            if int(simpleGraph[i+1]) == 0:
                graph.addEdge(i,i+1,0)
            elif int(simpleGraph[i+1]) == 1:
                graph.addEdge(i,i+1,-1)
            elif int(simpleGraph[i+1]) == 2:
                graph.addEdge(i,i+1,None)
            elif int(simpleGraph[i+1]) == 3:
                graph.addEdge(i,i+1,-2)
            elif int(simpleGraph[i+1]) == 50:
                graph.addEdge(i,i+1,50)
            else:
                graph.addEdge(i,i+1,1)


        if i in range(0,70): #node exists below
            if int(simpleGraph[i+10]) == 0:
                graph.addEdge(i,i+10,0)
            elif int(simpleGraph[i+10]) == 1:
                graph.addEdge(i,i+10,-1)
            elif int(simpleGraph[i+10]) == 2:
                graph.addEdge(i,i+10,None)
            elif int(simpleGraph[i+10]) == 3:
                graph.addEdge(i,i+10,-2)
            else:
                graph.addEdge(i,i+10,1)


        if i in range (10,80): #node exists above
            if int(simpleGraph[i-10]) == 0:
                graph.addEdge(i,i-10,0)
            elif int(simpleGraph[i-10]) == 1:
                graph.addEdge(i,i-10,-1)
            elif int(simpleGraph[i-10]) == 2:
                graph.addEdge(i,i-10,None)
            elif int(simpleGraph[i-10]) == 3:
                graph.addEdge(i,i-10,-2)
            elif int(simpleGraph[i-10]) == 50:
                graph.addEdge(i,i-10,50)
            else:
                graph.addEdge(i,i-10,1)



    return graph


def bestReward(graph,x,y,eps):
    node = y*10 + x
    if (node%10-1) >= 0: #node exists to left
        valueLeft = graph.getWeight(node,node-1)
    else:
        valueLeft = None
    if (node%10+1) <= 9: #node exists to right
        valueRight = graph.getWeight(node,node+1)
    else:
        valueRight = None
    if node in range (10,80): #node exists above
        valueAbove = graph.getWeight(node,node-10)
    else:
        valueAbove = None
    if node in range (0,70): #node exists below
        valueBelow = graph.getWeight(node,node+10)
    else:
        valueBelow = None
    
    if valueLeft != None:
        valueLeft = valueLeft+eps
    else:
        valueLeft = eps
    if valueRight != None:
        valueRight = valueRight+eps
    else:
        valueRight = eps
    if valueBelow != None:
        valueBelow = valueBelow+eps
    else:
        valueBelow = eps
    if valueAbove != None:
        valueAbove = valueAbove+eps
    else:
        valueAbove = eps

    finalAbove = .9*(.8*valueAbove + .1*valueLeft + .1*valueRight)
    finalBelow = .9*(.8*valueBelow + .1*valueLeft + .1*valueRight)
    finalLeft = .9*(.8*valueLeft + .1*valueAbove + .1*valueBelow)
    finalRight = .9*(.8*valueRight + .1*valueAbove + .1*valueBelow)
    if finalAbove > finalBelow and finalAbove > finalRight and finalAbove > finalLeft:
        if node > 10:    
            if graph.getWeight(node-10,node) != None:
                return ['up',graph.getWeight(node-10,node)+finalAbove]
            else:
                return['up',finalAbove]
        elif graph.getWeight(node+10,node) != None:
            return ['up',graph.getWeight(node+10,node)+finalAbove]
        else:
            return['up',finalAbove]
    elif finalBelow > finalLeft and finalBelow > finalRight:
        if node < 70:    
            if graph.getWeight(node+10,node) != None:
                return ['down', graph.getWeight(node+10,node)+finalBelow]
            else:
                return['down',finalBelow]
        elif graph.getWeight(node-10,node) != None:
            return ['down', graph.getWeight(node-10,node)+finalBelow]
        else:
            return['down',finalBelow]
    elif finalLeft > finalRight:
        if node != 50 and node != 60:
            if graph.getWeight(node-1,node) != None:
                return ['left',graph.getWeight(node-1,node)+finalLeft]
            else:
                return ['left',finalLeft]
        elif graph.getWeight(node+1,node) != None:
            return ['left', graph.getWeight(node+1,node)+finalLeft]
        else:
            return['left',finalLeft]
    else:
        if node%10 != 9:
            if graph.getWeight(node+1,node) != None:
                return ['right',graph.getWeight(node+1,node)+finalRight]
            else: 
                return ['right',finalRight]
        elif graph.getWeight(node-1,node) != None:
            return ['right', graph.getWeight(node-1,node)+finalRight]
        else:
            return['right',finalRight]
def valueIteration(graph,eps):

    Vold = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
    Vnew = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
    for x in range (0,10):
        for y in range (0,8):
            Vold[y][x] = bestReward(graph,x,y,eps)
    for x in range (0,10):
        for y in range (0,8):
            delta = 10000
            while delta > eps*(1-.9)/.9:
                if Vold[y][x][0] == 'left' and x > 0:
                    Vnew[y][x] = bestReward(graph,(x-1),y,eps)
                elif Vold[y][x][0] == 'right' and x < 9: 
                    Vnew[y][x] = bestReward(graph,(x+1),y,eps)
                elif Vold[y][x][0] == 'up' and y < 7:
                    Vnew[y][x] = bestReward(graph,x,(y+1),eps)
                elif Vold[y][x][0] == 'down' and y > 0:
                    Vnew[y][x] = bestReward(graph,x,(y-1),eps)
                else:
                    Vnew[y][x] = bestReward(graph,x,y,eps)
                delta = Vold[y][x][1] - Vnew[y][x][1]
                Vold[y][x] = Vnew[y][x]
            
             

    Vold[0][9] = ["stay",50]
    return Vold

readInGraph = sys.argv[1]
eps = sys.argv[2]
graphDict = {}
simpleGraph = {}

graph = Graph()

graphDict = readFile(graphDict,readInGraph)
simpleGraph = addVerticesToGraph(simpleGraph,graphDict)
graph = addEdgesToGraph(graph,simpleGraph)


V = valueIteration(graph,float(eps))
print "node (0,0) is bottom left, (0,1) is above that, (1,0) is to the right:"
i = 7
j = 0
for valueRow in V:
    for value in valueRow:
        print "(",j,",",i,"):",value
        j = j + 1
    i = i - 1
    j = 0

#print "Nodes named 0-9 in first row, 10-19 in second, etc.."
#print "[Node name,'direction to go', weight", V
