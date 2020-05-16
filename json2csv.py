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
columnIdx = 0
addColumn = True
dumpColumn = False

outputDict = collections.OrderedDict()
outputColumns = []

def handleError(currentItem, error, exit):
    print("***Error*** Line=" + str(lineCounter) +
            "\nDesc=" + error + "\nCurrentItem=" + str(currentItem),
            file=sys.stderr)
    if exit:
        exit()

def printOutput(csvRow):
    global outputFile_fp
    global separator
    print(separator.join(csvRow), file=outputFile_fp)

def printCsvHeader(outputFile):
    global outputColumns
    global valueStartFormat
    global valueEndFormat
    global dumpColumn
    columnList = []

    colIdx = 0

    for colDict in outputColumns:
        columnList.append(valueStartFormat + list(colDict.keys())[0] + valueEndFormat)

    if outputFile:
        with open(outputFile, 'r+') as outFile_fp:
            content = outFile_fp.read()
            outFile_fp.seek(0, 0)
            outFile_fp.write(separator.join(columnList).rstrip('\r\n') + '\n' + content)
    elif dumpColumn:
        print(separator.join(columnList), file=sys.stderr)

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
            handleError(item, "Didn't expect list,int,str type in handleListType()", True)

def addToDict(key, value, outputDict):
    global addColumn
    global columnIdx

    # Add this column (Display all column case)
    #print("addToDict(): ColIdx=" + str(columnIdx) + " Len=" + str(len(outputColumns)))
    if addColumn:
        outputColumns.append({key:0})
    # Didn't match
    elif not (list(outputColumns[columnIdx].keys())[0] == key):
        return

    columnIdx += 1

    appendIndex = 1
    if key in outputDict.keys():
        while True:
            key = key + "_" + str(appendIndex)
            if not key in outputDict.keys():
                break
            appendIndex += 1
    outputDict[key] = valueStartFormat + value + valueEndFormat


def handleDictType(inputDict, outputDict):
    global lastItemIsList
    global columnIdx
    global addColumn
    global outputColumns

    #print("handleDictType(): ColIdx=" + str(columnIdx) + " Len=" + str(len(outputColumns)))
    for key in inputDict:
        if not addColumn and columnIdx >= len(outputColumns):
            return

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
    global columnIdx

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
            columnIdx = 0
        else:
            break

    #Let's close output file so that it gets flushed, and wish that
    # we have something useful in this :P
    if args.outputFile:
        outputFile_fp.close()
        printCsvHeader(args.outputFile)

    if args.dump_columns:
        printCsvHeader(None)

    #And be a gentleman, not sure if python does it automatically
    jsonDataFile_fp.close()

def updateCsvColumns(args):
    global outputColumns
    global addColumn

    # we have to use user provided column only
    addColumn = False

    columnPattern = '(?P<column>.*):(?P<depth>.*)$'
    columns = args.csvColumns.split(',')

    for col in columns:
        colDepth = col.split(':')
        if len(colDepth) == 2:
            try:
                outputColumns.append({colDepth[0]:int(colDepth[1])})
            except ValueError:
                print("Depth in column=" + col +" is not a valid number")
        else:
            outputColumns.append({colDepth[0]:0})

def updateGlobals(args):
    global separator
    global valueStartFormat
    global valueEndFormat
    global dumpColumn

    # Don't want to get it ugly so accepting only 1 char separator
    if args.separator:
        if len(args.separator) == 1:
            separator = args.separator
        else:
            print("Expected separator length is 1, using , as separator")

    if args.plain_csv:
        valueStartFormat = ''
        valueEndFormat = ''

    if args.csvColumns:
        updateCsvColumns(args)

    if args.dump_columns:
        dumpColumn = True

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
    parser.add_argument(
            '--dump-columns',
            action = 'store_true',
            help = 'Dumps columns row in std.error before exit',
            )

    args = parser.parse_args()

    updateGlobals(args)

    if not args.inputJsonFile:
        parser.print_help()
    else:
        startParsing(args)

