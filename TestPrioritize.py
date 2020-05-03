from random import randint, randrange
import time
from math import floor

class test:
    def __init__(self, tName, tPass, tTime, tRatio):
        self.name = tName
        self.succeed = tPass,
        self.duration = tTime
        self.PRatio = tRatio

def generateData(maxRange, minRand, maxRand, passRatio):
    generData = list()
    cur_testCase = 0
    for row in range(maxRange):
        #generate data
        cur_testCase += 1
        cur_timeSinceFail = randint(minRand, maxRand)
        cur_timeSinceRun = randint(minRand, maxRand)
        cur_timesRun = randint(minRand, maxRand)
        cur_FailureRatio = randint(minRand, cur_timesRun) / cur_timesRun 
        #generate pass/fail
        passes_num = randint(minRand, maxRand)
        if passes_num > maxRand * passRatio:
            passes = False
        else:
            passes = True
        cur_data = (cur_testCase, passes, cur_timeSinceFail, cur_timeSinceRun, cur_FailureRatio)
        generData.append(cur_data)
    
    return generData

def findMin(data, index):
    
    curMin = 10000000
    curMinIndex = -1
    curIndex = 0
    for num in data:
        if num[index] < curMin:
            curMin = num[index]
            curMinIndex = curIndex
        curIndex += 1
        
    return curMinIndex

def findMax(data, index):
    curMax = -1
    curMaxIndex = -1
    curIndex = 0
    for num in data:
        if num[index] > curMax:
            curMax = num[index]
            curMaxIndex = curIndex
        curIndex += 1
        
    return curMaxIndex
            
#prioritizes based on most recently failed tests only
def timeSinceFail_Heuristic(testData):
    startTime = time.clock()
    testQueue = list()
    while len(testData) > 0:
        curMin = findMin(testData, 2)
        testQueue.append(testData[curMin])
        testData.pop(curMin)
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return (testQueue, elapsed)

#prioritizes based on cur_TimeSinceRun only
def timeSinceRun_Heuristic(testData):
    startTime = time.clock()
    testQueue = list()
    while len(testData) > 0:
        curMax = findMax(testData, 3)
        testQueue.append(testData[curMax])
        testData.pop(curMax)
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return (testQueue, elapsed)

#prioritizes based on failure ratio only (higher ratio preferred)
def failureRatio_Heuristic(testData):
    startTime = time.clock()
    testQueue = list()
    while len(testData) > 0:
        curMax = findMax(testData, 4)
        testQueue.append(testData[curMax])
        testData.pop(curMax)
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return (testQueue, elapsed)

#assigns priority levels
'''
nextObj = [testCaseNumber, pass/fail boolean, timeSinceLastFail, timeSinceLastRun, testFailureRatio]
'''
def combination_Heuristic(testData, failRatio):
    startTime = time.clock()
    testQueue = list()
    while len(testData) > 0:
        nextObj = testData.pop()
        nextPriority = -1
        if nextObj[2] == nextObj[3]: #if test failed the last time it was run
            nextPriority = 1
        elif nextObj[4] >= failRatio: #if test's failure ratio is >= failRatio parameter
            nextPriority = 2
        else:
            priorityCalc = (nextObj[2] + nextObj[4] * 1.5 + nextObj[3] * 5)
            nextPriority = floor(priorityCalc)
        sortedInsert(testQueue, (nextPriority, nextObj[0]))
    endTime = time.clock()
    elapsed = endTime - startTime
        
    return (testQueue, elapsed)
        

#test order randomly selected
def random(testData):
    #time sort
    startTime = time.clock()
    ordered = list()
    maxRand = len(testData)
    for cur in range(maxRand):
        curTestNum = randrange(0, len(testData))
        curTest = testData.pop(curTestNum)
        ordered.append((curTest[0], curTest[1]))
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return (ordered, elapsed)
    
def sortedInsert(curQueue, newObj):
    if newObj[0] > 2:
        for index in range(len(curQueue), 0, -1):
            if curQueue[index][0] < newObj[0]:
                break
    else:
        for index in range(len(curQueue)):
            if curQueue[index][0] > newObj[0]:
                break
    curQueue.insert(index, newObj)
    
def simulate_tests(tests):
    startTime = time.clock()
    for test in tests:
        if test[1] == False:
            break
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return elapsed
    
def compareResults(method1, method2, method1_failTime, method2_failTime):
    faster = min(method1_failTime, method2_failTime)
    if faster == method1_failTime:
        fasterMethod = method1
        slowerMethod = method2
        slower = method2_failTime
    else:
        fasterMethod = method2
        slowerMethod = method1
        slower = method1_failTime
        
    print(fasterMethod, " failed ", slower - faster, " seconds faster than ", slowerMethod)
    timesFaster = slower / faster
    if timesFaster == 1:
        timesFaster = 0
    print("(", timesFaster, " times faster)")
    print()
    
    
#main function
data = generateData(1000000, 1, 1000000, .8)
rand = random(data)
rand_timeToFail = simulate_tests(rand[0])
lastFail = timeSinceFail_Heuristic(data)
lastFail_timeToFail = simulate_tests(lastFail[0])
notRun = timeSinceRun_Heuristic(data)
notRun_timeToFail= simulate_tests(notRun[0])
failRatio = failureRatio_Heuristic(data)
failRatio_timeToFail = simulate_tests(failRatio[0])
combine = combination_Heuristic(data, .7)
combine_timeToFail = simulate_tests(combine[0])


#print results
print("Time to sort tests:")
print("RecentlyFailedHeuristic (RFH): ", lastFail[1], " seconds")
print("NotRunRecentlyHeuristic (NRRH): ", notRun[1], " seconds")
print("FailureRatioHeuristic (FRH): ", failRatio[1], " seconds")
print("CombinationHeuristic (CH): ", combine[1], " seconds")
print()
print("Time to first failure:")
print("Random: ", rand_timeToFail, " seconds")
print("RFH: ", lastFail_timeToFail, " seconds")
print("NRRH: ", notRun_timeToFail, " seconds")
print("FRH: ", failRatio_timeToFail, " seconds")
print("CH: ", combine_timeToFail, " seconds")
print()
compareResults("RFH", "random", lastFail_timeToFail, rand_timeToFail)
compareResults("NRRH", "random", notRun_timeToFail, rand_timeToFail)
compareResults("FRH", "random", failRatio_timeToFail, rand_timeToFail)
compareResults("CH", "random", combine_timeToFail, rand_timeToFail)
compareResults("NRRH", "RFH", notRun_timeToFail, lastFail_timeToFail)
compareResults("RFH", "FRH", lastFail_timeToFail, failRatio_timeToFail)
compareResults("NRRH", "FRH", notRun_timeToFail, failRatio_timeToFail)
compareResults("CH", "RFH", combine_timeToFail, lastFail_timeToFail)
compareResults("CH", "NRRH", combine_timeToFail, notRun_timeToFail)
compareResults("CH", "FRH", combine_timeToFail, failRatio_timeToFail)