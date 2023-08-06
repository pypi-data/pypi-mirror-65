# -*- coding: UTF-8 -*-
 
import sys
import re
import os
import Queue
import subprocess

from utility import splitTargetCallToNameAndParams
from info    import Info
from config  import bcolors, defaultScenarioNameEnding, defaultScenarioDir

def countLeadingSymbols(line, symbol):
    counter = 0
    for i in line:
        if i == symbol:
            counter+=1
        else:
            break
    return counter

def calculateShiftings(text, symbol):
    shiftings = []
    for i in text.split('\n'):
        if len(i) != 0:
            shiftings.append(countLeadingSymbols(i, symbol))

    return shiftings

def findMinimumShiftingLength(shiftings):
    minimumShiftingLength = sys.maxint
    for i in shiftings:
        if i < minimumShiftingLength:
            minimumShiftingLength = i
    if minimumShiftingLength != sys.maxint:
        return minimumShiftingLength
    else:
        return 0

def removeShiftings(text):
    shiftingsByTabs   = calculateShiftings(text, '\t')
    shiftingsBySpaces = calculateShiftings(text, ' ')
    minimumShiftingLengthByTabs   = findMinimumShiftingLength(shiftingsByTabs)
    minimumShiftingLengthBySpaces = findMinimumShiftingLength(shiftingsBySpaces)

    if minimumShiftingLengthByTabs > 0:
        minimumShiftingLength = minimumShiftingLengthByTabs
    else:
        minimumShiftingLength = minimumShiftingLengthBySpaces

    if minimumShiftingLength > 0:
        cleanText = ""
        for i in text.split('\n'):
            cleanLine = i
            if len(i) != 0:
                cleanLine = i[minimumShiftingLength:]
            cleanText += cleanLine + '\n'
        return cleanText
    else:
        return text

def getTargets(pathToScenario):
    with open(pathToScenario) as f:
        content = f.readlines()

    targetPositions = []
    for lineIndex, text in enumerate(content):
        if bool(re.match("^(\[+.*\]+)$", text)):
            targetPositions.append(lineIndex)

    targets = {}
    fro=0
    to=0
    targetName="None"
    for i, val in enumerate(targetPositions):
        fro = targetPositions[i]+1
        if i+1 < len(targetPositions):
            to = targetPositions[i+1]
        else:
            to = len(content)
        targetName = content[targetPositions[i]][1:-2]
        targetCode = '\n'.join(content[fro:to])
        targets[targetName] = targetCode
    return targets

def isTargetExist(target, pathToScenario):
    targetsCode = getTargets(pathToScenario)
    return target in targetsCode

def scenarioPath(scenarioName, scenarioDir=defaultScenarioDir, defaultScenarioNameEnding=defaultScenarioNameEnding):
    return os.path.join(scenarioDir, scenarioName + defaultScenarioNameEnding)

def compatibleScenariosPathes():
    info = Info()
    pathes = []
    path = scenarioPath(info.osName()+"_"+info.distName()+"_"+info.distVersion())
    if os.path.isfile(path):
        pathes.append(path)

    path = scenarioPath(info.osName()+"_"+info.distName())
    if os.path.isfile(path):
        pathes.append(path)

    path = scenarioPath(info.osName())
    if os.path.isfile(path):
        pathes.append(path)

    return pathes

def runTargets(targets, scenarioDir=defaultScenarioDir):
    targetsQueue = Queue.Queue()
    for targetCall in targets:
        targetAndParams = splitTargetCallToNameAndParams(targetCall)
        targetsQueue.put(targetAndParams)

    notFoundTargets = []

    while not targetsQueue.empty():
        target, params = targetsQueue.get()
        targetFound = False
        for scenarioPath in compatibleScenariosPathes():
            if isTargetExist(target, scenarioPath):
                if len(params)>0:
                    print (bcolors.OKGREEN + "Target \"" + target + ":" + ",".join(params)+"\"" + bcolors.ENDC)
                else:
                    print (bcolors.OKGREEN + "Target \"" + target +"\"" + bcolors.ENDC)

                targetsCode = getTargets(scenarioPath)
                sys.stdout.flush()
                code = "from scenario_help_utils import runTarget, runShell, cd\n"
                code += "from os.path import exists\n"
                code += "from os import makedirs\n"
                for paramCode in params:
                    code += "%s\n" % (paramCode)
                code += removeShiftings(targetsCode[target])
                exec(code)
                targetFound = True
                break
        if targetFound == False:
            print (bcolors.FAIL + "\nError: Target \"%s\" not found" % (target) + bcolors.ENDC)
            sys.stdout.flush()
            break