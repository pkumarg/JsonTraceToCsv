#!/afs/sero.gic.ericsson.se/app/vbuild/RHEL7-x86_64/python/3.8.0/bin/python3
import json 
import collections
import copy 
import sys 
import argparse

lineCounter = 0

printList = 0

outputDict = collections.OrderedDict()

def JSON2CSV_TRACE(formatedString):
    #print(formatedString)
    pass

def unknownError(lastItem, error):
    print("Unkown error occurred at line=" + str(lineCounter) +
            "\nErrorDesc: " + error + "\nLastItem: " + str(lastItem),
            file=sys.stderr)
    exit()

#JSON2CSV_TRACE(data)
#JSON2CSV_TRACE(type(data))

def handleList(inputList, outputDict, printListCount):
    global printList

    for item in inputList:
        if(printListCount > 1):
            printList = 1
        newDict = outputDict
        if (len(inputList) > 1 and bool(outputDict)):
            # Make copy of previous list and pass into next call
            JSON2CSV_TRACE("Making copy")
            newDict = copy.deepcopy(outputDict)
        if type(item) is dict:
            handlDictType(item, newDict, printListCount)
        else:
            # Not expected a list, str, number type item
            unknownError(item, "Didn't expect list,int,srt type in handleList()")

    printListCount /= len(inputList)

def addToDict(key, value, dict):
    appendIndex = 1
    if key in dict.keys():
        while True:
            key = key + "_" + str(appendIndex)
            if not key in dict.keys():
                break
            appendIndex += 1
    dict[key] = "=\"" + value + "\""


def handlDictType(inputDict, outputDict, printListCount):
    JSON2CSV_TRACE(outputDict)
    global printList
    for key in inputDict:
        if type(inputDict[key]) is dict:
            JSON2CSV_TRACE("handlDictType dict type" + " key=" + key)
            handlDictType(inputDict[key], outputDict, printListCount)
        elif type(inputDict[key]) is list:
            if ((type(inputDict[key][0]) is int) or (type(inputDict[key][0]) is str)):
                JSON2CSV_TRACE("handlDictType list in list type")
                valueArray = ' '.join([str(strOrInt) for strOrInt in inputDict[key]])
                addToDict(key, valueArray, outputDict)
            else:
                JSON2CSV_TRACE("handlDictType list type" + " key=" + key + " elements=" + str(len(inputDict[key])))
                handleList(inputDict[key], outputDict, printListCount*len(inputDict[key]))
        elif type(inputDict[key]) is str:
            JSON2CSV_TRACE("handlDictType appending value")
            JSON2CSV_TRACE(inputDict[key])
            addToDict(key, inputDict[key], outputDict)
        else:
            JSON2CSV_TRACE("handlDictType appending value")
            JSON2CSV_TRACE(inputDict[key])
            addToDict(key, str(inputDict[key]), outputDict)

    JSON2CSV_TRACE(outputDict)
    if printList:
        print(','.join(outputDict.values()))
        printList = 0


def toCsv(inputJson):
    handlDictType(inputJson, outputDict, 1)
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

