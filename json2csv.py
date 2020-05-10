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
    #print(formatedString)
    pass

#JSON2CSV_TRACE(data)
#JSON2CSV_TRACE(type(data))

def handleList(inputList, outputDict):
    for item in inputList:
        newDict = outputDict
        if (len(inputList) > 1 and bool(outputDict)):
            # Make copy of previous list and pass into next call
            JSON2CSV_TRACE("Making copy")
            newDict = copy.deepcopy(outputDict)
        if type(item) is dict:
            handlDictType(item, newDict)
        elif type(item) is list:
            print("This should never come")
        elif type(item) is str:
            print("This should never come")
        else:
            print("This should never come")

def addToDict(key, value, dict):
    appendIndex = 1
    if key in dict.keys():
        while True:
            key = key + "_" + str(appendIndex)
            if not key in dict.keys():
                break
            appendIndex += 1
    dict[key] = value


def handlDictType(inputDict, outputDict):
    JSON2CSV_TRACE(outputDict)
    recurring = False
    for key in inputDict:
        if type(inputDict[key]) is dict:
            JSON2CSV_TRACE("handlDictType dict type" + " key=" + key)
            recurring = True
            handlDictType(inputDict[key], outputDict)
        elif type(inputDict[key]) is list:
            JSON2CSV_TRACE("handlDictType list type" + " key=" + key + " elements=" + str(len(inputDict[key])))
            recurring = True
            handleList(inputDict[key], outputDict)
        elif type(inputDict[key]) is str:
            JSON2CSV_TRACE("handlDictType appending value")
            JSON2CSV_TRACE(inputDict[key])
            recurring = False
            addToDict(key, inputDict[key], outputDict)
        else:
            JSON2CSV_TRACE("handlDictType appending value")
            JSON2CSV_TRACE(inputDict[key])
            recurring = False
            addToDict(key, str(inputDict[key]), outputDict)

    JSON2CSV_TRACE(outputDict)
    if not recurring:
        print(','.join(outputDict.values()))


def toCsv(inputJson):
    handlDictType(inputJson, outputDict)

# Summon the magic
toCsv(data)
