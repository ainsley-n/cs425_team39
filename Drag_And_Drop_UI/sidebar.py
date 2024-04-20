from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
from Drag_And_Drop_UI.elements import Element, CircularElement
from Drag_And_Drop_UI.voltageSource import VoltageSource
from Drag_And_Drop_UI.resistorSource import Resistor
from Drag_And_Drop_UI.capacitorSource import Capacitor
from Drag_And_Drop_UI.inductorSource import Inductor

class Sidebar(QtWidgets.QGraphicsView):
    def __init__(self, canvas, parent=None):
        super(Sidebar, self).__init__(parent)
        self.canvas = canvas
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setStyleSheet("background-color: #A6ADEB")
        self.create_sidebar_elements()  

    def create_sidebar_elements(self):
        voltageSource = VoltageSource("Voltage Source", "Drag_And_Drop_UI/Images/voltage_source1.png")
        resistor = Resistor("Resistor", "Drag_And_Drop_UI/Images/resistor_image1.png")
        capacitor = Capacitor("Capacitor", "Drag_And_Drop_UI/Images/capacitor_image1.png")
        inductor = Inductor("Inductor", "Drag_And_Drop_UI/Images/inductor_image1.png")
        node = CircularElement("Node", QtCore.QRectF(0, 250, 50, 20), QtGui.QColor("blue"))
        
        voltageSource.setPos(0, 0)
        resistor.setPos(-10, 70)
        capacitor.setPos(0, 120)
        inductor.setPos(-20, 200)
        
        self.scene().addItem(voltageSource)
        self.scene().addItem(resistor)
        self.scene().addItem(capacitor)
        self.scene().addItem(inductor)
        self.scene().addItem(node)
        
        
        self.elements = {
            "Voltage Source": voltageSource,
            "Resistor": resistor,
            "Capacitor": capacitor,
            "Inductor": inductor,
            "Node": node
        }

        for element in self.elements.values():
            element.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
            # Display the name label for the original element
            name_label = QtWidgets.QGraphicsTextItem(element.name, element)
            name_label.setDefaultTextColor(QtGui.QColor("black"))  # Set text color
            name_label.setFont(QtGui.QFont("Arial", 8))  # Set font and size
            name_rect = name_label.boundingRect()
            name_label.setPos(element.boundingRect().left() - name_rect.width(),  # Adjust the offset as needed
                       element.boundingRect().center().y() - name_rect.height() / 2)
            element.name_label = name_label  # Store the label in the element for later reference
            
            
    def mousePressEvent(self, event):
        try:
            item = self.itemAt(event.pos())
            print(f"Sidebar mousePressEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
            if item and (isinstance(item, Element) or isinstance(item, CircularElement) or (isinstance(item, VoltageSource))):
                print(f"Sidebar mousePressEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
                # Create a copy of the selected element and add it to the main canvas
                copied_element = item.clone()
                copied_element.setPos(50, 50)  # Set a default position for the copied element
                self.canvas.scene().addItem(copied_element)
        except Exception as e:
            print(f"Exception in mousePressEvent: {e}")
