import sys
import os
from PyQt5 import QtWidgets
from NewGUI.ui_MainMenu import Ui_MainWindow
import drag_and_drop

dirname = os.path.dirname(__file__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.newCircuit.clicked.connect(openEditor)

        


def openEditor():
    editor.show()
    

def getFileName():
    pass


app = QtWidgets.QApplication(sys.argv)
mainMenu = MainWindow()
editor = drag_and_drop.MainWindow(drag_and_drop.Canvas())
mainMenu.show()
app.exec()