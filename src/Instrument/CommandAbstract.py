#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# This file, 'CommandAbstract.py,' was created by Alexandrae Duran on 2/24/20 for the 'IccsoTesting' project.
# 
# Description: Abstract for CommandInstrument.
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

class CommandAbstract:

    command = []
    commandName = None
    commandType = None
    description = None
    hasParameter = False
    hasUnit = False
    hasOptions = False
    parameter = None
    unit = None
    options = None
    commandID = None
    value = None
    link = None
    address = None
    next = None
    back = None
    hasValDb = None
    valDb = None
    userInput = None

    def toString(self):
        pass

    def load(self, kwargs):
        pass

    def addLink(self, comObj):
        pass

    def removeLink(self):
        pass

    def hasLink(self):
        return True if self.link is not None else False
