import random
import matplotlib.pyplot as plt
import numpy as np
from termcolor import colored

def easomFunc(x1,x2):
    val = -np.cos(x1)*np.cos(x2)*np.exp(-(x1 - np.pi)**2 - (x2 - np.pi)**2)
    return val

def generateInitialPoints():
    initialPoints = []
    for i in range(10):
        initialPoints.append([random.uniform(-10,10), random.uniform(-10,10)])
    return initialPoints

def generateInitialTemps():
    initialTemps = np.zeros(10)
    for i in range(len(initialTemps)):
        initialTemps[i] = random.uniform(0.001,1)
    return initialTemps

def generateAlphas(min, max):
    alphas = np.zeros(3)
    for i in range(len(alphas)):
        alphas[i] = random.uniform(min,max)
    return alphas

def findNeighbour(currentPoint):
    maxDist = 3.0
    newPoint = [currentPoint[0] + random.uniform(-maxDist, maxDist), currentPoint[1] + random.uniform(-maxDist, maxDist)]
    if (newPoint[0] > 10):
        newPoint[0] = 10
    elif(newPoint[0] < -10):
        newPoint[0] = -10
    if (newPoint[1] > 10):
        newPoint[1] = 10
    elif (newPoint[1] < -10):
        newPoint[1] = -10

    return newPoint


def acceptanceAlgorithm(changeInCost, temperature):
    if (changeInCost <= 0):
        return True
    else:
        exponent = (-changeInCost/temperature)
        prob = np.exp(exponent)
        check = random.uniform(0,1)
        if(check < prob):
            return True
        else:
            return False

def annealingScheduleLinear(temp, alpha):
    newTemp = temp - alpha
    return  newTemp

def annealingScheduleExpo(temp, alpha):
    newTemp = temp*alpha
    return  newTemp

def annealingScheduleSlow(temp, alpha):
    newTemp = temp/(1+alpha*temp)
    return  newTemp

def simulatedAnnealingLinear(initialPoint, initialTemp, alpha):
    currentPoint = initialPoint
    currentTemp = initialTemp
    currentCost = easomFunc(currentPoint[0], currentPoint[1])
    tempIterations = 100
    while (currentTemp >= 0.0001):
        newCandidatePoint = findNeighbour(currentPoint)
        changeInCost = easomFunc(newCandidatePoint[0], newCandidatePoint[1]) - currentCost
        if(acceptanceAlgorithm(changeInCost, currentTemp)):
            currentPoint = newCandidatePoint
        if(tempIterations == 0):
            currentTemp = annealingScheduleLinear(currentTemp, alpha)
            tempIterations = 100
        else:
            tempIterations -= 1

    return currentPoint


def simulatedAnnealingExpo(initialPoint, initialTemp, alpha):
    currentPoint = initialPoint
    currentTemp = initialTemp
    currentCost = easomFunc(currentPoint[0], currentPoint[1])
    tempIterations = 100
    while (currentTemp >= 0.0001):
        newCandidatePoint = findNeighbour(currentPoint)
        changeInCost = easomFunc(newCandidatePoint[0], newCandidatePoint[1]) - currentCost
        if(acceptanceAlgorithm(changeInCost, currentTemp)):
            currentPoint = newCandidatePoint
        if(tempIterations == 0):
            currentTemp = annealingScheduleExpo(currentTemp, alpha)
            tempIterations = 100
        else:
            tempIterations -= 1

    return currentPoint


def simulatedAnnealingSlow(initialPoint, initialTemp, alpha):
    currentPoint = initialPoint
    currentTemp = initialTemp
    currentCost = easomFunc(currentPoint[0], currentPoint[1])
    while (currentTemp >= 0.0001):
        newCandidatePoint = findNeighbour(currentPoint)
        changeInCost = easomFunc(newCandidatePoint[0], newCandidatePoint[1]) - currentCost
        if(acceptanceAlgorithm(changeInCost, currentTemp)):
            currentPoint = newCandidatePoint

        currentTemp = annealingScheduleSlow(currentTemp, alpha)


    return currentPoint



initialPoints = generateInitialPoints()
initialTemps = generateInitialTemps()
alphasLin = generateAlphas(0.001,0.005)
alphasExpo = generateAlphas(0.95,1)
alphasSlow = generateAlphas(0.1,0.5)

LinPoints = []
ExpoPoints = []
SlowPoints = []
count56 = 0
count67 = 0
count78 = 0
count89 = 0
count910 =0
count = 0
print(colored("Linear Annealing", 'red'))
print("")
for i in range(len(initialPoints)):
    for j in range(len(initialTemps)):
        for k in range(len(alphasLin)):
            point = simulatedAnnealingLinear(initialPoints[i], initialTemps[j], alphasLin[k])
            # LinPoints.append((point))
            if(easomFunc(point[0], point[1]) < -0.01):
                LinPoints.append((point))
                print("Best", end="")
                print(initialPoints[i])
                print(initialTemps[j])
                print(alphasLin[k])

print("")
print("")
print(colored("Expo Annealing", 'magenta'))
print("")
for i in range(len(initialPoints)):
    for j in range(len(initialTemps)):
        for k in range(len(alphasExpo)):
            point = simulatedAnnealingExpo(initialPoints[i], initialTemps[j], alphasExpo[k])
            # ExpoPoints.append((point))
            if(easomFunc(point[0], point[1]) < -0.01):
                ExpoPoints.append((point))
                print("Best", end="")
                print(initialPoints[i])
                print(initialTemps[j])
                print(alphasExpo[k])

print("")
print("")
print(colored("Slow Annealing", 'green'))
print("")
for i in range(len(initialPoints)):
    for j in range(len(initialTemps)):
        for k in range(len(alphasSlow)):
            point = simulatedAnnealingSlow(initialPoints[i], initialTemps[j], alphasSlow[k])
            # SlowPoints.append((point))
            if(easomFunc(point[0], point[1]) < -0.01):
                SlowPoints.append((point))
                print("Best", end="")
                print(initialPoints[i])
                print(initialTemps[j])
                print(alphasSlow[k])


ax = plt.axes(projection='3d')

x1 = np.arange(-100, 100, 0.1)
x2 = np.arange(-100, 100, 0.1)

xx1, xx2, = np.meshgrid(x1, x2)

func = -np.cos(xx1) * np.cos(xx2) * np.exp(-(xx1 - np.pi) ** 2 - (xx2 - np.pi) ** 2)

ax.plot_surface(xx1, xx2, func)
for point in LinPoints:
    ax.scatter(point[0], point[1], easomFunc(point[0], point[1]), c='red')
for point in ExpoPoints:
    ax.scatter(point[0], point[1], easomFunc(point[0], point[1]), c='magenta')
for point in SlowPoints:
    ax.scatter(point[0], point[1], easomFunc(point[0], point[1]), c='green')

plt.show()



