import numpy as np
from queue import Queue
from queue import LifoQueue
import heapq
from termcolor import colored



bfsQ = Queue()
aStarQ = []
heapq.heapify(aStarQ)
dfsQ = LifoQueue()



def bredthFirstSearch(Maze):
    currentNode = Node(Maze.startCoord[0], Maze.startCoord[1])
    while not(currentNode.xCoord == Maze.goalCoord[0] and currentNode.yCoord == Maze.goalCoord[1]):
        Maze.visitedNodes[currentNode.xCoord, currentNode.yCoord] = 2
        enqueueLegalMoves(currentNode, Maze, bfsQ)
        currentNode = bfsQ.get()

    print("Goal Found")
    return givePath(currentNode, Maze)

def depthFirstSearch(Maze):
    currentNode = Node(Maze.startCoord[0], Maze.startCoord[1])
    while not (currentNode.xCoord == Maze.goalCoord[0] and currentNode.yCoord == Maze.goalCoord[1]):
        Maze.visitedNodes[currentNode.xCoord, currentNode.yCoord] = 2
        enqueueLegalMoves(currentNode, Maze, dfsQ)
        currentNode = dfsQ.get()

    print("Goal Found")

    return givePath(currentNode, Maze)

def aStarSearch(Maze):
    currentNode = Node(Maze.startCoord[0], Maze.startCoord[1])
    while not (currentNode.xCoord == Maze.goalCoord[0] and currentNode.yCoord == Maze.goalCoord[1]):
        Maze.visitedNodes[currentNode.xCoord, currentNode.yCoord] = 2
        enqueueLegalMoves(currentNode, Maze, aStarQ, True)
        currentNode = heapq.heappop(aStarQ)[1]

    print("Goal Found")

    return givePath(currentNode, Maze)

def givePath(currentNode, Maze):
    path = []
    print("Num Nodes in Path")
    print(currentNode.distFromStart)
    while(currentNode.previousNode != None):
        path.append(currentNode)
        Maze.visitedNodes[currentNode.xCoord, currentNode.yCoord] = 3
        currentNode = currentNode.previousNode
    path.append(currentNode)
    return path

class Node:
    def __init__(self, xCoord, yCoord, distFromStart = 0, previousNode = None, priority = 0):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.distFromStart = distFromStart
        self.previousNode = previousNode
        self.priority = priority

    def __lt__(self, other):
        return (self.xCoord + self.yCoord) < (other.xCoord + other.yCoord)

class Maze:
    def __init__(self, mazeMatrix, startCoord = [0,0], goalCoord = [24,24]):
        self.mazeMatrix = mazeMatrix
        self.startCoord = startCoord
        self.goalCoord = goalCoord
        #1 means in the queue, 2 means ACTUALLY visited, 3 means on the path
        self.visitedNodes = np.zeros((len(mazeMatrix), len(mazeMatrix[0])))

    def displayMaze(self):
        for i in range(len(self.mazeMatrix[1]) - 1, -1, -1):
             for j in range(len(self.mazeMatrix[0])):
                 if (self.mazeMatrix[i][j] == 1):
                     print('| # ', end="")
                 elif(self.startCoord[0] == i and self.startCoord[1] == j):
                     print('|' + colored(' S ', 'blue'), end="")
                 elif(self.goalCoord[0] == i and self.goalCoord[1] == j):
                     print('|' + colored(' G ', 'green'), end="")
                 elif(self.visitedNodes[i][j] == 3):
                     print('|' + colored(' * ', 'magenta'), end="")
                 elif (self.visitedNodes[i][j] == 2):
                     print('|' + colored(' * ', 'red'), end="")
                 else:
                     print('|   ', end="")
             print("| \n")

