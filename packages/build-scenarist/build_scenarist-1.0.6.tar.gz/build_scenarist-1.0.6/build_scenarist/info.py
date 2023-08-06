# -*- coding: UTF-8 -*-
 
import os
import platform
import build_scenarist.utility
from build_scenarist.config import defaultScenarioNameEnding

class Info:
    def osName(self):
        return platform.system().replace('"', '')
    
    def distName(self):
        distName = "None_None"
        if self.osName() == "Linux":
            distName = platform.dist()[0].replace('"', '')
        elif self.osName() == "Windows":
            distName = platform.win32_ver()[0].replace('"', '')
        elif self.osName() == "Darwin":
            distName = "MacOS"
        return distName

    def distVersion(self):
        distVersion = "None"
        if self.osName() == "Linux":
            distVersion = platform.dist()[1].replace('"', '')
        elif self.osName() == "Windows":
            distVersion = platform.win32_ver()[2].replace('"', '')
        elif self.osName() == "Darwin":
            distVersion = platform.mac_ver()[0]

        return distVersion

    def fullPlatformName(self):
        return self.osName() + '_' + self.distName() + '_' + self.distVersion()

    def defaultScriptName(self):
        return self.fullPlatformName() + defaultScenarioNameEnding

    def scriptName(self, osName, distName, distVersion):
        return osName + '_' + distName + ' ' + distVersion + defaultScenarioNameEnding

    def about_platform(self):
        return """            OS name:    {0}
          Dist name:    {1}
          Dist version: {2}
Default script name: {3}""".format(self.osName(), self.distName(), self.distVersion(), self.defaultScriptName())
