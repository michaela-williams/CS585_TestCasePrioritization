import time
from random import randint, randrange

def readInData(filename):
    if filename == 'testShareData.csv.rev':
        data = read_testShare()
    elif filename == 'TestData.csv':
        data = read_generated()
        
def read_testShare():
    print("Reading in testShareData. This may take some time.")
    tests = list()
    with open('testShareData.csv.rev') as file:
        test_num = 0
        read_data = file.readline()
        while not read_data == '':
            cur_test = list()
            index = 0
            while not read_data == '':
                extracted_data = read_data.partition(',')
                if extracted_data[0] == '':
                    read_data = extracted_data[2]
                    continue
                if index == 0:
                    cur_test.append("test_" + str(test_num))
                elif index == 2 and extracted_data[0] != 'post':
                    break
                elif not (index == 1 or index == 4 or index == 7 or index == 9):
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
                if index == 7:
                    extracted_data = extracted_data[0].partition('\n')
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