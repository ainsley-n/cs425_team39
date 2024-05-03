from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
from Drag_And_Drop_UI.wire import Wire

class Node(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, parent, position):
        super(Node, self).__init__(parent)
        self.setRect(-3, -3, 6, 6)  # Adjust the size of the node
        self.setPos(position)
        self.setBrush(QtGui.QColor("#183B23"))
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.wire_in_progress = None
        self.hovering = False

    def hoverEnterEvent(self, event):
        # Change the color when the mouse hovers over the node
        # print('Hovering Node')
        self.hovering = True
        self.setRect(-6, -6, 9, 9)  # Increase the size of the node
        super(Node, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Restore the original color when the mouse leaves the node
        # print('Stop hovering node')
        self.hovering = False
        self.setRect(-3, -3, 6, 6)  # Restore the original size of the node
        super(Node, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # Create a wire starting from this node
            print(f"Node mousePressEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
            self.wire_in_progress = Wire(self.scenePos(), self.scenePos())
            self.scene().addItem(self.wire_in_progress)
            event.accept()

    def mouseMoveEvent(self, event):
        if self.wire_in_progress:
            # Update the position of the wire while dragging
            # print(f"Node mouseMoveEvent - LeftButton: {self.mapToScene(event.pos()).x()}, {self.mapToScene(event.pos()).y()}")
            line = QtCore.QLineF(self.wire_in_progress.line().p1(), self.mapToScene(event.pos()))
            self.wire_in_progress.setLine(line)


    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.wire_in_progress:
            # Get the release point in scene coordinates
            release_point = self.mapToScene(event.pos())

            # Find all Node items in the scene
            all_nodes = [item for item in self.scene().items() if isinstance(item, Node) and item != self]

            # Find the closest node within 10 pixels radius
            min_distance = float('inf')
            closest_node = None
            for node in all_nodes:
                distance = (node.scenePos() - release_point).manhattanLength()  # Using manhattanLength to calculate distance
                if distance < min_distance and distance <= 15:  # Check if within 15 pixels
                    min_distance = distance
                    closest_node = node

            if closest_node:
                # Snap and connect the wire to the closest node
                print(f"Node mouseReleaseEvent - LeftButton: {release_point.x()}, {release_point.y()}")
                self.wire_in_progress.setLine(QtCore.QLineF(self.wire_in_progress.line().p1(), closest_node.scenePos()))
                self.wire_in_progress.start_node = self
                self.wire_in_progress.end_node = closest_node
                closest_node.wire_in_progress = self.wire_in_progress
            else:
                # Remove the wire if no suitable node found within the radius
                self.scene().removeItem(self.wire_in_progress)

            self.wire_in_progress = None

            
    def connected_wires(self):
        # Return a list of wires connected to this node
        return [wire for wire in self.scene().items() if isinstance(wire, Wire) and (wire.start_node == self or wire.end_node == self)]



