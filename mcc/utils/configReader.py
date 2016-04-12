#-*-coding:utf8-*-
from configparser import ConfigParser
import os, sys

class ConfigReader(object):
    def __init__(self, configPath):
        configFile = os.path.join(sys.path[0],configPath)
        self.cReader = ConfigParser()
        self.cReader.read(configFile)

    def readConfig(self, section, item):
        return self.cReader[section][item]

    def getDict(self, section):
        commandDict = {}
        items = self.cReader.items(section)
        for key, value in items:
            commandDict[key] = value
        return commandDict
