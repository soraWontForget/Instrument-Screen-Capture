#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# This file, 'CommandInstrument.py,' was created by Alexandrae Duran on 2/24/20 for the 'IccsoTesting' project.
#
# Description: Models a parsed SCPI command of an instrument. Passes back the SCPI command as a string for the
# instrument class to execute.
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

#TODO Update references to packages.

from vikavolt.Application.Command.CommandAbstract import CommandAbstract as ca
import re
import os
import binascii


class CommandInstrument(ca):

    def __init__(self, kwargs):
        super().__init__()
        self.commandID = binascii.b2a_hex(os.urandom(15))
        self.load(kwargs)

    def toString(self):
        command = self.command
        if not self.link:
            if re.search('{}{}', command):
                command = command.format(self.parameter, self.unit)
            elif re.search('{}, {}', command):
                command = command.format(self.parameter, "1")
            elif re.search('{}', command):
                command = command.format(self.parameter)
            return command #+ ";"
            #TODO The semicolon is to be used for inline command statements. This is done to concatenate two or more
            # separate commands into one single line command.

    def setParameter(self, parameter):
        self.parameter = parameter

    def load(self, kwargs):
        if kwargs:
            print(kwargs)
            self.command = kwargs['command']
            self.commandName = kwargs['name']
            self.description = kwargs['description']
            self.commandType = kwargs['type']
            self.address = kwargs['address']
            # self.userInput = kwargs['userInput']
            if kwargs['hasParameter']:
                self.hasParameter = True
                self.parameter = kwargs['parameter']
            if kwargs['hasUnit']:
                self.unit = kwargs['unit']
                self.hasUnit = True
            if kwargs['hasOptions']:
                self.hasOptions = True
                if self.options is None:
                    self.options = []
                for option in kwargs['options']:
                    self.options.append(option)
                print(self.options)
            if kwargs['hasValDb']:
                self.hasValDb = True
                self.valDb = kwargs['valDb']
        else:
            print("None found in Command Object while loading new Command")

    # Vestigial. Links aren't used. There's never a call to these functions.
    def addLink(self, comObj):
        self.link = comObj

    def removeLink(self):
        self.link = None




