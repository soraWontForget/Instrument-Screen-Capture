#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# This file, 'GUI.py,' was created by Alexandrae Duran on 10/04/19 for the 'ScreenshotsForTri' project.
#
# Description: Screenshots for Tri!!!
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

#TODO Remove reference to vikavolt_instrument. Create new class for generic instrument. Parsed SCPI commands from xml file
# will be used in screen capture functions of this class. Move screen capture functions in this class to the generic
# instrument class. Map the signals from those functions to buttons to instrument class in a controller class.

from PyQt5.QtWidgets import QPushButton, QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QComboBox
import Vikavolt_Instrument.AgilentE4446A as agi
import Vikavolt_Instrument.RhodeNSchwarzFSV40 as rns
import pyvisa
import re


class GUI(QWidget):

    #TODO Add field for overriding combobox with manual input for VISA address

    # def __init__(self, parent, instruments):
    def __init__(self, parent):
        super().__init__(parent=parent)
        # Setup screenshot items
        self.button = QPushButton()
        self.button.setText("Capture")
        self.button.clicked.connect(self.capture)
        self.button_2 = QPushButton()
        self.button_2.clicked.connect(self.open_directory_dialog)
        self.button_2.setText("Storage")
        self.button_3 = QPushButton()
        self.button_3.clicked.connect(self.peak_search)
        self.button_3.setText("Peak Search")
        self.text_box = QLineEdit()
        self.text_box.setText("FileName")
        self.text_box_2 = QLineEdit()
        self.directory_name = None

        # Setup instrument items
        self.connectButton = QPushButton()
        self.connectButton.setText("Connect")
        self.connectButton.clicked.connect(self.connect)
        self.comboBox = QComboBox()
        self.comboBox.addItem("E4446A")
        self.comboBox.addItem("FSV40")
        self.comboBox.addItem("FSQ")

        #TODO Below function call is for when instrument parsing is added.

        # self.add_instruments(instruments)

        # Init layout
        self.row_1_layout = QHBoxLayout()
        self.row_2_layout = QHBoxLayout()
        self.row_3_layout = QHBoxLayout()
        self.container_layout = QVBoxLayout()

        # Add widgets to layout
        self.row_1_layout.addWidget(self.button)
        self.row_1_layout.addWidget(self.text_box)
        self.row_2_layout.addWidget(self.button_2)
        self.row_2_layout.addWidget(self.text_box_2)
        self.row_3_layout.addWidget(self.button_3)

        # Setup layout
        self.container_layout.addWidget(self.comboBox)
        self.container_layout.addWidget(self.connectButton)
        self.container_layout.addLayout(self.row_1_layout)
        self.container_layout.addLayout(self.row_2_layout)
        self.container_layout.addLayout(self.row_3_layout)

    def add_instruments(self, instruments):
        for i in instruments:
            self.comboBox.addItem(str(i))

    #TODO Move capture process to generic instrument class.
    def capture(self):
        file_name = self.text_box_2.text() + "/" + self.text_box.text()
        self.instrument.capture_image()
        self.instrument.get_image(file_name)
        self.instrument.delete_image()

    def open_directory_dialog(self):
        self.directory_name = QFileDialog.getExistingDirectory(parent=None, options=QFileDialog.ShowDirsOnly) + "/"
        print(str(self.directory_name))
        self.text_box_2.setText(self.directory_name)

    #TODO Move function to gerneric instrument class
    def peak_search(self):
        self.instrument.peak_search()

    #TODO Get selected instrument in combobox and open that resource. Move actual connection process to generic instrument
    # class
    def connect(self):
        try:
            rm = pyvisa.ResourceManager()

            if re.search("E4446A", self.comboBox.currentText()):
                inst = rm.open_resource("TCPIP::192.168.1.3::inst0::INSTR")
                inst.timeout = 100000
                self.instrument = agi.AgilentE4446A(inst)
            elif re.search("FSQ", self.comboBox.currentText()):
                inst = rm.open_resource("GPIB0::20::INSTR")
                inst.timeout = 100000
                self.instrument = rns.RhodeNSchwarzFSV40(inst)
            else:
                inst = rm.open_resource("TCPIP0::192.168.1.4::inst0::INSTR")
                inst.timeout = 100000
                self.instrument = rns.RhodeNSchwarzFSV40(inst)
        except:
            print("Could not connect to instrument")