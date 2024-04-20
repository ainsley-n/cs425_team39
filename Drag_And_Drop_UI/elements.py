from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QGraphicsPixmapItem
from Drag_And_Drop_UI.node import Node
from Drag_And_Drop_UI.setValueDialog import SetValueDialog
# from voltageSource import VoltageSource

class Element(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, name, pixmap, parent=None):
        super(Element, self).__init__(pixmap, parent)
        # self.setRect(rect)
        # self.setBrush(color)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.name = name
        self.nodes = []
        
        self.value_label = QtWidgets.QGraphicsTextItem("", self)
        self.value_label.setDefaultTextColor(QtGui.QColor("black"))
        self.value_label.setFont(QtGui.QFont("Arial", 8))
        # value_rect = self.value_label.boundingRect()
        self.value_label.setPos(self.boundingRect().bottomLeft().x() - 20, self.boundingRect().bottom() - 5)
        self.value_label.hide()  # Initially hide the value label 
        
    # def init_nodes(self):
    #     # Create nodes at desired positions
    #     if not self.nodes:
    #         self.nodes = [
    #             Node(self, self.boundingRect().topLeft() + QtCore.QPointF(self.boundingRect().width() / 2, 0)),  # Top middle
    #             Node(self, self.boundingRect().topLeft() + QtCore.QPointF(self.boundingRect().width() / 2, self.boundingRect().height())),  # Bottom middle
    #             Node(self, self.boundingRect().topLeft() + QtCore.QPointF(0, self.boundingRect().height() / 2)),  # Left middle
    #             Node(self, self.boundingRect().topLeft() + QtCore.QPointF(self.boundingRect().width(), self.boundingRect().height() / 2))  # Right middle
    #         ]
            
    def clone(self):
        # Create a new instance with the same properties
        cloned_element = Element(self.name, self.pixmap())
        cloned_element.init_nodes()
        return cloned_element
    
    def mousePressEvent(self, event):
        # Store the initial position of the element when the mouse is pressed
        self.initial_pos = self.pos()
        print(f"Element mousePressEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
        super(Element, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # print(f"Element mouseMoveEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
        super(Element, self).mouseMoveEvent(event)

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
    
    def contextMenuEvent(self, event):
        # Create a context menu for rotating the voltage source
        menu = QtWidgets.QMenu()
        rotate_action = menu.addAction("Rotate 90°")
        
        # Map the action to the rotate method
        rotate_action.triggered.connect(self.rotate)
        
        # Show the context menu at the cursor position
        menu.exec_(event.screenPos())

    def rotate(self):
        # Get the center point of the bounding rectangle
        center = self.boundingRect().center()
        
        # Set the transform origin to the center point
        self.setTransformOriginPoint(center)
        
        # Rotate the item by 90 degrees
        self.setRotation(self.rotation() + 90)
        
         # Rotate the label in the opposite direction to keep it upright
        self.value_label.setRotation(self.rotation() - 90)

        
    # def set_value(self, value):
    #     self.value = value
    #     self.value_label.setPlainText(str(value))
    #     self.value_label.show()

    # def mouseDoubleClickEvent(self, event):
    #     dialog = SetValueDialog(None)  # Pass None as the parent
    #     if dialog.exec_() == QtWidgets.QDialog.Accepted:
    #         value = dialog.get_value()
    #         if value is not None:
    #             self.set_value(value)
                
    # def get_value(self):
    #     return None
                

class CircularElement(QtWidgets.QGraphicsEllipseItem):
    deleted_node_labels = set()
    label_number = 0  
    
    @classmethod
    def increment_label_number(cls):
        cls.label_number += 1
        
    def __init__(self, name, rect, color, parent=None):
        diameter = min(rect.width(), rect.height())
        super(CircularElement, self).__init__(rect.topLeft().x(), rect.topLeft().y(), diameter, diameter, parent)
        self.setBrush(color)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.name = name
        self.nodes = []
        self.init_nodes()

        # Create a QGraphicsTextItem to display the name beneath the circle
        self.name_label = QtWidgets.QGraphicsTextItem("", self)
        self.name_label.setDefaultTextColor(QtGui.QColor("black"))
        self.name_label.setFont(QtGui.QFont("Arial", 8))
        self.name_label.setPos(self.rect().center().x() - self.name_label.boundingRect().width() / 2,
                        self.rect().center().y() - self.name_label.boundingRect().height() / 2)
        self.name_label.hide()  # Initially hide the name label

    def init_nodes(self):
        # Create nodes at the center of the circle
        if not self.nodes:
            center = self.rect().center()
            self.nodes = [
                Node(self, self.rect().topLeft() + QtCore.QPointF(self.rect().width() / 2, 0)),  # Top middle
                Node(self, self.rect().topLeft() + QtCore.QPointF(self.rect().width() / 2, self.rect().height())),  # Bottom middle
                Node(self, self.rect().topLeft() + QtCore.QPointF(0, self.rect().height() / 2)),  # Left middle
                Node(self, self.rect().topLeft() + QtCore.QPointF(self.rect().width(), self.rect().height() / 2))  # Right middle
                ]

    def clone(self):
        # Create a new instance with the same properties
        cloned_circular_element = CircularElement("", self.rect(), self.brush().color().lighter())
        cloned_circular_element.init_nodes()
        
        # Check if there are deleted node labels to reuse
        if self.deleted_node_labels:
            cloned_circular_element.label_number = self.deleted_node_labels.pop()
        else:
            # Increment the label number for the next CircularElement clone
            cloned_circular_element.label_number = self.label_number
            CircularElement.increment_label_number()
        
        # Update the name label for the clone
        cloned_circular_element.updateNameLabel()
        
        return cloned_circular_element
    
    def updateNameLabel(self):
        # Update the name label with the current name and label number
        self.name_label.setPlainText(f"{self.label_number}")
        self.name_label.show()

    def mousePressEvent(self, event):
        # Store the initial position of the element when the mouse is pressed
        self.initial_pos = self.pos()
        print(f"CircularElement mousePressEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
        super(CircularElement, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # print(f"CircularElement mouseMoveEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
        super(CircularElement, self).mouseMoveEvent(event)
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

    def deleteNode(self):
        # Add the label number of the deleted node to the set for reuse
        self.deleted_node_labels.add(self.label_number)
        # print(f'adding {self.label_number} to array')
  
    def get_value(self):
        return None
  