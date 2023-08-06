# -*- coding: UTF-8 -*-
 
import sys
import os

from subprocess import call
import subprocess
import shlex

from build_scenarist.utility import splitTargetCallToNameAndParams
from build_scenarist.config import bcolors, global_vars, defaultScenarioNameEnding, defaultScenarioDir
from build_scenarist.runner import runTargets

def runTarget(targetCall):
    runTargets([targetCall])

def runShell(cmd, fallAtFail=True):
    sys.stdout.write("\n" + bcolors.HEADER + "shell: " + bcolors.ENDC + "\n")
    sys.stdout.write(bcolors.BOLD + cmd + bcolors.ENDC + "\n")
    sys.stdout.flush()
    retCode = subprocess.call(shlex.split(cmd))
    if retCode != 0 and fallAtFail:
        sys.stdout.write("\nShell code failed with code: " + str(retCode) + "\n")
        sys.stdout.flush()
        sys.exit(retCode)
    sys.stdout.write("\n")
    sys.stdout.flush()
    return retCode

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        try:
            os.chdir(self.newPath)
        except OSError:
            raise Exception(bcolors.FAIL + "Path: {0}. No such file or directory!".format(self.newPath) + bcolors.ENDC)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
