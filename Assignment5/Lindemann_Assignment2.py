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

    finalAbove = (.8*valueAbove + .1*valueLeft + .1*valueRight)
    finalBelow = (.8*valueBelow + .1*valueLeft + .1*valueRight)
    finalLeft = (.8*valueLeft + .1*valueAbove + .1*valueBelow)
    finalRight = (.8*valueRight + .1*valueAbove + .1*valueBelow)
    if finalAbove > finalBelow and finalAbove > finalRight and finalAbove > finalLeft:
        return [node,'up',finalAbove]
    elif finalBelow > finalLeft and finalBelow > finalRight:
        return [node,'down', finalBelow]
    elif finalLeft > finalRight:
        return [node,'left',finalLeft]
    else:
        return [node,'right',finalRight]

def valueIteration(graph,eps):

    V = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],]
    Vprime = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
    while True:
        for x in range (0,10):
            for y in range (0,8):
                V[y][x] = bestReward(graph,x,y,eps)
        
        V[0][9] = [9,"stay",50]
        return V

readInGraph = sys.argv[1]
eps = sys.argv[2]
graphDict = {}
simpleGraph = {}

graph = Graph()

graphDict = readFile(graphDict,readInGraph)
simpleGraph = addVerticesToGraph(simpleGraph,graphDict)
graph = addEdgesToGraph(graph,simpleGraph)


V = valueIteration(graph,float(eps))


print "Nodes named 0-9 in first row, 10-19 in second, etc.."
print "[Node name,'direction to go', weight", V
