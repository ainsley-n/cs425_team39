from PyQt5 import QtWidgets, QtGui, QtCore

class Node(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, parent, position):
        super(Node, self).__init__(parent)
        self.setRect(-3, -3, 6, 6)  # Adjust the size of the node
        self.setPos(position)
        self.setBrush(QtGui.QColor("red"))
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.wire_in_progress = None
        self.hovering = False

    def hoverEnterEvent(self, event):
        # Change the color when the mouse hovers over the node
        print('Hovering Node')
        self.hovering = True
        super(Node, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Restore the original color when the mouse leaves the node
        print('Stop hovering node')
        self.hovering = False
        super(Node, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # Create a wire starting from this node
            self.wire_in_progress = Wire(self.scenePos(), self.scenePos())
            self.scene().addItem(self.wire_in_progress)
            event.accept()

    def mouseMoveEvent(self, event):
        if self.wire_in_progress:
            # Update the position of the wire while dragging
            line = QtCore.QLineF(self.wire_in_progress.line().p1(), self.mapToScene(event.pos()))
            self.wire_in_progress.setLine(line)
            
            

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.wire_in_progress:
            # Find the item at the release point, considering only Node items
            items_at_release = self.scene().items(self.mapToScene(event.pos()))
            end_item = next((item for item in items_at_release if isinstance(item, Node) and item != self), None)

            print(f'End Item: {end_item}')
            if end_item:
                # Connect the wire to the end node
                self.wire_in_progress.setLine(QtCore.QLineF(self.wire_in_progress.line().p1(), end_item.scenePos()))
                self.wire_in_progress.start_node = self
                self.wire_in_progress.end_node = end_item
                end_item.wire_in_progress = self.wire_in_progress
            else:
                # Remove the wire if it doesn't connect to a node
                self.scene().removeItem(self.wire_in_progress)

            self.wire_in_progress = None
            
    def connected_wires(self):
        # Return a list of wires connected to this node
        return [wire for wire in self.scene().items() if isinstance(wire, Wire) and (wire.start_node == self or wire.end_node == self)]
    
    

class Element(QtWidgets.QGraphicsRectItem):
    def __init__(self, name, rect, color, parent=None):
        super(Element, self).__init__(parent)
        self.setRect(rect)
        self.setBrush(color)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.name = name
        self.nodes = []
        self.init_nodes()
        
        
        # Create a QGraphicsTextItem to display the name beneath the box
        self.name_label = QtWidgets.QGraphicsTextItem(self.name, self)
        self.name_label.setDefaultTextColor(QtGui.QColor("white"))  # Set text color
        self.name_label.setFont(QtGui.QFont("Arial", 8))  # Set font and size
        name_rect = self.name_label.boundingRect()
        self.name_label.setPos(self.rect().center().x() - name_rect.width() / 2,
                               self.rect().bottom() + 2)  # Adjust the vertical position
    
    def init_nodes(self):
        # Create nodes at desired positions
        if not self.nodes:
            self.nodes = [
                Node(self, self.rect().topLeft() + QtCore.QPointF(self.rect().width() / 2, 0)),  # Top middle
                Node(self, self.rect().topLeft() + QtCore.QPointF(self.rect().width() / 2, self.rect().height())),  # Bottom middle
                Node(self, self.rect().topLeft() + QtCore.QPointF(0, self.rect().height() / 2)),  # Left middle
                Node(self, self.rect().topLeft() + QtCore.QPointF(self.rect().width(), self.rect().height() / 2))  # Right middle
            ]


    def clone(self):
        # Create a new instance with the same properties
        cloned_element = Element("", self.rect(), self.brush().color().lighter())
        cloned_element.init_nodes()
        return cloned_element
    
    def mousePressEvent(self, event):
        # Store the initial position of the element when the mouse is pressed
        self.initial_pos = self.pos()
        super(Element, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        print(f"Element mouseMoveEvent - LeftButton: {event.buttons() == QtCore.Qt.LeftButton}")
        super(Element, self).mouseMoveEvent(event)

        # Update the position of connected wires
        for node in self.nodes:
            for wire in node.connected_wires():
                if wire.start_node == node:
                    # Update the start position if the moving element is the start node
                    print("Updating start position")
                    line = QtCore.QLineF(node.scenePos(), wire.line().p2())
                elif wire.end_node == node:
                    # Update the end position if the moving element is the end node
                    print("Updating end position")
                    line = QtCore.QLineF(wire.line().p1(), node.scenePos())
                else:
                    continue
                wire.setLine(line)
        
        
class Wire(QtWidgets.QGraphicsLineItem):
    def __init__(self, start_pos, end_pos, parent=None):
        super(Wire, self).__init__(parent)
        self.setLine(QtCore.QLineF(start_pos, end_pos))
        self.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)



class Sidebar(QtWidgets.QGraphicsView):
    def __init__(self, canvas, parent=None):
        super(Sidebar, self).__init__(parent)
        self.canvas = canvas
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.create_sidebar_elements()

    def create_sidebar_elements(self):
        voltageSource = Element("Voltage Source", QtCore.QRectF(0, 0, 50, 20), QtGui.QColor("red"))
        resistor = Element("Resistor", QtCore.QRectF(0, 50, 50, 20), QtGui.QColor("blue"))
        capacitor = Element("Capacitor", QtCore.QRectF(0, 100, 50, 20), QtGui.QColor("yellow"))

        self.scene().addItem(voltageSource)
        self.scene().addItem(resistor)
        self.scene().addItem(capacitor)
        
        self.elements = {
            "Voltage Source": voltageSource,
            "Resistor": resistor,
            "Capacitor": capacitor
        }

        for element in self.elements.values():
            element.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
            # Display the name label for the original element
            name_label = QtWidgets.QGraphicsTextItem(element.name, element)
            name_label.setDefaultTextColor(QtGui.QColor("black"))  # Set text color
            name_label.setFont(QtGui.QFont("Arial", 8))  # Set font and size
            name_rect = name_label.boundingRect()
            name_label.setPos(element.rect().center().x() - name_rect.width() / 2,
                               element.rect().bottom() + 2)  # Adjust the vertical position
            element.name_label = name_label  # Store the label in the element for later reference
            
            
    def mousePressEvent(self, event):
        try:
            item = self.itemAt(event.pos())
            if item and isinstance(item, Element):
                # Create a copy of the selected element and add it to the main canvas
                copied_element = item.clone()
                copied_element.setPos(50, 50)  # Set a default position for the copied element
                # Hide the name label for the copied element
                for child_item in copied_element.childItems():
                    if isinstance(child_item, QtWidgets.QGraphicsTextItem):
                        child_item.hide()
                self.canvas.scene().addItem(copied_element)
        except Exception as e:
            print(f"Exception in mousePressEvent: {e}")

class Canvas(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        element = Element(mime_data.text(), QtCore.QRectF(0, 0, 50, 20), QtGui.QColor("blue"))
        element.setPos(self.mapToScene(event.pos()))  # Use mapToScene to get the correct position
        self.scene().addItem(element)
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            selected_items = self.scene().selectedItems()
            for item in selected_items:
                if isinstance(item, Element):
                    self.scene().removeItem(item)
                elif isinstance(item, Wire):
                    self.scene().removeItem(item)
                else:
                    super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, canvas, parent=None):
        super(MainWindow, self).__init__(parent)

        self.sidebar = Sidebar(canvas)
        self.canvas = canvas

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.canvas)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

def main():
    app = QtWidgets.QApplication([])
    canvas = Canvas()
    window = MainWindow(canvas)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()