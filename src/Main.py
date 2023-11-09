#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# This file, 'Main.py,' was created by Alexandrae Duran on 10/04/19 for the 'ScreenshotsForTri' project.
#
# Description: Main loop
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#TODO Add init for parsing instruments_xml in xml folder.
#TODO GUI class needs access to parsed instrument models VISA addresses.
#TODO Center the window.
#TODO Add generic instrument class with fields for parsed commands

from PyQt5.QtWidgets import QApplication, QGroupBox, QVBoxLayout, QMainWindow
import sys
from src.GUI import GUI


class Main(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)
        self.title = "EZPZ Screenshots for Tri"
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 50
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.gui = GUI.GUI(self)
        self.group_box = QGroupBox()
        self.group_box.layout = QVBoxLayout()
        self.group_box.layout.addLayout(self.gui.container_layout)
        self.group_box.setLayout(self.group_box.layout)
        self.setCentralWidget(self.group_box)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())