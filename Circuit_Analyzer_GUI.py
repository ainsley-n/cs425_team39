import sys
import os
from shutil import copyfile
from PyQt5 import QtWidgets, QtGui, QtCore
from tempfile import NamedTemporaryFile
from PyQt5.QtGui import QFont

from GUI.ui_MainMenu import Ui_MainWindow
from GUI.ui_AnalysisOptions import Ui_AnalysisWindow
from GUI.ui_RequestProperty import Ui_RequestProperty
from Drag_And_Drop_UI import drag_and_drop
from Drag_And_Drop_UI.fonts import getFont

from Circuit_Analyzer import create_circuit_from_file
from Circuit_Analyzer import perform_analysis
from Circuit_Analyzer import perform_norton_analysis
from Circuit_Analyzer import perform_thevenin_analysis
from Circuit_Analyzer import get_component_property
from Circuit_Analyzer import get_node_property

from Extra_Methods.LatexConverter import latexSingleTerm
from Extra_Methods.ImageConverter import latex_to_png
from Extra_Methods import ImageConverter
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

        # Attempt to load the font
        font = getFont('Drag_And_Drop_UI/fonts/brasika.otf')
        if font is not None:
            font.setPointSize(40)
            self.ui.label.setFont(font)
        else:
            try:
                font =  QFont("Brasika Display - Trial")
                font.setPointSize(40)
                self.ui.label.setFont(font)
            except:
                print("font loading failed")

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
        self.ui.homeButton.clicked.connect(controller.showHome)
        self.ui.RequestProperty.clicked.connect(controller.OpenPropertyRequest)

