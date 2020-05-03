import time
from random import randrange
        
def read_testShare():
    print("Reading in testShareData. This may take some time.")
    tests = list()
    with open('testShareData.csv.rev') as file:
        test_num = 0
        read_data = file.readline()
        while not read_data == '':
            cur_test = list()
            index = 0
            while index < 7:
                extracted_data = read_data.partition(',')
                if extracted_data[0] == '':
                    read_data = extracted_data[2]
                    continue
                if index == 0:
                    cur_test.append("test_" + str(test_num))
                if index == 3:
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
    with open('TestData.csv') as file:  
        read_data = file.readline()
        while not read_data == '':
            cur_test = list()
            for index in range(8):
                extracted_data = read_data.partition(',')
                if index == 1:
                    cur_test.append(int(extracted_data[0]))
                elif index == 2 or index == 6:
                    cur_test.append(float(extracted_data[0]))
                elif index == 3 or index == 4 or index == 5:
                    cur_test.append(int(extracted_data[0]))
                elif index == 7:
                    extracted_data = extracted_data[0].partition('\n')
                    cur_test.append(float(extracted_data[0]))
                else:
                    cur_test.append(extracted_data[0])
                    
                read_data = extracted_data[2]
                
            tests.append(cur_test)
            read_data = file.readline()
            
    return tests

#test order randomly selected
def random(testData):
    ordered = list()
    maxRand = len(testData)
    for cur in range(maxRand):
        curTestNum = randrange(0, len(testData))
        curTest = testData.pop(curTestNum)
        ordered.append((curTest[0], curTest[1]))
        
    elapsed = 0 #value to keep the return format the same as other sort functions
    
    return (ordered, elapsed)

def simulateTests(testQueue):
    duration = 2
    passed = 1
    testsRun = 0
    timeRun = 0
    print(testQueue)
    for curTest in testQueue:
        testsRun += 1
        timeRun += curTest[duration]
        if not curTest[passed]:
            print(curTest)
            break
        
    report(testsRun, timeRun)
        

def smallest_sort(testData):
    print("Sorting")
    startTime = time.clock()
    testQueue = list()
    index = 3
    while len(testData) > 0:
        curSmallest = findMin(testData, index)
        testQueue.append(testData[curSmallest])
        testData.pop(curSmallest)
    endTime = time.clock()
    elapsed = endTime - startTime
    
    return (testQueue, elapsed)

def report(testsRun, timeRun):
    print("Ran ", testsRun, "tests for ", timeRun, " seconds before failing.")

def findMin(data, index):
    curMin = 100000000
    curMinIndex = -1
    curIndex = 0
    for num in data:
        if num[index] < curMin:
            curMin = num[index]
            curMinIndex = curIndex
        curIndex += 1
        
    return curMinIndex



#testing
cur_tests = read_testShare()
#cur_tests = read_generated()
#print (cur_tests)
smallest = smallest_sort(cur_tests)
#print(smallest)
simulated = simulateTests(smallest[0])