import sys
import os
from shutil import copyfile
from PyQt5 import QtWidgets, QtGui, QtCore
from tempfile import NamedTemporaryFile

from GUI.ui_MainMenu import Ui_MainWindow
from GUI.ui_AnalysisOptions import Ui_AnalysisWindow
from Drag_And_Drop_UI import drag_and_drop

from Circuit_Analyzer import create_circuit_from_file
from Circuit_Analyzer import perform_analysis
from Circuit_Analyzer import perform_norton_analysis
from Circuit_Analyzer import perform_thevenin_analysis
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
        self.ui.TheveninAnalysis.clicked.connect(controller.PerformTheveninAnalysis)
        self.ui.NortonAnalysis.clicked.connect(controller.PerformNortonAnalysis)
        self.ui.ExportCircuitBtn.clicked.connect(lambda: controller.ExportCircuit(controller.circuit))
        self.ui.backButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.switchResult.clicked.connect(controller.SwitchResult)
        self.ui.exportButton.clicked.connect(controller.ExportResults)
        

class Controller():
    def __init__(self):
        self.file_path = ""
        self.circuit = None
        self.circuit_image = None
        self.analysis_image = None
        self.analysis_pdf = None
        self.simplified_circuit = None
        self.simplified_circuit_image = None
        self.simplified_circuit_showing = False
        self.editor = drag_and_drop.MainWindow(drag_and_drop.Canvas())
                
        styleFile = QtCore.QFile(os.path.join(dirname, 'GUI/style.qss'))
        styleFile.open(QtCore.QFile.ReadOnly)
        style = str(styleFile.readAll() , encoding='utf-8')

        self.mainMenu = MainWindow(self)
        self.mainMenu.setStyleSheet(style)
        self.analysisWindow = AnalysisWindow(self)
        self.analysisWindow.setStyleSheet(style)
        self.mainMenu.showMaximized()
    #__init__

    def OpenEditor(self):
        self.editor = drag_and_drop.MainWindow(drag_and_drop.Canvas())
        self.editor.show()
    #OpenEditor

    def OpenFile(self):
        new_file_path = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', '', 'All Files (*)')[0]
        if new_file_path:
            try:
                new_circuit = create_circuit_from_file(new_file_path)
            except FileNotFoundError:
                self.ErrorBox('File not found.\nTry again.')
                return
            except ValueError:
                self.ErrorBox('File does not contain a netlist.\nTry again.')
                return

            self.file_path = new_file_path
            self.circuit = new_circuit

            if self.circuit_image is None:
                self.circuit_image = NamedTemporaryFile(suffix='.png', delete=False).name

            try:
                self.circuit.draw(self.circuit_image)
            except Exception as e:
                self.ErrorBox(str(e))
                return

            self.mainMenu.hide()
            self.analysisWindow.ui.CircuitImage.setPixmap(QtGui.QPixmap(self.circuit_image))
            self.analysisWindow.ui.stackedWidget.setCurrentIndex(0)
            self.analysisWindow.showMaximized()
    #OpenFile

    def SaveFile(self):
        new_file_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', 'Documents/circuit.txt', 'Text Files (*.txt);;All Files (*)')[0]
        if new_file_path:
            self.file_path = new_file_path
            with open(self.file_path, 'w') as file:
                file.write(self.circuit.netlist())
    #SaveFile

    def PerformAnalysis(self, analysis_type):
        if self.circuit is not None:
            if self.analysis_image is None:
                self.analysis_image = NamedTemporaryFile(suffix='.png', delete=False).name
            try:
                self.analysis_pdf = perform_analysis(self.circuit, analysis_type, self.analysis_image)
            except Exception as e:
                self.ErrorBox(str(e))
            else:
                self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(self.analysis_image))
                self.analysisWindow.ui.stackedWidget.setCurrentIndex(1)
                self.analysisWindow.ui.switchResult.hide()
                self.simplified_circuit_showing = False
        else:
            self.ErrorBox('No circuit loaded.\nPlease load a circuit.')
    #PerformAnalysis
        
    def PerformNortonAnalysis(self):
        if self.circuit is not None:
            if self.analysis_image is None:
                self.analysis_image = NamedTemporaryFile(suffix='.png', delete=False).name
            if self.simplified_circuit_image is None:
                self.simplified_circuit_image = NamedTemporaryFile(suffix='.png', delete=False).name

            # Get user input for start and end nodes
            # get list of nodes
            try:
                nodes = self.circuit.nodes
                node_list = list(nodes.keys())
                node_list = sorted([node for node in node_list if node.isnumeric()], key=int)
            except Exception as e:
                self.ErrorBox(str(e))
                return
            
            # get user input
            start_node, okPressed = QtWidgets.QInputDialog.getItem(None, "Get start node","Start Node:", node_list, 0, False)
            if not okPressed:
                return
            node_list.remove(start_node)
            end_node, okPressed = QtWidgets.QInputDialog.getItem(None, "Get end node","End Node:", node_list, 0, False)
            if not okPressed:
                return
            if start_node == end_node:
                self.ErrorBox('Start and end nodes cannot be the same.\nPlease try again.')
                return
            
            try:
                self.analysis_pdf, self.simplified_circuit = perform_norton_analysis(self.circuit, self.simplified_circuit_image, self.analysis_image, start_node, end_node)
            except Exception as e:
                self.ErrorBox(str(e))
            else:
                self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(self.analysis_image))
                self.analysisWindow.ui.stackedWidget.setCurrentIndex(1)
                self.analysisWindow.ui.switchResult.show()
                self.analysisWindow.ui.switchResult.setText('Show Simplified Circuit')
        else:
            self.ErrorBox('No circuit loaded.\nPlease load a circuit.')
    #PerformNortonAnalysis

    def PerformTheveninAnalysis(self):
        if self.circuit is not None:
            if self.analysis_image is None:
                self.analysis_image = NamedTemporaryFile(suffix='.png', delete=False).name
            if self.simplified_circuit_image is None:
                self.simplified_circuit_image = NamedTemporaryFile(suffix='.png', delete=False).name

            # Get user input for start and end nodes
            # get list of nodes
            try:
                nodes = self.circuit.nodes
                node_list = list(nodes.keys())
                node_list = sorted([node for node in node_list if node.isnumeric()], key=int)
            except Exception as e:
                self.ErrorBox(str(e))
                return
            
            # get user input
            start_node, okPressed = QtWidgets.QInputDialog.getItem(None, "Get start node","Start Node:", node_list, 0, False)
            if not okPressed:
                return
            node_list.remove(start_node)
            end_node, okPressed = QtWidgets.QInputDialog.getItem(None, "Get end node","End Node:", node_list, 0, False)
            if not okPressed:
                return
            if start_node == end_node:
                self.ErrorBox('Start and end nodes cannot be the same.\nPlease try again.')
                return
            
            try:
                self.analysis_pdf, self.simplified_circuit = perform_thevenin_analysis(self.circuit, self.simplified_circuit_image, self.analysis_image, start_node, end_node)
            except Exception as e:
                self.ErrorBox(str(e))
            else:
                self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(self.analysis_image))
                self.analysisWindow.ui.stackedWidget.setCurrentIndex(1)
                self.analysisWindow.ui.switchResult.show()
                self.analysisWindow.ui.switchResult.setText('Show Simplified Circuit')
        else:
            self.ErrorBox('No circuit loaded.\nPlease load a circuit.')
    #PerformTheveninAnalysis

    def SwitchResult(self):
        if not self.simplified_circuit_showing:
            self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(self.simplified_circuit_image))
            self.analysisWindow.ui.switchResult.setText('Show Symbolic Equations')
            self.simplified_circuit_showing = True
        else:
            self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(self.analysis_image))
            self.analysisWindow.ui.switchResult.setText('Show Simplified Circuit')
            self.simplified_circuit_showing = False
    #SwitchResult

    def ExportResults(self):
        if not self.simplified_circuit_showing:
            # get file path for pdf or png
            file_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', 'Documents/result.pdf', 'PDF Files (*.pdf);;PNG Files (*.png)')[0]
            if file_path:
                try:
                    if file_path.endswith('.pdf'):
                        copyfile(self.analysis_pdf, file_path)
                    elif file_path.endswith('.png'):
                        copyfile(self.analysis_image, file_path)
                    else:
                        self.ErrorBox('Invalid file type.\nPlease select a PDF or PNG file.')
                except Exception as e:
                    self.ErrorBox(str(e))
            else:
                self.ErrorBox('No file selected.')
        else:
            self.ExportCircuit(self.simplified_circuit)
    
    #ExportResults

    def ExportCircuit(self, circuit):
        if circuit is not None:
            # get file path for pdf or png
            file_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', 'Documents/circuit.pdf', 'PDF Files (*.pdf);;PNG Files (*.png)')[0]
            if file_path:
                try:
                    if file_path.endswith('.pdf'):
                        # create temp file
                        temp_file = NamedTemporaryFile(suffix='.pdf', delete=False).name
                        circuit.draw(temp_file)
                        copyfile(temp_file, file_path)
                    elif file_path.endswith('.png'):
                        # create temp file
                        temp_file = NamedTemporaryFile(suffix='.png', delete=False).name
                        circuit.draw(temp_file)
                        copyfile(temp_file, file_path)
                except Exception as e:
                    self.ErrorBox(str(e))
            else:
                self.ErrorBox('No file selected.')
        else:
            self.ErrorBox('No circuit to export.')

    def ErrorBox(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
    #ErrorBox




app = QtWidgets.QApplication(sys.argv)
controller = Controller()

app.exec()