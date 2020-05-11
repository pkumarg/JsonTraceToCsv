#!/usr/bin/python3
import json 
import collections
import copy 
import sys 
import argparse

lineCounter = 0
outputDict = collections.OrderedDict()

def JSON2CSV_TRACE(formatedString):
    #print(formatedString)
    pass

def unknownError(lastItem):
    print("Unkown error occurred at line=" + str(lineCounter) + " LastItem:\n" + str(lastItem), file=sys.stderr)
    exit()

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
        if type(item) is list:
        else:
            # Not expected a list, str, number type item
            unknownError(item)

def addToDict(key, value, dict):
    appendIndex = 1
    if key in dict.keys():
        while True:
            key = key + "_" + str(appendIndex)
            if not key in dict.keys():
                break
            appendIndex += 1
    dict[key] = "=\"" + value + "\""


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

def parsingStart(jsonDataFile):
    global lineCounter
    # Open JSON data file
    jsonDataFile_fp = open(jsonDataFile, "r")

    while True:
        jsonObj = jsonDataFile_fp.readline()
        lineCounter += 1
        if jsonObj:
            toCsv(json.loads(jsonObj))
            outputDict.clear()
        else:
            break

# Summon the magic
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="JSON Object Parser",
            epilog="",
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
            '-j',
            '--jsonDataFile',
            metavar = '<JSON data file>',
            help = 'JSON data file input is mandotory !')

    args = parser.parse_args()

    if not args.jsonDataFile:
        parser.print_help()
    else:
        parsingStart(args.jsonDataFile)

