import time
from PyQt6.QtGui import QTextCursor

from models.LecAnalysis import LecAnalysis


class MainWindowController():
    def __init__(self,window):
        super(MainWindowController,self).__init__()
        self._window = window
        self._model = LecAnalysis()
    @property
    def window(self):
        return self._window
    @property
    def model(self):
        return self._model
    def start(self):
        out,inp=self._model.process()
        self._window.output.setText(out)
        self._window.input.setText(inp)
        f = open('./files/Output.txt','w')
        f.write(out)
    def start_reverse(self):
        out=self._model.reverse_polsk()
        self._window.reverse_output.setText(out)
        f = open('./files/reverse_polsk.txt', 'w')
        f.write(out)