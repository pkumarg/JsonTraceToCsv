#!/usr/bin/python3
import json 
import collections
import copy 
import sys 
import argparse

lineCounter = 0
lastItemIsList = 0
outputFile_fp = sys.stdout

outputDict = collections.OrderedDict()

def handleError(currentItem, error, exit):
    print("***Error*** Line=" + str(lineCounter) +
            "\nDesc=" + error + "\nCurrentItem=" + str(currentItem),
            file=sys.stderr)
    if exit:
        exit()

def printOutput(outTrace):
    global outputFile_fp
    print(outTrace, file=outputFile_fp)

def handleListType(inputList, outputDict):
    for item in inputList:
        newDict = outputDict
        if (len(inputList) > 1 and bool(outputDict)):
            # Make copy of previous list and pass into next call
            newDict = copy.deepcopy(outputDict)
        if type(item) is dict:
            handleDictType(item, newDict)
            # Let's print after handling list element
            printOutput(','.join(newDict.values()))
        else:
            # Not expected a list, str, number type item
            handleError(item, "Didn't expect list,int,srt type in handleListType()", True)

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
        printOutput(','.join(outputDict.values()))

def startParsing(args):
    global lineCounter
    global outputFile_fp
    # Open JSON data file
    jsonDataFile_fp = open(args.inputJsonFile, "r")

    # if we have to write output file
    if args.outputFile:
        print(args.outputFile)
        outputFile_fp = open(args.outputFile, "w")

    while True:
        jsonObjLine = jsonDataFile_fp.readline()
        lineCounter += 1
        if jsonObjLine:
            try:
                toCsv(json.loads(jsonObjLine))
            except json.JSONDecodeError:
                handleError(jsonObjLine, "json.JSONDecodeError", False)
            outputDict.clear()
        else:
            break

    #Let's close output file so that it gets flushed, and wish that
    # we have something useful in this :P
    if args.outputFile:
        outputFile_fp.close()

    #And be a gentleman, not sure if python does it automatically
    jsonDataFile_fp.close()

# Summon the magic
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="JSON Object Parser",
            epilog="",
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
            'inputJsonFile',
            metavar='<inputFile.json>',
            help=''
            )
    parser.add_argument(
            '-f',
            '--outputFile',
            metavar = '<outputFile.csv>',
            help = '')
    parser.add_argument(
            '-c',
            '--csvColumns',
            metavar = '<"col1,col2,col3 ...">',
            help = 'Column name should exactly match, in JSON objects. Columns printed in output CSV file only make sense if input JSON file have all lines of same JSON object type')

    args = parser.parse_args()

    if not args.inputJsonFile:
        parser.print_help()
    else:
        startParsing(args)

