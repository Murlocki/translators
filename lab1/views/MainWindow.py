from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
import os
import sys
from PyQt6.QtCore import Qt

from controllers.MainWindowController import MainWindowController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    def create(self):

        print(os.path.join(os.path.dirname(__file__), '..\\ui\\main.ui'))
        uic.loadUi(os.path.join(os.path.dirname(__file__), '..\\ui\\main.ui'), self)
        self.controller = MainWindowController(self)
        self.startButton.clicked.connect(lambda :self.controller.start())
        self.reverseButton.clicked.connect(lambda: self.controller.start_reverse())
        self.translateRButton.clicked.connect(lambda : self.controller.start_r_translate())
        self.syntButton.clicked.connect(lambda: self.controller.start_synt())
        return self
    def show(self):
        super().show()
        return self

    def closeEvent(self, QCloseEvent):
        del self.controller
        sys.exit()