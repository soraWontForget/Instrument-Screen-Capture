#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# This file, 'InstrumentParsing.py,' was created by Alexandrae Duran on 2/25/20 for the 'IccsoTesting' project.
# 
# Description: Parses the instrument XML file into an instrument object.
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

#TODO Update references to packages

import xml.etree.ElementTree as et
import re
from vikavolt.Application.Command.CommandInstrument import CommandInstrument as ci

class InstrumentParsing:
    def __init__(self):
        super().__init__()
        self.parsed = None
        self.root = None
        self.COMMAND_NAME = "Command Name"
        self.COMMAND_STR = "Command"
        self.COMMAND_TYPE = "Type"
        self.COMMAND_DESC = "Description"
        self.HAS_PARAM = "hasParameter"
        self.HAS_UNIT = "hasUnit"
        self.HAS_OPTIONS = "hasOptions"

    def parse_xml(self, source):
        self.parsed = et.parse(source=source)
        self.root = self.parsed.getroot()

    def get_inst_info(self):
        cons = {}
        serial = self.root.find("serial").text
        model = self.root.find("model").text
        manufacturer = self.root.find("manufacturer").text
        instType = self.root.find("instType")
        calDate = self.root.find("lastcal")
        calDue = self.root.find("caldue")
        for con in self.root.findall("connections/contype"):
            if con.get('conSup') == 'true':
                if con.get('default') == 'true':
                    defaultCon = con.get('name')
                    defaultAddress = con.find('address').text.replace('\n', '').replace(' ', '')
                # try:
                cons[con.get('name')] = con.find('address').text.replace('\n', '').replace(' ', '')


        return {'serial': serial, 'model': model, 'manufacturer': manufacturer, 'instType': instType, 'caldue': calDue,
                'caldate': calDate, 'connections': cons, 'defaultAddress': defaultAddress, 'defaultCon': defaultCon}

    def get_subsystems(self):
        speccom = self.root.findall("./commands/subsystem")
        for a in speccom:
            yield a.get('name')

    def getSubsystemCommands(self, subsystem, address):
        subsys = self.root.findall(".//*[@name='{}']/command".format(subsystem))
        for i in subsys:
            comname = i.get('name')
            comstr = i.get('comstr')
            comtype = i.get('comtype')
            comdesc = i.find('description').text.replace("\n                        ", "").replace("\n                    ", "")
            print(i.get('comstr'), i.get('name'), i.get('comtype'))
            print(i.find('description').text.replace("\n                        ", "").replace("\n                    ", ""))
            if i.get('hasValDb') == "true":
                hasValDb = True
                valDb = i.get('valDb')
            else:
                hasValDb = False
                valDb = None
            if re.search('{}{}', i.get('comstr')):
                print(i.get('comstr').format('X', i.get('unit')))
                unit = i.get('unit')
                hasUnit = True
                hasParameter = True
                parameter = 'X'
                hasOptions = False
                options = None
            elif re.search('{}', i.get('comstr')):
                print("Options:")
                options = []
                if i.findall('option'):
                    for option in i.findall('option'):
                        print(option.get('default'))
                        if option.get('default') == 'true':
                            parameter = option.text
                        # print(option.text)
                    # _ = i.find('option').text
                    # print(_.find('true'))
                        print(i.get('comstr').format(option.text))
                        options.append(option.text)
                        hasOptions = True
                        hasUnit = None
                        unit = None
                    hasParameter = True
                else:
                    parameter = None
                    hasParameter = False
                    hasUnit = False
                    unit = None
                    hasOptions = None
                    options = None
            elif i.get('parameter') == 'true':
                hasParameter = True
                parameter = None
            else:
                hasParameter = False
                parameter = None
                options = None
                unit = None
                hasUnit = False
                hasOptions = False

            comObj = ci({"command": comstr,
                         "name": comname,
                         "description": comdesc,
                         "type": comtype,
                         "hasParameter": hasParameter,
                         "parameter": parameter,
                         "hasUnit": hasUnit,
                         "unit": unit,
                         "hasOptions": hasOptions,
                         "options": options,
                         "hasValDb": hasValDb,
                         "valDb": valDb,
                         "address": address}
                         )
            print(comObj.toString())
            yield comObj