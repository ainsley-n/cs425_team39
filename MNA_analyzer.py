import numpy as np
import subprocess

np.set_printoptions(precision=3, suppress=True)

# circuit component structure
class Component:  
    def __init__(self, comp_type, high_str, low_str, value):
        # component type
        self.comp_type = comp_type
        # nodes as strings
        self.high_str = high_str
        self.low_str = low_str
        # mapped nodes
        self.high = -1
        self.low = -1
        # component value
        self.value = value

    def __repr__(self):
        return str(self.comp_type) + " " + str(self.high) + " " + str(self.low) + " " + str(self.value)

# nodes hash table
class NodeHashtable:  
    def __init__(self):
        self.nodes = {}
        self.nodeCount = 0

    def addToNodes(self, node_str):
        # check if node not already added
        if node_str not in self.nodes:
            self.nodes[node_str] = self.nodeCount
            self.nodeCount = self.nodeCount + 1
        return self.nodes[node_str]

    def __del__(self):
        del self.nodes

# Parse file and return componets
def parseFile(fileName):
    # open file for reading
    file = open(fileName, "r")

    # use global scope variables for component counts
    global voltageCount, currentCount, resistorCount, capacitorCount, inductorCount

    # component list
    components = []

    # read netlist
    for line in file:
        # split line
        parts = line.split()

        # add component to list
        components.append(
            Component(parts[0][0].upper(), parts[1].upper(), parts[2].upper(), float(parts[3])))

        # update component counts
        if parts[0][0] == 'V':
            voltageCount = voltageCount + 1
        elif parts[0][0] == 'I':
            currentCount = currentCount + 1
        elif parts[0][0] == 'R':
            resistorCount = resistorCount + 1
        elif parts[0][0] == 'C':
            capacitorCount = capacitorCount + 1
        elif parts[0][0] == 'L':
            inductorCount = inductorCount + 1

    # return components
    return components

# Add components to hashtable
def mapNodes(components):
    # create hashtable
    hashtable = NodeHashtable()

    # add '0' node
    hashtable.addToNodes('0')

    # for all components
    for component in components:
        component.high = hashtable.addToNodes(component.high_str)
        component.low = hashtable.addToNodes(component.low_str)

    return components, hashtable


def calculateMatrices(components, nodeCount):

    # use global scope variables for component counts
    global voltageCount, inductorCount

    # calculate g2 components
    g2Count = voltageCount + inductorCount
    print("Group 2 count:", g2Count)

    # calculate matrix size
    matrixSize = nodeCount + g2Count - 1
    print("Matrix size:", matrixSize, "\n")

    # define Matrices
    A = np.zeros((matrixSize, matrixSize))
    b = np.zeros(matrixSize)

    # Group 2 component index
    g2Index = matrixSize - g2Count

    # loop through all components
    for component in components:
        # store component info in temporary variable
        high = component.high
        low = component.low
        value = component.value

        if component.comp_type == 'R':
            # affects G-matrix of A
            # diagonal self-conductance of node
            if high != 0:
                A[high - 1][high - 1] = A[high - 1][high - 1] + 1/value
            if low != 0:
                A[low - 1][low - 1] = A[low - 1][low - 1] + 1/value

            # mutual conductance between nodes
            if high != 0 and low != 0:
                A[high - 1][low - 1] = A[high - 1][low - 1] - 1/value
                A[low - 1][high - 1] = A[low - 1][high - 1] - 1/value
        
        # elif component.comp_type == 'C':
            # Capacitance is an open circuit for Static Analysis

        elif component.comp_type == 'L':
            # closed circuit  in Static Analysis: 0 resistance and 0 voltage
            # affects the B and C matrices of A
            if high != 0:
                A[high - 1][g2Index] = A[high - 1][g2Index] + 1
                A[g2Index][high - 1] = A[g2Index][high - 1] + 1
            if low != 0:
                A[low - 1][g2Index] = A[low - 1][g2Index] - 1
                A[g2Index][low - 1] = A[g2Index][low - 1] - 1

            # affects b-matrix
            b[g2Index] = 0

            # increase G2 index
            g2Index = g2Index + 1

        elif component.comp_type == 'V':
            # affects the B and C matrices of A
            if high != 0:
                A[high - 1][g2Index] = A[high - 1][g2Index] + 1
                A[g2Index][high - 1] = A[g2Index][high - 1] + 1
            if low != 0:
                A[low - 1][g2Index] = A[low - 1][g2Index] - 1
                A[g2Index][low - 1] = A[g2Index][low - 1] - 1

            # affects b-matrix
            b[g2Index] = value

            # increase G2 counter
            g2Index = g2Index + 1

        elif component.comp_type == 'I':
            # affects b-matrix
            if high != 0:
                b[high - 1] = b[high - 1] - value
            if low != 0:
                b[low - 1] = b[low - 1] + value

    return A, b


