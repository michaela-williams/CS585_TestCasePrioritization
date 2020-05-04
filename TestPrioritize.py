import time
from random import randrange
from copy import deepcopy

maxNumTests = 300000
sortSize = 10000
        
def read_testShare():
    print("Reading in testShareData. This may take some time.")
    tests = list()
    with open('testShareData.csv.rev') as file:
        test_num = 0
        read_data = file.readline()
        for line in range(maxNumTests):
            cur_test = list()
            index = 0
            while index < 7:
                extracted_data = read_data.partition(',')
                if extracted_data[0] == '':
                    read_data = extracted_data[2]
                    continue
                if index == 0:
                    cur_test.append("test_" + str(test_num))
                elif index == 3:
                    if extracted_data[0] == 'PASSED':
                        cur_test.append(True)
                    else:
                        cur_test.append(False)
                elif index == 2 and extracted_data[0] != 'post':
                    break
                elif index == 5:
                    #convert milliseconds to seconds
                    cur_test.append(float(extracted_data[0]) / 1000)
                elif index == 6:
                    size = extracted_data[0]
                    if size == 'SMALL':
                        size_int = 1
                    elif size == 'MEDIUM':
                        size_int = 2
                    else:   #LARGE
                        size_int = 3
                    cur_test.append(size_int)
                elif not (index == 1 or index == 2 or index == 4 or index == 6):
                    cur_test.append(extracted_data[0])
                    
                read_data = extracted_data[2]
                index += 1
            if not index == 2:    
                tests.append(cur_test)
                
            test_num += 1
            read_data = file.readline()
    
    return tests
    
def read_generated():
    tests = list()
    failed = 0
    with open('TestData.csv') as file:  
        read_data = file.readline()
        while not read_data == '':
            failRatio = 0
            cur_test = list()
            for index in range(8):
                extracted_data = read_data.partition(',')
                if index == 1:
                    cur_test.append(int(extracted_data[0]))
                    if not int(extracted_data[0]):
                        failed += 1
                elif index == 2 or index == 6:
                    cur_test.append(float(extracted_data[0]))
                elif index == 3:
                    cur_test.append(int(extracted_data[0]))
                elif index == 4:
                    failRatio = float(extracted_data[0])
                elif index == 5:
                    failRatio = failRatio / float(extracted_data[0])
                    cur_test.append(failRatio)
                elif index == 7:
                    extracted_data = extracted_data[0].partition('\n')
                    cur_test.append(float(extracted_data[0]))
                else:
                    cur_test.append(extracted_data[0])
                    
                read_data = extracted_data[2]
                
            tests.append(cur_test)
            read_data = file.readline()
        print(failed)
    return tests

#test order randomly selected
def random(origData):
    testData = deepcopy(origData)
    ordered = list()
    maxRand = len(testData)
    for cur in range(maxRand):
        curTestNum = randrange(0, len(testData))
        curTest = testData.pop(curTestNum)
        ordered.append(curTest)
        
    elapsed = 0 #value to keep the return format the same as other sort functions
    
    return (ordered, elapsed)

def smallest_sort(origData):
    startTime = time.clock()
    testQueue = list()
    index = 3
    testData = deepcopy(origData)
    
    while len(testData) > 0:
        start_index = 0
        end_index = sortSize        
        while start_index < len(testData) - 1:
            if len(testData) == 1:
                testQueue.append(testData[0])  
                break
            if (end_index >= len(testData)):
                end_index = len(testData) - 1
            curSmallest = findMin(testData, index, start_index, end_index)
            testQueue.append(testData[curSmallest])
            testData.pop(curSmallest)
            start_index = end_index
            end_index += sortSize
            
        if (len(testData) == 1):
            testQueue.append(testData[0])
            testQueue.pop()
            break
        
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return (testQueue, elapsed)

#sort by highest fail ratio
def failRatio_sort(origData):
    startTime = time.clock()
    testQueue = list()
    index = 4
    testData = deepcopy(origData)
    
    while len(testData) > 0:
        start_index = 0
        end_index = sortSize
        while start_index < len(testData) - 1:
            if (end_index >= len(testData)):
                end_index = len(testData) - 1
            curLargest = findMax(testData, index, start_index, end_index)
            testQueue.append(testData[curLargest])
            testData.pop(curLargest)
            start_index = end_index
            end_index += sortSize
        
        if (len(testData) == 1):
            testQueue.append(testData[0])
            testData.pop()
            break
        
    endTime = time.clock()
    elapsed = endTime - startTime
                            
    return (testQueue, elapsed)                 

def timeFailed_sort(origData):
    startTime = time.clock()
    testQueue = list()
    index = 6
    testData = deepcopy(origData)
    
    while len(testData) > 0:
        start_index = 0
        end_index = sortSize
        while start_index < len(testData) - 1:
            if (end_index >= len(testData)):
                end_index = len(testData) - 1
            curRecent = findMin(testData, index, start_index, end_index)
            testQueue.append(testData[curRecent])
            testData.pop(curRecent)
            start_index = end_index
            end_index += sortSize
        
        if (len(testData) == 1):
            testQueue.append(testData[0])
            testQueue.pop()
            break
        
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return (testQueue, elapsed)

