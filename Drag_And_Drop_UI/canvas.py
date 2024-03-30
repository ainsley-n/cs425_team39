from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
from elements import Element, CircularElement
from voltageSource import VoltageSource
from resistorSource import Resistor
from capacitorSource import Capacitor
from inductorSource import Inductor
from wire import Wire

class Canvas(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        
        # Add a button to save the order
        self.save_button = QtWidgets.QPushButton("Save Order", self)
        self.save_button.clicked.connect(self.save_order)
        self.save_button.setGeometry(10, 10, 100, 30)
        
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            selected_items = self.scene().selectedItems()
            for item in selected_items:
                if isinstance(item, Element):
                    if isinstance(item, VoltageSource):
                        item.deleteVoltageSource()
                    elif isinstance(item, Resistor):
                        item.deleteResistor()
                    elif isinstance(item, Capacitor):
                        item.deleteCapacitor()
                    elif isinstance(item, Inductor):
                        item.deleteInductor()
                    self.scene().removeItem(item)
                elif isinstance(item, Wire):
                    self.scene().removeItem(item)
                elif isinstance(item, CircularElement):
                    item.deleteNode()
                    self.scene().removeItem(item)
                    self.checkNumNodesOnCanvas()
                else:
                    super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)
        
    def save_order(self):
        # Get the order of elements in the scene
        elements = self.scene().items()

        # Create a dictionary to store information about each element and its connections
        elements_info = {}

        for element in elements:
            if isinstance(element, (Element, VoltageSource, Resistor, Capacitor, Inductor, CircularElement)):
                if isinstance(element, (VoltageSource, Resistor, Capacitor, Inductor, CircularElement)):
                    name_label_text = element.name_label.toPlainText()
                else:
                    name_label_text = element.name
                    
                # Calculate the position relative to the canvas
                canvas_pos = element.mapToScene(element.pos())

                # Get the x and y coordinates of the position
                canvas_x = canvas_pos.x()
                canvas_y = canvas_pos.y()

                element_info = {
                    'name': name_label_text,
                    'pos': (canvas_x, canvas_y),
                    'connections': [],
                    'values': element.get_value()
                }
                # print(f'name: {element_info["name"]}, {element_info["pos"]}, {element_info["connections"]}')

                # Check if the element has connected wires
                for node in element.nodes:
                    # print('checking node in element.nodes')
                    for wire in node.connected_wires():
                        # print('in wire for node.conected_wire')
                        other_node = wire.start_node if wire.end_node == node else wire.end_node
                        other_element = other_node.parentItem()
                        connection_info = {
                            'other_element_name': other_element.name_label.toPlainText(),
                            'direction': 'right' if wire.line().dx() > 0 else 'left' if wire.line().dx() < 0 else 'down' if wire.line().dy() > 0 else 'up'
                        }
                        element_info['connections'].append(connection_info)
                print(f'name: {element_info["name"]}, {element_info["pos"]}, {element_info["connections"]}')
                elements_info[name_label_text] = element_info
                ##########################################################################################################################
                ##########################################################################################################################
                ##########HERE I AM STRUGGLING BECAUSE THE LOGIC TO FINDING THE DIRECTION ISNT CORRECT####################################
                ##########MAYBE THINK OF DESIGNATING A POSITIVE AND NEGATIVE NODE TO VOLTAGE##############################################
        
        # Save the order and connection information to a .txt file
        # file_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Order', '', 'Text Files (*.txt);;All Files (*)')[0]
        # if file_path:
        #     with open(file_path, 'w') as file:
        
        for element_name, element_info in elements_info.items():
            if element_info['name'].isdigit():
                continue
            name = element_info['name']
            value = element_info['values']
            print(f"{name}", end="")
            for connection in element_info['connections']:
                print(f" {connection['other_element_name']}", end="")
            # print(f' {value}')
            if value is not None:     
                if value != 0:#i am struggling here
                # print(f'active here')
                    print(f' {value}', end="")              #it is only printing the value when there is a print statement
                # print(f'active here')
            print(f"; {connection['direction']}")     #it should be printing the values of the voltage thingy next to the nodes its connected to
            
        # check if circular elements are next to eachother    
        circular_elements = [element for element in elements if isinstance(element, CircularElement)]
        printed_circular_connections  = set()
        
        for circular_element in circular_elements:
            connected_circular_elements = []
            name = circular_element.name_label.toPlainText()
            # print(f"Checking connections for circular element {name}:")
            for node in circular_element.nodes:
                for wire in node.connected_wires():
                    other_node = wire.start_node if wire.end_node == node else wire.end_node
                    other_element = other_node.parentItem()
                    if isinstance(other_element, CircularElement):
                        connected_circular_elements.append(other_element)
            # print(f"Found {len(connected_circular_elements)} connected circular elements.")
            if connected_circular_elements:
                for connected_element in connected_circular_elements:
                    # Sort the circular element names to ensure consistency
                    circular_connection = tuple(sorted([name, connected_element.name_label.toPlainText()]))
                    # Check if the circular connection has already been printed
                    if circular_connection not in printed_circular_connections:
                        direction = connection['direction']  # Assign direction based on the current connection
                        if connected_circular_elements[0].name_label.toPlainText() == '0':
                            # print(f'{name} is connected to 0')
                            print(f'W 0_{name} 0; {direction}')
                        elif name == '0':
                            # print(f'0 is connected to {connected_circular_elements[0].name_label.toPlainText()}')
                            print(f'W 0 0_{connected_circular_elements[0].name_label.toPlainText()}; {direction}')
                        else:
                            print(f'{name} is connected to {connected_circular_elements[0].name_label.toPlainText()}')
                        # Add the circular connection to the set of printed connections
                        printed_circular_connections.add(circular_connection)
            elif len(connected_circular_elements) > 2:
                print(f"Error: More than three nodes connected together.")

    # def access_voltage_source_label(self, voltage_source_name):
    #     for item in self.scene().items():
    #         if isinstance(item, VoltageSource) and item.name == voltage_source_name:
    #             return item.name_label
    #     return None

    def checkNumNodesOnCanvas(self):
        num_nodes = sum(1 for item in self.scene().items() if isinstance(item, CircularElement))
        # print(f"Number of CircleNodeElements on the canvas: {num_nodes}")
        if num_nodes == 0:
            CircularElement.deleted_node_labels.clear()
            # print('we have no more nodes')
            
            # Clear the set of deleted_node_labels
            CircularElement.label_number = 0
