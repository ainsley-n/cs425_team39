import sys
import os
from PyQt5 import QtWidgets, QtGui

from GUI.ui_MainMenu import Ui_MainWindow
from GUI.ui_AnalysisOptions import Ui_AnalysisWindow
from Drag_And_Drop_UI import drag_and_drop

from Circuit_Analyzer import create_circuit_from_file
from Circuit_Analyzer import perform_analysis
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
        self.ui.actionMesh.triggered.connect(lambda: controller.PerformAnalysis('Mesh analysis'))
        self.ui.MeshAnalysis.clicked.connect(lambda: controller.PerformAnalysis('Mesh analysis'))
        self.ui.actionNodal.triggered.connect(lambda: controller.PerformAnalysis('Nodal analysis'))
        self.ui.NodeAnalysis.clicked.connect(lambda: controller.PerformAnalysis('Nodal analysis'))
        self.ui.backButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        

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
            try:
                new_circuit = create_circuit_from_file(new_file_path)
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
                self.file_path = new_file_path
                self.circuit = new_circuit
                self.circuit.draw('temp/circuit.png')
                self.analysisWindow.ui.CircuitImage.setPixmap(QtGui.QPixmap('temp/circuit.png'))
                self.analysisWindow.ui.stackedWidget.setCurrentIndex(0)
                self.analysisWindow.show()
                self.mainMenu.hide()
    def SaveFile(self):
        new_file_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', '', 'Text Files (*.txt);;All Files (*)')[0]
        if new_file_path:
            self.file_path = new_file_path
            with open(self.file_path, 'w') as file:
                file.write(self.circuit.netlist())
    def PerformAnalysis(self, analysis_type):
        if self.circuit:
            try:
                result_file = perform_analysis(self.circuit, analysis_type)
            except ValueError as e:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(result_file))
                self.analysisWindow.ui.stackedWidget.setCurrentIndex(1)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No circuit loaded.\nPlease load a circuit.')
            msg.setWindowTitle("Error")
            msg.exec_()
        
    




app = QtWidgets.QApplication(sys.argv)
controller = Controller()

app.exec()