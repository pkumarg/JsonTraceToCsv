#!/usr/bin/python3
import json 
import collections
import copy 
import gc 

csvLine = []
outputDict = collections.OrderedDict()

# Opening JSON file and loading the data 
# into the variable data 
with open('Bk.json') as json_file: 
    data = json.load(json_file) 

def JSON2CSV_TRACE(formatedString):
    print(formatedString)
    #pass

#JSON2CSV_TRACE(data)
#JSON2CSV_TRACE(type(data))

def handleList(inputList, outputDict):
    for item in inputList:
        newDict = outputDict
        if (len(inputList) > 1 and bool(outputDict)):
            # Make copy of previous list and pass into next call
            print("Making copy")
            newDict = copy.deepcopy(outputDict)
        if type(item) is dict:
            handlDictType(item, newDict)
        elif type(item) is list:
            print("This should never come")
        elif type(item) is str:
            print("This should never come")
        else:
            print("This should never come")


def handlDictType(inputDict, outputDict):
    recurring = False
    for key in inputDict:
        if type(inputDict[key]) is dict:
            JSON2CSV_TRACE("handlDictType dict type" + "key=" + key)
            recurring = True
            handlDictType(inputDict[key], outputDict)
        elif type(inputDict[key]) is list:
            JSON2CSV_TRACE("handlDictType list type" + "key=" + key)
            recurring = True
            handleList(inputDict[key], outputDict)
        elif type(inputDict[key]) is str:
            JSON2CSV_TRACE("handlDictType appending value")
            JSON2CSV_TRACE(inputDict[key])
            outputDict[key] = "=\"" + inputDict[key] + "\""
            recurring = False
        else:
            JSON2CSV_TRACE("handlDictType appending value")
            JSON2CSV_TRACE(inputDict[key])
            outputDict[key] = "=\"" + str(inputDict[key]) + "\""
            recurring = False

    #print(outputDict)
    if not recurring:
        print(','.join(outputDict.values()))


def toCsv(inputJson):
    handlDictType(inputJson, outputDict)

toCsv(data)

# now we will open a file for writing 
data_file = open('output.csv', 'w') 

data_file.write("Hi\n");

data_file.close() 
