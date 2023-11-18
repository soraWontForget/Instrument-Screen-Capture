# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# This file, 'Instrument.py,' was created by Alexandrae Duran on 11/18/23 at 10:17 AM for the 'Instrument-Screen-Capture' project. 
#
# Description: Instrument class with functions for capturing, retrieving, and deleting screenshots on SCPI enabled
# equipment. Implements core pyvisa library functions for instrument communication. Equipment specific command strings
# will be parsed from the instrument xml file and passed to the CommandInstrument class. Instrument object will access
# appropriate strings from CommandInstrument.
# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

import pyvisa


class InstrumentAbstract:

    IDENTIFY = "*IDN?"
    OPERATION_COMPLETE = "*OPC?"
    BINARY_DATATYPE = "c"

    def __init__(self, visa_address, commands):
        self.VISA_ADDRESS = visa_address
        self.COMMANDS = commands
        self.INSTRUMENT = None
        check = lambda c: False if c == 1 else c

    def connect(self):
        pass

    def disconnect(self):
        pass

    def isConnected(self):
        pass

    def capture(self):
        pass

    def get_image(self):
        pass

    def delete_image(self):
        pass

    def write(self, COMMAND):
        pass

    def read(self, COMMAND):
        pass

    def query(self, COMMAND):
        pass

    def query_binary(self, COMMAND, DATATYPE):
        pass

    def operation_complete(self):
        pass


class Instrument(InstrumentAbstract):

    def __init__(self, visa_address, commands):
        super(Instrument, self).__init__(visa_address, commands)

    def connect(self):
        try:
            rm = pyvisa.ResourceManager()
            self.INSTRUMENT = rm.open_resource(self.VISA_ADDRESS)
            self.INSTRUMENT.timeout = 100000
            self.INSTRUMENT.read_termination = "\n"
        except:
            return 1
        return 0

    def disconnect(self):
        try:
            self.INSTRUMENT.close()
        except:
            return 1
        return 0

    def isConnected(self):
        try:
            print(self.write(self.IDENTIFY))
        except:
            return 1
        return 0

    def capture(self):
        try:
            self.write(self.COMMANDS.capture)
            self._operation_complete()
        except:
            return 1
        return 0

    def get_image(self):
        try:
            image = self.query_binary(self.COMMANDS.get_image, self.BINARY_DATATYPE)
            self._operation_complete()
        except:
            return 1
        return image

    def delete_image(self):
        try:
            self.write(self.COMMANDS.delete_image)
            self._operation_complete()
        except:
            return 1
        return 0

    def write(self, COMMAND):
        try:
            self.INSTRUMENT.write(COMMAND)
            self._operation_complete()
        except:
            return 1
        return 0

    def read(self, COMMAND):
        try:
            read_item = self.INSTRUMENT.read(COMMAND)
            self._operation_complete()
        except:
            return 1
        return read_item

    def query(self, COMMAND):
        try:
            query_item = self.INSTRUMENT.query(COMMAND)
            self._operation_complete()
        except:
            return 1
        return query_item

    def query_binary(self, COMMAND, DATATYPE):
        try:
            query_b_item = self.INSTRUMENT.query_binary_values(COMMAND, datatype=DATATYPE)
            self._operation_complete()
        except:
            return 1
        return query_b_item

    def _operation_complete(self):
        try:
            self.INSTRUMENT.query(self.OPERATION_COMPLETE)
        except:
            return 1
        return 0
