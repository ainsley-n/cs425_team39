from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QGraphicsPixmapItem
from node import Node
from setValueDialog import SetValueDialog
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
        self.init_nodes()
        
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
  
        
# class Capacitor(Element):
#     deleted_capacitor_labels = set()
#     label_number = 1  
    
#     @classmethod
#     def increment_label_number(cls):
#         cls.label_number += 1

#     def __init__(self, name, rect, color, parent=None):
#         super().__init__(name, rect, color, parent)
        
#         # Create a QGraphicsTextItem to display the name beneath the circle
#         self.name_label = QtWidgets.QGraphicsTextItem("", self)
#         self.name_label.setDefaultTextColor(QtGui.QColor("black"))
#         self.name_label.setFont(QtGui.QFont("Arial", 8))
#         # name_rect = self.name_label.boundingRect()
#         self.name_label.setPos(self.rect().center().x() - self.name_label.boundingRect().width() / 2,
#                         self.rect().center().y() - self.name_label.boundingRect().height() / 2)
#         self.name_label.hide()  # Initially hide the name label
#         self.capacitance_value = 0
        
#     def clone(self):
#         # Create a new instance with the same properties
#         cloned_capacitor = Capacitor("", self.rect(), self.brush().color().lighter())
#         cloned_capacitor.init_nodes()
        
#         # Check if there are deleted node labels to reuse
#         if self.deleted_capacitor_labels:
#             cloned_capacitor.label_number = self.deleted_capacitor_labels.pop()
#         else:
#             # Increment the label number for the next CircularElement clone
#             cloned_capacitor.label_number = self.label_number
#             Capacitor.increment_label_number()
        
#         # Update the name label for the clone
#         cloned_capacitor.updateNameLabel()
        
#         return cloned_capacitor
    
#     def updateNameLabel(self):
#         # Update the name label with the current name and label number
#         self.name_label.setPlainText(f"C{self.label_number}")
#         self.name_label.show()
        
#     def mousePressEvent(self, event):
#         # Store the initial position of the element when the mouse is pressed
#         self.initial_pos = self.pos()
#         print(f"Capacitor mousePressEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
#         super(Capacitor, self).mousePressEvent(event)

#     def mouseMoveEvent(self, event):
#         super(Capacitor, self).mouseMoveEvent(event)

#         # Update the position of connected wires
#         for node in self.nodes:
#             for wire in node.connected_wires():
#                 if wire.start_node == node:
#                     # Update the start position if the moving element is the start node
#                     # print("Updating start position")
#                     line = QtCore.QLineF(node.scenePos(), wire.line().p2())
#                 elif wire.end_node == node:
#                     # Update the end position if the moving element is the end node
#                     # print("Updating end position")
#                     line = QtCore.QLineF(wire.line().p1(), node.scenePos())
#                 else:
#                     continue
#                 wire.setLine(line)
        
#     def deleteCapacitor(self):
#         # Add the label number of the deleted node to the set for reuse
#         self.deleted_capacitor_labels.add(self.label_number)
#         # print(f'adding {self.label_number} to array')
        
#     def mouseDoubleClickEvent(self, event):
#         # Get the scene
#         scene = self.scene()
#         if scene is None:
#             return

#         # Get the first view associated with the scene
#         view = scene.views()[0]
#         dialog = QtWidgets.QInputDialog(view)
#         dialog.setWindowTitle("Capacitor")
#         dialog.setLabelText("Enter the Capacitance:")
#         dialog.setOkButtonText("Set")
#         dialog.setCancelButtonText("Cancel")
#         dialog.setInputMode(QtWidgets.QInputDialog.DoubleInput)
#         dialog.setDoubleRange(0, 1000)  # Set the range for the resistor
#         dialog.setDoubleDecimals(2)  # Set the number of decimals
#         dialog.setDoubleValue(self.get_value())  # Set the initial value

#         if dialog.exec_() == QtWidgets.QDialog.Accepted:
#             value = dialog.doubleValue()
#             self.set_value(value)

#     def get_value(self):
#         # Retrieve the current value of the resistor 
#         return self.capacitance_value

