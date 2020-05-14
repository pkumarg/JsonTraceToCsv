#!/usr/bin/python3
import json 
import collections
import copy 
import sys 
import argparse

lineCounter = 0
lastItemIsList = 0
outputFile_fp = sys.stdout
separator = ','
valueStartFormat = '="'
valueEndFormat = '"'

outputDict = collections.OrderedDict()
outputColumns = collections.OrderedDict()

def handleError(currentItem, error, exit):
    print("***Error*** Line=" + str(lineCounter) +
            "\nDesc=" + error + "\nCurrentItem=" + str(currentItem),
            file=sys.stderr)
    if exit:
        exit()

def printOutput(csvColumns):
    global outputFile_fp
    global separator
    print(separator.join(csvColumns), file=outputFile_fp)

def handleListType(inputList, outputDict):
    for item in inputList:
        newDict = outputDict
        if (len(inputList) > 1 and bool(outputDict)):
            # Make copy of previous list and pass into next call
            newDict = copy.deepcopy(outputDict)
        if type(item) is dict:
            handleDictType(item, newDict)
            # Let's print after handling list element
            printOutput(newDict.values())
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
    dict[key] = valueStartFormat + value + valueEndFormat


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
        printOutput(outputDict.values())

def startParsing(args):
    global lineCounter
    global outputFile_fp
    # Open JSON data file
    jsonDataFile_fp = open(args.inputJsonFile, "r")

    # if we have to write output file
    if args.outputFile:
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

def updateOutputColumns(args):
    columns = args.csvColumns.split(',')

    for col in columns:
        outputColumns[col]= '0'

def updateGlobals(args):
    global separator
    global valueStartFormat
    global valueEndFormat

    # Don't want to get it ugly so accepting only 1 char separator
    if args.separator and (len(args.separator) == 1):
        separator = args.separator
    else:
        print("Expected separator length is 1, using , as separator")

    if args.plain_csv:
        valueStartFormat = ''
        valueEndFormat = ''

    updateOutputColumns(args)

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
            '-o',
            '--outputFile',
            metavar = '<outputFile.csv>',
            help = ''
            )
    parser.add_argument(
            '-c',
            '--csvColumns',
            metavar = '<"col1,col2,col3 ...">',
            help = 'Column name should exactly match, in JSON objects. \
                    Columns printed in output CSV file only make sense \
                    if input JSON file have all lines of same JSON object type'
            )
    parser.add_argument(
            '--separator',
            metavar = '<Custom CSV separator, default is comma>',
            help = ''
            )
    parser.add_argument(
            '--plain-csv',
            action = 'store_true',
            help = 'Makes standard CSV, useful if not using Excel',
            )

    args = parser.parse_args()

    updateGlobals(args)

    if not args.inputJsonFile:
        parser.print_help()
    else:
        startParsing(args)

