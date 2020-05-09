#!/usr/bin/python3
import json 
import collections

csvLine = []
outputDict = collections.OrderedDict()

# Opening JSON file and loading the data 
# into the variable data 
with open('Bk.json') as json_file: 
    data = json.load(json_file) 

def JSON2CSV_TRACE(formatedString):
    #print(formatedString)
    pass

#JSON2CSV_TRACE(data)
#JSON2CSV_TRACE(type(data))

def handleList(inputList):
    for item in inputList:
        if type(item) is dict:
            JSON2CSV_TRACE("handleList dict type")
            handlDictType(item)
        elif type(item) is list:
            JSON2CSV_TRACE("handleList list type")
            print("This should never come")
            handleList(item)
        elif type(item) is str:
            JSON2CSV_TRACE("handleList printing value")
            JSON2CSV_TRACE(item)
            print("This should never come")
        else:
            JSON2CSV_TRACE("handleList printing value")
            print("This should never come")
            JSON2CSV_TRACE(item)


def handlDictType(inputDict):
    for key in inputDict:
        if type(inputDict[key]) is dict:
            JSON2CSV_TRACE("handlDictType dict type")
            handlDictType(inputDict[key])
        elif type(inputDict[key]) is list:
            JSON2CSV_TRACE("handlDictType list type")
            handleList(inputDict[key])
        elif type(inputDict[key]) is str:
            JSON2CSV_TRACE("handlDictType printing value")
            JSON2CSV_TRACE(inputDict[key])
            outputDict[key] = "=\"" + inputDict[key] + "\""
        else:
            JSON2CSV_TRACE("handlDictType printing value")
            JSON2CSV_TRACE(inputDict[key])
            outputDict[key] = "=\"" + str(inputDict[key]) + "\""


def toCsv(inputJson):
    handlDictType(inputJson)
    print(outputDict)
    print("CSV Line: " + ','.join(outputDict.values()))

toCsv(data)

# now we will open a file for writing 
data_file = open('output.csv', 'w') 

data_file.write("Hi\n");

data_file.close() 