def timeRun_sort(origData):
    startTime = time.clock()
    testQueue = list()
    index = 5
    testData = deepcopy(origData)
    
    while len(testData) > 0:
        start_index = 0
        end_index = sortSize
        while start_index < len(testData) - 1:
            if (end_index >= len(testData)):
                end_index = len(testData) - 1
            curRecent = findMin(testData, index, start_index, end_index)
            testQueue.append(testData[curRecent])
            testData.pop(curRecent)
            start_index = end_index
            end_index += sortSize
        
        if len(testData) == 1:
            testQueue.append(testData[0])
            testData.pop()
            break        
        
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return (testQueue, elapsed)    

def combination_sort(origData):
    startTime = time.clock()
    testQueue = list()
    testData = deepcopy(origData)
    ratioIndex = 4
    sizeIndex = 3
    
    while len(testData) > 0:
        start_index = 0
        end_index = sortSize
        while start_index < len(testData) - 1:
            if end_index >= len(testData):
                end_index = len(testData) - 1
            nextTest = findBest(testData, sizeIndex, \
                                ratioIndex, start_index, end_index)
            testQueue.append(testData[nextTest])
            testData.pop(nextTest)
            start_index = end_index
            end_index += sortSize
            
        if len(testData) == 1:
            testQueue.append(testData[0])
            testData.pop()
            break
        
    endTime = time.clock()
    elapsed = endTime - startTime
            
    return (testQueue, elapsed)
    
def simulateTests(testQueue):
    duration = 2
    passed = 1
    testsRun = 0
    timeRun = 0
    for curTest in testQueue:
        testsRun += 1
        timeRun += curTest[duration]
        if not curTest[passed]:
            break
        
    report(testsRun, timeRun)

def report(testsRun, timeRun):
    units = "seconds"
    if timeRun > 60:
        timeRun = timeRun / 60
        units = "minutes"
    if timeRun > 60:
        timeRun = timeRun / 60
        units = "hours"
    print("Ran ", testsRun, "tests for ", timeRun, " ", units, " before failing.")

def report_sort(timeToSort, name):
    units = "seconds"
    if timeToSort > 60:
        timeToSort = timeToSort / 60 #convert to minutes
        units = "minutes"
    print(name, " took ", timeToSort, " ", units)

def findMin(data, index, start_index, end_index):
    curMin = 100000000
    curMinIndex = -1
    curIndex = start_index
    while curIndex < end_index:
        if data[curIndex][index] < curMin:
            curMin = data[curIndex][index]
            curMinIndex = curIndex
        curIndex += 1
        
    return curMinIndex

def findMax(data, index, start_index, end_index):
    curMax = -1
    curMaxIndex = -1
    curIndex = start_index
    while curIndex < end_index:
        if data[curIndex][index] < curMax:
            curMax = data[curIndex][index]
            curMaxIndex = curIndex
        curIndex += 1
        
    return curMaxIndex

def findBest(data, sortBy, tiebreaker, start_index, end_index):
    curBest = -1
    curBestIndex = -1
    curIndex = start_index
    while curIndex < end_index:
        if data[curIndex][sortBy] > curBest:
            curBest = data[curIndex][sortBy]
            curBestIndex = curIndex
        elif data[curIndex][sortBy] == curBest:
            if data[curBestIndex][tiebreaker] < data[curIndex][tiebreaker]:
                curBest = data[curIndex][sortBy]
                curBestIndex = curIndex
        
        curIndex += 1
                
    return curBestIndex

#testing
#cur_tests = read_testShare()
cur_tests = read_generated()
#print(cur_tests)
#Tests that can be run on both read_generated() and read_testShare()

simulateTests(cur_tests)
print()

rand = random(cur_tests)
simulateTests(rand[0])
rand = random(cur_tests)
simulateTests(rand[0])
rand = random(cur_tests)
simulateTests(rand[0])
print()

smallest = smallest_sort(cur_tests)
simulateTests(smallest[0])
report_sort(smallest[1], "smallest_sort")
print()

#Tests that can only be run on read_generated()

failRatio = failRatio_sort(cur_tests)
simulateTests(failRatio[0])
report_sort(failRatio[1], "failRatio_sort")
print()

timeFail = timeFailed_sort(cur_tests)
simulateTests(timeFail[0])
report_sort(timeFail[1], "timeFail_sort")
print()

timeRun = timeRun_sort(cur_tests)
simulateTests(timeFail[0])
report_sort(timeRun[1], "timeRun_sort")
print()

combin = combination_sort(cur_tests)
simulateTests(combin[0])
report_sort(combin[1], "combination_sort")