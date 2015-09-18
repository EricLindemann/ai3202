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
    for i in range (0,79):
        if (i%10-1) >= 0: #node exists to left
            if int(simpleGraph[i-1]) == 0:
                graph.addEdge(i,i-1,10)
            elif int(simpleGraph[i-1]) == 1:
                graph.addEdge(i,i-1,20)
            else:
                graph.addEdge(i,i-1,100000)
        if (i%10+1) <= 9: #node exists to right
            if int(simpleGraph[i+1]) == 0:
                graph.addEdge(i,i+1,10)
            elif int(simpleGraph[i+1]) == 1:
                graph.addEdge(i,i+1,20)
            else:
                graph.addEdge(i,i+1,100000)
        if i in range(0,70): #node exists below
            if int(simpleGraph[i+10]) == 0:
                graph.addEdge(i,i+10,10)
            elif int(simpleGraph[i+10]) == 1:
                graph.addEdge(i,i+10,20)
            else:
                graph.addEdge(i,i+10,100000)
        if i in range (10,80): #node exists above
            if int(simpleGraph[i-10]) == 0:
                graph.addEdge(i,i-10,10)
            elif int(simpleGraph[i-10]) == 1:
                graph.addEdge(i,i-10,20)
            else:
                graph.addEdge(i,i-10,100000)
        if i in range(0,70) and (i%10-1) >= 0:#node exists to the bottom-left
            if int(simpleGraph[i+9]) == 0:
                graph.addEdge(i,i+9,14)
            elif int(simpleGraph[i+9]) == 1:
                graph.addEdge(i,i+9,24)
            else:
                graph.addEdge(i,i+9,100000)       
        if i in range(0,70) and (i%10+1) <= 9:#node exists to the bottom-right
            if int(simpleGraph[i+11]) == 0:
                graph.addEdge(i,i+11,14)
            elif int(simpleGraph[i+11]) == 1:
                graph.addEdge(i,i+11,24)
            else:
                graph.addEdge(i,i+11,100000)       
        if i in range(10,80) and (i%10-1) >= 0: #node exists to upper-left
            if int(simpleGraph[i-11]) == 0:
                graph.addEdge(i,i-11,14)
            elif int(simpleGraph[i-11]) == 1:
                graph.addEdge(i,i-11,24)
            else:
                graph.addEdge(i,i-11,100000)      
        if i in range(10,80) and (i%10+1) <= 9: #node exists to upper-right
            if int(simpleGraph[i-9]) == 0:
                graph.addEdge(i,i-9,14)
            elif int(simpleGraph[i-9]) == 1:
                graph.addEdge(i,i-9,24)
            else:
                graph.addEdge(i,i-9,100000)   

    return graph

def manhattan(start):
    horizontal = 9 - start%10
    vertical = start/10
    return (vertical*7 + horizontal*7)

def diagonal(start):
    horizontal = 9 - start%10
    vertical = start/10
    final = pow(horizontal,2) + pow(vertical,2)
    final = math.sqrt(final)*14
    return final

def aStarManhattan(graph):
    closedSet = []
    openSet = []
    openSet.append(70)
    cameFrom = {}
    gScore={}
    gScore[70] = 0
    fScore = {}
    fScore[70] = manhattan(70)
    current = 100000
    i = 0
    while openSet:
        current = 10000
        for element in openSet:
            if current > fScore[element]:
                current = element
        if current == 9:
            finalReversed = [] 
            finalReversed.append(current)
            while current in cameFrom:
                current = cameFrom[current]
                finalReversed.append(current)
            final = list(reversed(finalReversed))
            print "Number of nodes evaluated =", i
            return final
        openSet.remove(current)
        closedSet.append(current)
        currentAdjacent = graph.getAllWeights(current)
        if currentAdjacent:   
           for adjacentNode in currentAdjacent:
                tentativeGScore = gScore[current] + currentAdjacent[adjacentNode]
                if adjacentNode not in openSet or tentativeGScore < gScore[adjacentNode]:
                    if adjacentNode in closedSet:
                        continue
                    i = i + 1
                    cameFrom[adjacentNode] = current
                    gScore[adjacentNode] = tentativeGScore
                    fScore[adjacentNode] = gScore[adjacentNode] + manhattan(adjacentNode)
                    if adjacentNode not in openSet:
                        openSet.append(adjacentNode)
    return "failure"

def aStarDiagonal(graph):
    closedSet = []
    openSet = []
    openSet.append(70)
    cameFrom = {}
    gScore={}
    gScore[70] = 0
    fScore = {}
    fScore[70] = diagonal(70)
    current = 100000
    i = 0
    while openSet:
        current = 10000
        for element in openSet:
            if current > fScore[element]:
                current = element
        if current == 9:
            finalReversed = [] 
            finalReversed.append(current)
            while current in cameFrom:
                current = cameFrom[current]
                finalReversed.append(current)
            final = list(reversed(finalReversed))
            print "Number of nodes evaluated =", i
            return final
        openSet.remove(current)
        closedSet.append(current)
        currentAdjacent = graph.getAllWeights(current)
        if currentAdjacent:   
           for adjacentNode in currentAdjacent:
                tentativeGScore = gScore[current] + currentAdjacent[adjacentNode]
                if adjacentNode not in openSet or tentativeGScore < gScore[adjacentNode]:
                    if adjacentNode in closedSet:
                        continue
                    i = i + 1
                    cameFrom[adjacentNode] = current
                    gScore[adjacentNode] = tentativeGScore
                    fScore[adjacentNode] = gScore[adjacentNode] + diagonal(adjacentNode)
                    if adjacentNode not in openSet:
                        openSet.append(adjacentNode)
    return "failure"

readInGraph = sys.argv[1]
heuristic = sys.argv[2]

graphDict = {}
simpleGraph = {}
graph = Graph()

graphDict = readFile(graphDict,readInGraph)
simpleGraph = addVerticesToGraph(simpleGraph,graphDict)
graph = addEdgesToGraph(graph,simpleGraph)


path = []
if heuristic == '1':
    path = aStarManhattan(graph)
elif heuristic == '2':
    path = aStarDiagonal(graph)
else:
    print "Please enter 1(manhattan) or 2(diagonal) as second argument"

print "Nodes named 0-9 in first row, 10-19 in second, etc.., path is:", path
pastElement=-1
cost = 0
for element in path:
    if pastElement != -1:
        cost = cost + graph.getWeight(pastElement,element)
    pastElement = element

print "Cost is", cost

