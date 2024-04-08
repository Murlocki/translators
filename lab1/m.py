import re

from PyQt6.QtWidgets import QApplication

from models.LecAnalysis import LecAnalysis
from views.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    # mainWindow = MainWindow()
    # mainWindow.create()
    # mainWindow.show()
    # app.exec()
    print(re.match(r'^M\d+$','M11111'))
    p = LecAnalysis()
    out,inp=p.process()
    f = open('./files/Output.txt','w')
    f.write(out)
    f.close()
    out=p.reverse_polsk()
    f = open('./files/reverse_polsk.txt', 'w')
    f.write(out)
    f.close()
    out=p.translate_to_R()
    print(out)