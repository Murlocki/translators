from PyQt6.QtWidgets import QApplication

from views.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.create()
    mainWindow.show()
    app.exec()