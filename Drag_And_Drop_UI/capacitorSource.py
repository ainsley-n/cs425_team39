from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QGraphicsPixmapItem
from Drag_And_Drop_UI.node import Node
from Drag_And_Drop_UI.elements import Element

class Capacitor(Element):
    deleted_capacitor_labels = set()
    label_number = 1  
    
    @classmethod
    def increment_label_number(cls):
        cls.label_number += 1

    def __init__(self, name, image_path, is_clone = False, parent=None):
        pixmap = QtGui.QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(30, 60)
        super().__init__(name, scaled_pixmap, parent)
        self.is_clone = is_clone
        
        # Create a QGraphicsTextItem to display the name beneath the circle
        self.name_label = QtWidgets.QGraphicsTextItem("", self)
        self.name_label.setDefaultTextColor(QtGui.QColor("black"))
        self.name_label.setFont(QtGui.QFont("Arial", 8))
        self.name_label.setPos(self.boundingRect().center().x() - self.name_label.boundingRect().width() - 17 ,self.boundingRect().center().y() + 12)
        self.name_label.hide()  # Initially hide the name label
        
        self.capacitance_value = 0
        
    def init_nodes(self):
        # Create nodes at desired positions
        if not self.nodes:
            self.nodes = [
                Node(self, self.boundingRect().topLeft() + QtCore.QPointF(self.boundingRect().width() / 2, 0)),  # Top middle
                Node(self, self.boundingRect().topLeft() + QtCore.QPointF(self.boundingRect().width() / 2, self.boundingRect().height())),  # Bottom middle
                # Node(self, self.boundingRect().topLeft() + QtCore.QPointF(0, self.boundingRect().height() / 2)),  # Left middle
                # Node(self, self.boundingRect().topLeft() + QtCore.QPointF(self.boundingRect().width(), self.boundingRect().height() / 2))  # Right middle
            ]
            
    def clone(self):
        # Create a new instance with the same properties
        cloned_capacitor = Capacitor(self.name, self.pixmap(), is_clone = True)
        cloned_capacitor.init_nodes()
        
        # Check if there are deleted node labels to reuse
        if self.deleted_capacitor_labels:
            cloned_capacitor.label_number = self.deleted_capacitor_labels.pop()
        else:
            # Increment the label number for the next CircularElement clone
            cloned_capacitor.label_number = self.label_number
            Capacitor.increment_label_number()
        
        # Update the name label for the clone
        cloned_capacitor.updateNameLabel()
        
        return cloned_capacitor
    
    def updateNameLabel(self):
        # Update the name label with the current name and label number
        self.name_label.setPlainText(f"C{self.label_number}")
        self.name_label.show()
        
    def mousePressEvent(self, event):
        # Store the initial position of the element when the mouse is pressed
        self.initial_pos = self.pos()
        # print(f"Capacitor mousePressEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
        super(Capacitor, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # print(f"CircularElement mouseMoveEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
        super(Capacitor, self).mouseMoveEvent(event)

        # Update the position of connected wires
        for node in self.nodes:
            for wire in node.connected_wires():
                if wire.start_node == node:
                    # Update the start position if the moving element is the start node
                    # print("Updating start position")
                    line = QtCore.QLineF(node.scenePos(), wire.line().p2())
                elif wire.end_node == node:
                    # Update the end position if the moving element is the end node
                    # print("Updating end position")
                    line = QtCore.QLineF(wire.line().p1(), node.scenePos())
                else:
                    continue
                wire.setLine(line)
        
    def deleteCapacitor(self):
        # Add the label number of the deleted node to the set for reuse
        self.deleted_capacitor_labels.add(self.label_number)
        # print(f'adding {self.label_number} to array')
        
    def mouseDoubleClickEvent(self, event):
        if self.is_clone:
            # Get the scene
            scene = self.scene()
            if scene is None:
                return

            # Get the first view associated with the scene
            view = scene.views()[0]
            dialog = QtWidgets.QInputDialog(view)
            dialog.setWindowTitle("Capacitor")
            dialog.setLabelText("Enter the Capacitence:")
            dialog.setOkButtonText("Set")
            dialog.setCancelButtonText("Cancel")
            dialog.setInputMode(QtWidgets.QInputDialog.DoubleInput)
            dialog.setDoubleRange(0, 1000)  # Set the range for the voltage source power
            dialog.setDoubleDecimals(2)  # Set the number of decimals
            dialog.setDoubleValue(self.get_value())  # Set the initial value

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                value = dialog.doubleValue()
                self.set_value(value)

    def get_value(self):
        # Retrieve the current value of the voltage source
        return self.capacitance_value

    def set_value(self, value):
        # Set the value of the voltage source
        self.capacitance_value = value
        self.value_label.setPlainText(f'{value} F')
        self.value_label.show()
    