#!/usr/bin/python3
import json 
import collections
import copy 
import sys 
import argparse

lineCounter = 0
lastItemIsList = 0

outputDict = collections.OrderedDict()

def unknownError(lastItem, error):
    print("Unkown error occurred at line=" + str(lineCounter) +
            "\nErrorDesc: " + error + "\nLastItem: " + str(lastItem),
            file=sys.stderr)
    exit()

def handleListType(inputList, outputDict):
    for item in inputList:
        newDict = outputDict
        if (len(inputList) > 1 and bool(outputDict)):
            # Make copy of previous list and pass into next call
            newDict = copy.deepcopy(outputDict)
        if type(item) is dict:
            handleDictType(item, newDict)
            # Let's print after handling list element
            print(','.join(newDict.values()))
        else:
            # Not expected a list, str, number type item
            unknownError(item, "Didn't expect list,int,srt type in handleListType()")

def addToDict(key, value, dict):
    appendIndex = 1
    if key in dict.keys():
        while True:
            key = key + "_" + str(appendIndex)
            if not key in dict.keys():
                break
            appendIndex += 1
    dict[key] = "=\"" + value + "\""


def handleDictType(inputDict, outputDict):
    global lastItemIsList
    for key in inputDict:
        if type(inputDict[key]) is dict:
            handleDictType(inputDict[key], outputDict)
            lastItemIsList = 0
        elif type(inputDict[key]) is list:
            if ((type(inputDict[key][0]) is int) or (type(inputDict[key][0]) is str)):
                valueArray = ' '.join([str(strOrInt) for strOrInt in inputDict[key]])
                addToDict(key, valueArray, outputDict)
            else:
                handleListType(inputDict[key], outputDict)
                lastItemIsList = 1
        elif type(inputDict[key]) is str:
            addToDict(key, inputDict[key], outputDict)
        else:
            addToDict(key, str(inputDict[key]), outputDict)

def toCsv(inputJson):
    global lastItemIsList
    handleDictType(inputJson, outputDict)
    if not lastItemIsList:
        print(','.join(outputDict.values()))

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

