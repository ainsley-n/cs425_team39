# Lcapy Implementation
from lcapy import *

from lcapy import state; state.current_sign_convention = 'passive'

def create_circuit_from_file(file_path):
    with open(file_path, 'r') as file:
        netlist = file.read()

    circuit = Circuit(netlist)
    return circuit

def perform_analysis(circuit, analysis_type):
    if analysis_type == 'draw':
        circuit.draw()
    elif analysis_type == 'freq_response':
        circuit.plot_freq_response()
    elif analysis_type == 'mesh':
        perform_mesh_analysis(circuit)
    elif analysis_type == 'nodal':
        perform_nodal_analysis(circuit)
    elif analysis_type == 'thevenin':
        perform_thevenin_analysis(circuit)
    elif analysis_type == 'norton':
        perform_norton_analysis(circuit)
    elif analysis_type == 'theveninTrans':
        perform_thevenin_transformation(circuit)
    elif analysis_type == 'nortonTrans':
        perform_norton_transformation(circuit)
    elif analysis_type == 'state_space':
        perform_state_space_analysis(circuit)
    # Add more analysis types as needed

def perform_mesh_analysis(circuit):
    l = circuit.mesh_analysis()
    print(l.mesh_equations())
    # S domain
    l = circuit.laplace().mesh_analysis()
    print(l.mesh_equations())

def perform_nodal_analysis(circuit):
    l = circuit.mesh_analysis()
    l.mesh_equations()
    # S domain
    l = circuit.laplace().mesh_analysis()
    l.mesh_equations()

def perform_state_space_analysis(circuit):
    ss = circuit.ss
    ss.state_equations().pprint()

def perform_thevenin_analysis(circuit):
    # Take input for start and end node
    startNode = input("Input start node as number: ")
    endNode = input("Input end node as number: ")
    thevenin = circuit.thevenin(startNode, endNode)
    thevenin.pprint()

def perform_norton_analysis(circuit):
    # Take input for start and end node
    startNode = input("Input start node as number: ")
    endNode = input("Input end node as number: ")
    norton = circuit.norton(startNode, endNode)
    norton.pprint()

def perform_thevenin_transformation(circuit):
    # Take input for volatge and resistance
    v = input("Input voltage as number: ")
    r = input("Input resistance as number: ")
    T = Vdc(v) + R(r)
    n = T.norton()
    n.pprint()

def perform_norton_transformation(circuit):
    # Take input for volatge and resistance
    i = input("Input current as number: ")
    r = input("Input resistance as number: ")
    n = Idc(i) | R(r)
    T = n.thevenin()
    T.pprint()

# Example usage
# file_path = 'D:/Circuit_Analyzer/testing/circuit.net'
# circuit = create_circuit_from_file(file_path)

# main example circuit
'''circuit = Circuit("""
...V1 1 0; down
...R1 1 2; right
...L1 2 3; right
...R2 3 4; right
...L2 2 0_2; down
...C2 3 0_3; down
...R3 4 0_4; down
...W 0 0_2; right
...W 0_2 0_3; right
...W 0_3 0_4; right""")'''

# thevenin example circuit, nodes 2 & 0
'''circuit = Circuit("""
...V1 1 0 V; down
...R1 1 2 R; right
...C1 2 0_2 C; down
...W 0 0_2; right""")'''

# state-space example
'''circuit = Circuit("""
V 1 0 {v(t)}; down
R1 1 2; right
L 2 3; right=1.5, i={i_L}
R2 3 0_3; down=1.5, i={i_{R2}}, v={v_{R2}}
W 0 0_3; right
W 3 3_a; right
C 3_a 0_4; down, i={i_C}, v={v_C}
W 0_3 0_4; right""")'''

# example for display use-cases below
'''circuit = Circuit("""
V_s fred 0
R_a fred 1
R_b 1 0""")'''
# Display branch voltages or current circuit.componentName.property.pprint()
# circuit.V_s.V.pprint()
# circuit.R_a.I.pprint()
# Display node voltages using name or index circuit.componentName.property.pprint() or circuit[index].property.pprint()
# circuit['fred'].V.pprint()
# circuit[1].V.pprint()


# Display analysis options to the user
print("Available analysis types:")
print("1. Draw circuit")
print("2. Frequency response")
print("3. Mesh analysis")
print("4. Nodal analysis")
print("5. Description")
print("6. Thevenin Analysis")
print("7. norton")
print("8. Thevenin-Norton Transformation")
print("9. Norton-Thevenin Transformation")
print("10. state_space")

# Get user input for analysis type
analysis_choice = input("Choose the analysis type (enter the corresponding number): ")

# Perform the selected analysis
if analysis_choice == '1':
    perform_analysis(circuit, 'draw')
elif analysis_choice == '2':
    perform_analysis(circuit, 'freq_response')
elif analysis_choice == '3':
    perform_analysis(circuit, 'mesh')
elif analysis_choice == '4':
    perform_analysis(circuit, 'nodal')
elif analysis_choice == '5':
    circuit.describe()
elif analysis_choice == '6':
    perform_analysis(circuit, 'thevenin')
elif analysis_choice == '7':
    perform_analysis(circuit, 'norton')
elif analysis_choice == '8':
    perform_analysis(circuit, 'theveninTrans')
elif analysis_choice == '9':
    perform_analysis(circuit, 'nortonTrans')
elif analysis_choice == '10':
    perform_analysis(circuit, 'state_space')
# Add more conditions for additional analysis types

# Note: You may want to add error handling for invalid user input

# Documentation 
# Step 1 Store circuit, 2 variation have subtle differences in equation output
    
    # Nelist Specification, advantage in use of component names
 
    # Componenet Combination, requires specific nodes to determine voltage

# Step 2 Solution Algorithm, call describe() on the circuit to see what analysis is used
''' 1 If a capacitor or inductor is found to have initial conditions,
    then the circuit is analysed as an initial value problem using Laplace methods.
    In this case, the sources are ignored for t < 0 and the result is only known for t > 0'''

''' 2 If there are no capacitors and inductors and if none of the independent sources
    are specified in the Laplace domain, then time-domain analysis is performed 
    (since no derivatives or integrals are required).'''

''' 3 Finally, Lcapy tries to decompose the sources into DC, AC, transient, and noise components.
    The circuit is analysed for each source category using the appropriate transform domain 
    (phasors for AC, Laplace domain for transients) and the results are added. If there are multiple noise sources, 
    these are considered independently since they are assumed to be uncorrelated.'''


# Switches
''' Lcapy can solve circuits with switches by converting them to an initial value problem (IVP) with the convert_IVP() method.
    This has a time argument that is used to determine the states of the switches. The circuit is solved prior to the moment when the last switch activates
    and this is used to provide initial values for the moment when the last switch activates. If there are multiple switches with different activation times, 
    the initial values are evaluated recursively.'''

# Circuit Graph
''' Both NodalAnalysis and LoopAnalysis use CircuitGraph to represent a netlist as a graph. This can be interrogated to find loops, etc.'''