def enqueueLegalMoves(currentNode, Maze, queue, priorityCheck = False):
    x = currentNode.xCoord
    y = currentNode.yCoord

    if(priorityCheck == False):
        if (not(x == 24) and (Maze.mazeMatrix[x+1][y] == 0) and (Maze.visitedNodes[x+1][y] == 0)):
            newNode = Node(x+1, y, currentNode.distFromStart + 1, currentNode)
            Maze.visitedNodes[currentNode.xCoord + 1, currentNode.yCoord] = 1
            queue.put(newNode)
        if (not(y == 24) and (Maze.mazeMatrix[x][y+1] == 0) and (Maze.visitedNodes[x][y+1] == 0)):
            newNode = Node(x, y+1, currentNode.distFromStart + 1, currentNode)
            Maze.visitedNodes[currentNode.xCoord, currentNode.yCoord + 1] = 1
            queue.put(newNode)
        if (not(x == 0) and (Maze.mazeMatrix[x-1][y] == 0) and (Maze.visitedNodes[x-1][y] == 0)):
            newNode = Node(x-1, y, currentNode.distFromStart + 1, currentNode)
            Maze.visitedNodes[currentNode.xCoord - 1, currentNode.yCoord] = 1
            queue.put(newNode)
        if (not(y == 0) and (Maze.mazeMatrix[x][y-1] == 0) and (Maze.visitedNodes[x][y-1] == 0)):
            newNode = Node(x, y-1, currentNode.distFromStart + 1, currentNode)
            Maze.visitedNodes[currentNode.xCoord, currentNode.yCoord - 1] = 1
            queue.put(newNode)
    else:
        if (not(x == 24) and (Maze.mazeMatrix[x+1][y] == 0) and (Maze.visitedNodes[x+1][y] == 0)):
            newNode = Node(x+1, y, currentNode.distFromStart + 1, currentNode)
            Maze.visitedNodes[currentNode.xCoord + 1, currentNode.yCoord] = 1
            priority = newNode.distFromStart + mazeHeuristicBasic(newNode, Maze.goalCoord)
            heapq.heappush(queue, (priority, newNode))
        if (not(y == 24) and (Maze.mazeMatrix[x][y+1] == 0) and (Maze.visitedNodes[x][y+1] == 0)):
            newNode = Node(x, y+1, currentNode.distFromStart + 1, currentNode)
            Maze.visitedNodes[currentNode.xCoord, currentNode.yCoord + 1] = 1
            priority = newNode.distFromStart + mazeHeuristicBasic(newNode, Maze.goalCoord)
            heapq.heappush(queue, (priority, newNode))
        if (not(x == 0) and (Maze.mazeMatrix[x-1][y] == 0) and (Maze.visitedNodes[x-1][y] == 0)):
            newNode = Node(x-1, y, currentNode.distFromStart + 1, currentNode)
            Maze.visitedNodes[currentNode.xCoord - 1, currentNode.yCoord] = 1
            priority = newNode.distFromStart + mazeHeuristicBasic(newNode, Maze.goalCoord)
            heapq.heappush(queue, (priority, newNode))
        if (not(y == 0) and (Maze.mazeMatrix[x][y-1] == 0) and (Maze.visitedNodes[x][y-1] == 0)):
            newNode = Node(x, y-1, currentNode.distFromStart + 1, currentNode)
            Maze.visitedNodes[currentNode.xCoord, currentNode.yCoord - 1] = 1
            priority = newNode.distFromStart + mazeHeuristicBasic(newNode, Maze.goalCoord)
            heapq.heappush(queue, (priority, newNode))


def printPath(path):
    for i in range(len(path)):
        print("[", end= "")
        print(path[i].xCoord, end ="")
        print(",", end = "")
        print(path[i].yCoord, end="")
        print("] , ", end= "")

def mazeHeuristicBasic(node, goalCoordinates):
    xDistanceToGoal = np.abs(goalCoordinates[0] - node.xCoord)
    yDistanceToGoal = np.abs(goalCoordinates[1] - node.yCoord)

    minimumMovesNeeded = xDistanceToGoal + yDistanceToGoal

    return minimumMovesNeeded




mazeMatrix = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]])


# startingCoordinates = [12,2]
# goalCoordinates = [19,23]

# startingCoordinates = [12,2]
# goalCoordinates = [21,2]

startingCoordinates = [0,0]
goalCoordinates = [24,24]

maze = Maze(mazeMatrix, startingCoordinates, goalCoordinates)



#path = depthFirstSearch(maze)
#path = bredthFirstSearch(maze)
path = aStarSearch(maze)

maze.displayMaze()

#print(len(path))

printPath(path)

numNodesExplored = 0

for i in range(len(maze.mazeMatrix[0])):
    for j in range(len(maze.mazeMatrix[1])):
        if(maze.visitedNodes[i,j] == 2 or maze.visitedNodes[i,j] == 3):
            numNodesExplored +=1

print("")
print("Num Nodes Expolored: " , end="")
print(numNodesExplored)




#node = dequeueNode()

#rint(node)


