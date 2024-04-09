import time

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat
from PyQt6.QtWidgets import QTextEdit

from models.LecAnalysis import LecAnalysis


class MainWindowController():
    def __init__(self,window):
        super(MainWindowController,self).__init__()
        self._window = window
        self._model = LecAnalysis()
        self.out=''
        self.start_select=0
        self.end_select=0
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
        f.close()
    def start_reverse(self):
        out=self._model.reverse_polsk()
        self._window.reverse_output.setText(out)
        f = open('./files/reverse_polsk.txt', 'w')
        f.write(out)
        f.close()
    def start_r_translate(self):
        out=self._model.translate_to_R()
        self._window.traslateR_output.setText(out)
        f = open('./files/ROutput.txt','w')
        f.write(out)
        f.close()
    def start_synt(self):
        out=self._model.analyzer()
        f = open('./files/error.txt', 'r')
        out=f.read()
        f.close()
        self._window.errors_output.setText(out)
        if out:
            strs = out.split('\n')[0]
            str_number = int(strs.split(' ')[3])
            print(str_number)
            input_program = self._window.input.toPlainText()
            self.start_select = 0
            self.end_select = 0
            counter = 0
            for i in range(len(input_program)):
                if input_program[i] == '\n':
                    counter += 1
                    if counter == str_number - 1:
                        self.start_select = i + 1
                    if counter == str_number:
                        self.end_select = i
            print(counter, self.start_select, self.end_select)
            self.cursor = self._window.input.textCursor()
            self.cursor.setPosition(self.start_select)
            self.cursor.setPosition(self.end_select, QTextCursor.MoveMode.KeepAnchor)
            self._window.input.setTextCursor(self.cursor)

            form = QTextCharFormat()
            form.setBackground(Qt.GlobalColor.yellow)
            selection = QTextEdit.ExtraSelection()
            selection.format = form
            selection.cursor = self.cursor
            self._window.input.setExtraSelections([selection])
            self._window.input.setFocus()

        self._window.update()
