# -*- coding: UTF-8 -*-
 
import sys
import argparse
import re
import os
import platform

from subprocess import call
import subprocess
import shlex

from os.path import exists, isfile, join
from os import makedirs, listdir

from build_scenarist.config import defaultScenarioNameEnding, bcolors

def chooseScenarioName(systemName, scriptsNames):
    sizeOfMatch = {}
    for scriptsName in scriptsNames:
        match = re.match("^(" + scriptsName + ")", systemName)
        if bool(match):
            sizeOfMatch[scriptsName]=len(match.group())
    if len(sizeOfMatch) == 0:
        return None
    return max(sizeOfMatch, key=sizeOfMatch.get)

def getScriptsVariants(scriptsDir):
    onlyfiles = [f for f in listdir(scriptsDir) if isfile(join(scriptsDir, f))]
    scriptsNames = []
    for fileName in onlyfiles:
        match = re.match("^(.*" + defaultScenarioNameEnding + ")$", fileName)
        if bool(match):
            scriptsNames.append(fileName[:-1 * len(defaultScenarioNameEnding)])
    return scriptsNames

def splitTargetCallToNameAndParams(targetCall):
    targetNamePart = re.findall("^([a-zA-Z][a-zA-Z0-9\_]*):*.*$", targetCall)
    targetName = ""
    if len(targetNamePart) == 1:
        targetName = targetNamePart[0]

    assignmentsPart = re.findall("^[a-zA-Z][a-zA-Z0-9\_]*:*(.+)$", targetCall)

    # print(assignmentsPart)

    if len(assignmentsPart) == 1:
        stringAssignments  = []
        numberAssignments = []
        arraysAssignments  = []

        numberAssignments = re.findall(r"([a-zA-Z][^,^=]*\=[\-\+]?[0-9\.]+)", assignmentsPart[0])
        stringAssignments  = re.findall(r"((?![a-zA-Z][^,^=]*\=[\d\+\-]+)[a-zA-Z][^\,^\=]*\=[^\,^\[^\]]+)", assignmentsPart[0])
        arraysAssignments  = re.findall(r"([a-zA-Z][^,^=]*\=\[.+\])", assignmentsPart[0])

    # print("stringAssignments ", stringAssignments)
    # print("numberAssignments ", numberAssignments)
    # print("arraysAssignments ", arraysAssignments)

    processedAssignments = []
    for assignment in numberAssignments:
        processedAssignments.append(assignment)

    for assignment in stringAssignments:
        # print(assignment)
        m = re.findall('^([a-zA-Z][a-zA-Z0-9\_]*=)([^\"^]+)$', assignment)
        if m:
            assignment = re.sub(r"^([a-zA-Z][a-zA-Z0-9\_]*=)([^\"^]+)$", r'\1"\2"', assignment)
            # print(assignment)
        processedAssignments.append(assignment)

    for assignment in arraysAssignments:
        stringRegexp = "[\,\]\[]((?![\d\+\-\ ]+)[^\[^\]^\"^\'^\,]+)[\,\[\]]"
        m = re.search(stringRegexp, assignment)
        while m:
            assignment = assignment[:m.span()[0]+1] + "\"" + m.groups()[0] + "\"" + assignment[m.span()[1]-1:]
            m = re.search(stringRegexp, assignment)
        processedAssignments.append(assignment)
    
    return (targetName, [assignment for assignment in processedAssignments])