def solveSystem(A, b):
    x = np.linalg.solve(A, b)
    return x

# Generate netlist
def generateLTspiceNetlist(components, filename="circuit.net"):
    # Write LTspice netlist format based on your component information
    # Ensure that the netlist follows LTspice syntax

    with open(filename, "w") as file:
        # Write component information to the file
        for component in components:
            file.write(f"{component.comp_type} {component.high} {component.low} {component.value}\n")


# Invoke LTspice
def runLTspice(filename="circuit.net"):
    ltspice_command = '"C:/Program Files/ADI/LTspice/LTspice.exe" -b -Run ' + filename
    subprocess.run(ltspice_command, shell=True)

# MAIN FUNCTION

# Initialize component counters
voltageCount = 0
currentCount = 0
resistorCount = 0
capacitorCount = 0
inductorCount = 0

# Parse File
fileName = "d:/Circuit_Analyzer/testing/circuit1.spice"
print("Parsing file...\n")
components = parseFile(fileName)

# Map nodes
print("Mapping nodes...\n")
components, hashtable = mapNodes(components)

# Generate LTspice netlist
# ltspice_filename = "d:/Circuit_Analyzer/testing/circuit.net"
# generateLTspiceNetlist(components, ltspice_filename)

# After mapping nodes
print("Node Mapping:")
for key, val in hashtable.nodes.items():
    print(f"Node \"{key}\": {val}")

# Circuit Summary
print("\nCircuit Summary:")
print(f"Total Components: {len(components)}")
print(f"Total Nodes: {hashtable.nodeCount}")
print(f"Component Counts - Voltage: {voltageCount}, Current: {currentCount}, Resistor: {resistorCount}, Capacitor: {capacitorCount}, Inductor: {inductorCount}")

# Component Details
print("\nCircuit Components:")
for i, component in enumerate(components):
    print(f"Component {i + 1}: Type: {component.comp_type}, Value: {component.value}, High Node: {component.high}, Low Node: {component.low}")

# Calculate and solve system
print("\nCalculating MNA Matrices...\n")
A, b = calculateMatrices(components, hashtable.nodeCount)
print("A:\n", A)
print("b:\n", b)

print("\nSolving System...\n")
x = solveSystem(A, b)
print("x:\n", x)

# After solving the system
print("\nchat display test 2")
print("\nNode Voltages:")
for i, voltage in enumerate(x[:hashtable.nodeCount]):
    print(f"Node {i + 1}: Voltage = {voltage:.4f} V")

# Currents through Components
print("\nCurrents through Components:")
for i, component in enumerate(components):
    if component.comp_type == 'R':
        current = (x[component.high - 1] - x[component.low - 1]) / component.value
        print(f"Resistor {i + 1}: Current = {current:.4f} A")

# Power Dissipation in Resistors
print("\nPower Dissipation in Resistors:")
for i, component in enumerate(components):
    if component.comp_type == 'R':
        current = (x[component.high - 1] - x[component.low - 1]) / component.value
        power = current**2 * component.value
        print(f"Resistor {i + 1}: Power = {power:.4f} W")