#     def set_value(self, value):
#         # Set the value of the resisitor
#         self.capacitance_value = value
#         self.value_label.setPlainText(f"{value} F")
#         self.value_label.show()
        
        
# class Inductor(Element):
#     deleted__labels = set()
#     label_number = 1  
    
#     @classmethod
#     def increment_label_number(cls):
#         cls.label_number += 1

#     def __init__(self, name, rect, color, parent=None):
#         super().__init__(name, rect, color, parent)
        
#         # Create a QGraphicsTextItem to display the name beneath the circle
#         self.name_label = QtWidgets.QGraphicsTextItem("", self)
#         self.name_label.setDefaultTextColor(QtGui.QColor("black"))
#         self.name_label.setFont(QtGui.QFont("Arial", 8))
#         # name_rect = self.name_label.boundingRect()
#         self.name_label.setPos(self.rect().center().x() - self.name_label.boundingRect().width() / 2,
#                         self.rect().center().y() - self.name_label.boundingRect().height() / 2)
#         self.name_label.hide()  # Initially hide the name label
#         self.inductance_value = 0
        
#     def clone(self):
#         # Create a new instance with the same properties
#         cloned_inductor = Inductor("", self.rect(), self.brush().color().lighter())
#         cloned_inductor.init_nodes()
        
#         # Check if there are deleted node labels to reuse
#         if self.deleted_inductor_labels:
#             cloned_inductor.label_number = self.deleted_inductor_labels.pop()
#         else:
#             # Increment the label number for the next CircularElement clone
#             cloned_inductor.label_number = self.label_number
#             Inductor.increment_label_number()
        
#         # Update the name label for the clone
#         cloned_inductor.updateNameLabel()
        
#         return cloned_inductor
    
#     def updateNameLabel(self):
#         # Update the name label with the current name and label number
#         self.name_label.setPlainText(f"L{self.label_number}")
#         self.name_label.show()
        
#     def mousePressEvent(self, event):
#         # Store the initial position of the element when the mouse is pressed
#         self.initial_pos = self.pos()
#         print(f"Inductor mousePressEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
#         super(Inductor, self).mousePressEvent(event)

#     def mouseMoveEvent(self, event):
#         super(Inductor, self).mouseMoveEvent(event)

#         # Update the position of connected wires
#         for node in self.nodes:
#             for wire in node.connected_wires():
#                 if wire.start_node == node:
#                     # Update the start position if the moving element is the start node
#                     # print("Updating start position")
#                     line = QtCore.QLineF(node.scenePos(), wire.line().p2())
#                 elif wire.end_node == node:
#                     # Update the end position if the moving element is the end node
#                     # print("Updating end position")
#                     line = QtCore.QLineF(wire.line().p1(), node.scenePos())
#                 else:
#                     continue
#                 wire.setLine(line)
        
#     def deleteInductor(self):
#         # Add the label number of the deleted node to the set for reuse
#         self.deleted_inductor_labels.add(self.label_number)
#         # print(f'adding {self.label_number} to array')
        
#     def mouseDoubleClickEvent(self, event):
#         # Get the scene
#         scene = self.scene()
#         if scene is None:
#             return

#         # Get the first view associated with the scene
#         view = scene.views()[0]
#         dialog = QtWidgets.QInputDialog(view)
#         dialog.setWindowTitle("Capacitor")
#         dialog.setLabelText("Enter the Capacitance:")
#         dialog.setOkButtonText("Set")
#         dialog.setCancelButtonText("Cancel")
#         dialog.setInputMode(QtWidgets.QInputDialog.DoubleInput)
#         dialog.setDoubleRange(0, 1000)  # Set the range for the resistor
#         dialog.setDoubleDecimals(2)  # Set the number of decimals
#         dialog.setDoubleValue(self.get_value())  # Set the initial value

#         if dialog.exec_() == QtWidgets.QDialog.Accepted:
#             value = dialog.doubleValue()
#             self.set_value(value)

#     def get_value(self):
#         # Retrieve the current value of the resistor 
#         return self.inductance_value

#     def set_value(self, value):
#         # Set the value of the resisitor
#         self.inductance_value = value
#         self.value_label.setPlainText(f"{value} F")
#         self.value_label.show()