class RequestProperty(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super(RequestProperty, self).__init__()
        self.ui = Ui_RequestProperty()
        self.ui.setupUi(self)
        self.controller = controller
        self.ui.NodeButton.clicked.connect(self.ui.VoltageButton.setChecked)
        self.ui.NodeButton.clicked.connect(self.ui.CurrentButton.setDisabled)
        self.ui.ComponentButton.clicked.connect(self.ui.CurrentButton.setEnabled)

        #populate combobox when component or node button is clicked
        self.ui.ComponentButton.clicked.connect(self.populateComponents)
        self.ui.NodeButton.clicked.connect(self.populateNodes)

        self.ui.getPropertyBtn.clicked.connect(controller.DisplayProperty)

    def populateComponents(self):
        self.ui.comboBox.clear()
        #get list of components from controller circuit
        try:
            component_list = self.controller.circuit.sources + self.controller.circuit.components.resistors
            component_list += (self.controller.circuit.components.capacitors + self.controller.circuit.components.inductors)
            print(component_list)
        except Exception as e:
            controller.ErrorBox(str(e))
            return
        #add components to combobox
        self.ui.comboBox.addItems(component_list)
    #populateComponents

    def populateNodes(self):
        self.ui.comboBox.clear()
        #get list of nodes from controller circuit
        try:
            nodes = self.controller.circuit.nodes
            node_list = list(nodes.keys())
            node_list = sorted([node for node in node_list if node.isnumeric()], key=int)
        except Exception as e:
            controller.ErrorBox(str(e))
            return
        #add nodes to combobox
        self.ui.comboBox.addItems(node_list)
    #populateNodes
        

class Controller():
    def __init__(self):
        self.file_path = ""
        self.circuit = None
        self.circuit_image = NamedTemporaryFile(suffix='.png', delete=False).name
        self.analysis_latex = None
        self.analysis_latex_file = NamedTemporaryFile(suffix='.tex', delete=False).name
        self.analysis_pdf = self.analysis_latex_file.replace('.tex', '.pdf')
        self.analysis_image = self.analysis_latex_file.replace('.tex', '.png')
        self.simplified_circuit = None
        self.simplified_circuit_image = NamedTemporaryFile(suffix='.png', delete=False).name
        self.simplified_circuit_showing = False

        self.editor = drag_and_drop.MainWindow(drag_and_drop.Canvas())

        styleFile = QtCore.QFile(os.path.join(dirname, 'GUI/style.qss'))
        styleFile.open(QtCore.QFile.ReadOnly)
        style = str(styleFile.readAll() , encoding='utf-8')

        self.mainMenu = MainWindow(self)
        self.mainMenu.setStyleSheet(style)
        self.requestProperty = RequestProperty(self)
        #self.requestProperty.setStyleSheet(style)
        self.analysisWindow = AnalysisWindow(self)
        self.analysisWindow.setStyleSheet(style)
        self.mainMenu.showMaximized()
    #__init__

    def showHome(self):
        self.analysisWindow.hide()
        self.mainMenu.showMaximized()

    def OpenEditor(self):
        self.editor = drag_and_drop.MainWindow(drag_and_drop.Canvas())
        self.editor.show()
    #OpenEditor

    def OpenPropertyRequest(self):
        self.requestProperty = RequestProperty(self)
        self.requestProperty.show()

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

    def DoFileConversions(self):
        if self.analysis_latex is not None:
            try:
                self.analysis_latex_file = ImageConverter.get_latex_file(self.analysis_latex, self.analysis_latex_file)
                self.analysis_pdf = ImageConverter.get_pdf_file(self.analysis_latex_file, self.analysis_pdf)
                self.analysis_image = ImageConverter.get_png_file(self.analysis_pdf, self.analysis_image)
            except Exception as e:
                self.ErrorBox(str(e))

    def PerformAnalysis(self, analysis_type):
        if self.circuit is not None:
            if self.analysis_image is None:
                self.analysis_image = NamedTemporaryFile(suffix='.png', delete=False).name
            try:
                self.analysis_latex = perform_analysis(self.circuit, analysis_type)
            except Exception as e:
                self.ErrorBox(str(e))
            else:
                self.DoFileConversions()
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
                self.analysis_latex, self.simplified_circuit = perform_norton_analysis(self.circuit, self.simplified_circuit_image, start_node, end_node)
            except Exception as e:
                self.ErrorBox(str(e))
            else:
                self.DoFileConversions()
                self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(self.analysis_image))
                self.analysisWindow.ui.stackedWidget.setCurrentIndex(1)
                self.analysisWindow.ui.switchResult.show()
                self.analysisWindow.ui.switchResult.setText('Show Simplified Circuit')
                self.simplified_circuit_showing = False
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
                self.analysis_latex, self.simplified_circuit = perform_thevenin_analysis(self.circuit, self.simplified_circuit_image, start_node, end_node)
            except Exception as e:
                self.ErrorBox(str(e))
            else:
                self.DoFileConversions()
                self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(self.analysis_image))
                self.analysisWindow.ui.stackedWidget.setCurrentIndex(1)
                self.analysisWindow.ui.switchResult.show()
                self.analysisWindow.ui.switchResult.setText('Show Simplified Circuit')
                self.simplified_circuit_showing = False
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
            file_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', 'Documents/result.pdf', 'PDF Files (*.pdf);;PNG Files (*.png);;LaTeX Files (*.tex)')[0]
            if file_path:
                try:
                    if file_path.endswith('.pdf'):
                        copyfile(self.analysis_pdf, file_path)
                    elif file_path.endswith('.png'):
                        copyfile(self.analysis_image, file_path)
                    elif file_path.endswith('.tex'):
                        copyfile(self.analysis_latex_file, file_path)
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
            file_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', 'Documents/circuit.pdf', 'PDF Files (*.pdf);;PNG Files (*.png);;LaTeX Files (*.tex)')[0]
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
                    elif file_path.endswith('.tex'):
                        # create temp file
                        temp_file = NamedTemporaryFile(suffix='.tex', delete=False).name
                        circuit.draw(temp_file)
                        copyfile(temp_file, file_path)
                except Exception as e:
                    self.ErrorBox(str(e))
            else:
                self.ErrorBox('No file selected.')
        else:
            self.ErrorBox('No circuit to export.')
    #ExportCircuit

    def DisplayProperty(self):
        if self.circuit is not None:
            #get user input
            element = self.requestProperty.ui.comboBox.currentText()
            if element == '':
                self.ErrorBox('Please select a component or node.')
                return
            property = 'v' if self.requestProperty.ui.VoltageButton.isChecked() else 'i' if self.requestProperty.ui.CurrentButton.isChecked() else None
            if property is None:
                self.ErrorBox('Please select a property.')
                return
            try:
                if self.requestProperty.ui.ComponentButton.isChecked():
                    property_value = get_component_property(self.circuit, element, property)
                elif self.requestProperty.ui.NodeButton.isChecked():
                    property_value = get_node_property(self.circuit, int(element), property)
                else:
                    self.ErrorBox('Please select component or node.')
                    return
            except Exception as e:
                self.ErrorBox(str(e))
                return
            self.requestProperty.hide()
            # turn property into latex image
            if self.analysis_image is None:
                self.analysis_image = NamedTemporaryFile(suffix='.png', delete=False).name
            try:
                self.analysis_latex = latexSingleTerm(property_value, property)
                self.DoFileConversions()
            except Exception as e:
                self.ErrorBox(str(e))
                return
            self.analysisWindow.ui.SolutionImage.setPixmap(QtGui.QPixmap(self.analysis_image))
            self.analysisWindow.ui.stackedWidget.setCurrentIndex(1)
            self.analysisWindow.ui.switchResult.hide()
            self.simplified_circuit_showing = False
        else:
            self.ErrorBox('No circuit loaded.\nPlease load a circuit.')
    #DisplayProperty
            
            


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