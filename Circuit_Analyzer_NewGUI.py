import sys
import os
from PyQt5 import QtWidgets, QtGui

from NewGUI.ui_MainMenu import Ui_MainWindow
#from NewGUI.ui_CircuitAnalysis import Ui_AnalysisWindow
from NewGUI.ui_AnalysisOptions import Ui_AnalysisWindow
from Drag_And_Drop_UI import drag_and_drop

from Circuit_Analyzer import create_circuit_from_file
from lcapy import Circuit

dirname = os.path.dirname(__file__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.newCircuit.clicked.connect(controller.OpenEditor)
        self.ui.actionNew.triggered.connect(controller.OpenEditor)
        self.ui.openCircuit.clicked.connect(controller.OpenFile)
        self.ui.actionOpen.triggered.connect(controller.OpenFile)

class AnalysisWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super(AnalysisWindow, self).__init__()
        self.ui = Ui_AnalysisWindow()
        self.ui.setupUi(self)
        self.ui.actionNew.triggered.connect(controller.OpenEditor)
        self.ui.actionOpen.triggered.connect(controller.OpenFile)
        self.ui.actionSave.triggered.connect(controller.SaveFile)
        

class Controller():
    def __init__(self):
        self.file_path = ""
        self.circuit = None
        self.editor = drag_and_drop.MainWindow(drag_and_drop.Canvas())
        self.mainMenu = MainWindow(self)
        self.analysisWindow = AnalysisWindow(self)
        self.mainMenu.show()
    def OpenEditor(self):
        self.editor = drag_and_drop.MainWindow(drag_and_drop.Canvas())
        self.editor.show()
    def OpenFile(self):
        new_file_path = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', '', 'All Files (*)')[0]
        if new_file_path != '':
            self.file_path = new_file_path
            try:
                self.circuit = create_circuit_from_file(self.file_path)
            except FileNotFoundError:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('File Does Not Exist')
                msg.setWindowTitle("Error")
                msg.exec_()
            except ValueError:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('File does not contain a netlist.\nTry again.')
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                self.circuit.draw('temp/circuit.png')
                self.analysisWindow.ui.CircuitImage.setPixmap(QtGui.QPixmap('temp/circuit.png'))
                self.analysisWindow.show()
                self.mainMenu.hide()
    def SaveFile(self):
        new_file_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', '', 'Text Files (*.txt);;All Files (*)')[0]
        if new_file_path:
            self.file_path = new_file_path
            with open(self.file_path, 'w') as file:
                file.write(self.circuit.netlist())
    




app = QtWidgets.QApplication(sys.argv)
controller = Controller()

app.exec()