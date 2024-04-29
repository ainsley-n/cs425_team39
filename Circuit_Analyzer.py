# Import needed files for analysis
from Analysis_Methods.mesh_analysis import perform_mesh_analysis
from Analysis_Methods.nodal_analysis import perform_nodal_analysis
from Analysis_Methods.state_analysis import perform_state_space_analysis
from Analysis_Methods.plot_analysis import perform_plot_analysis
from Analysis_Methods.beginner_analysis import perform_beginner_analysis

#image Conversion
from Extra_Methods.ImageConverter import latex_to_png
from Extra_Methods.NetlistConverter import remove_component_value

# Lcapy Implementation
from lcapy import *
from numpy import logspace

from lcapy import state; state.current_sign_convention = 'passive'

units = {
    'v': 'V',
    'i': 'A',
    'r': 'R',
    'c': 'G'
}

# Import an existing netlist 
def create_circuit_from_file(file_path):
    with open(file_path, 'r') as file:
        netlist = file.read()

    circuit = Circuit(netlist)
    return circuit

def request_component_property(circuit):
    # Draw circuit 
    circuit.draw()

    # Print Netlist
    print(circuit.netlist())
    componentName = input("Enter the name of the component you want to solve for: ")
    componentProperty = input("Enter i or v for current or voltage: ")
    # Access component property dynamically
    value = get_component_property(circuit, componentName, componentProperty)
    value.pprint()

def get_component_property(circuit, componentName, componentProperty):
    # Print the netlist
    # print(circuit.netlist())
    # Access component property dynamically
    try:
        if (componentProperty == 'v'):
            return circuit[componentName].V(t)
        elif (componentProperty == 'i'):
            return circuit[componentName].I(t)
    except KeyError:
        print(f"Error: Component '{componentName}' not found.")
    except AttributeError:
        print(f"Error: Property '{componentProperty}' not found for component '{componentName}'.")

def request_node_property(circuit):
    # Draw circuit
    circuit.draw()
    # Print Netlist
    print(circuit.netlist())

    nodeIndex = input("Give the number of the node: ")
    print(nodeIndex)
    property = input("Give the desired property as v or i: ")
    print(property)
    value = get_node_property(circuit, nodeIndex, property)
    value.pprint()
    
def get_node_property(circuit, nodeIndex, property):
    if property == 'v' or 'V':
        return circuit[nodeIndex].v
    else:
        return circuit[nodeIndex].i

# Dictionary for analysis by ainsley because this looks nicer and makes more sense
analysis_functions = {
    'Draw circuit': lambda c: c.draw(),
    'Mesh analysis': lambda c,f=None: perform_mesh_analysis(c,f),
    'Nodal analysis': lambda c,f=None: perform_nodal_analysis(c,f),
    'Description': lambda c: c.description(),
    'Thevenin Analysis': lambda c,f=None,e=None,start=None,end=None: perform_thevenin_analysis(c,f,e,start,end),
    'Norton Analysis': lambda c,f=None,e=None,start=None,end=None: perform_norton_analysis(c,f,e,start,end),
    'Thevenin-Norton Transformation': lambda c,f=None: perform_thevenin_transformation(c,f),
    'Norton-Thevenin Transformation': lambda c,f=None: perform_norton_transformation(c,f),
    'State Space Analysis': lambda c: perform_state_space_analysis(c),
    'For Beginners': lambda f=None: perform_beginner_analysis(f),
    'Plotting': lambda c: perform_plot_analysis(),
    'Component Property': lambda c: request_component_property(c),
    'Node Property': lambda c: request_node_property(c),
    # Add more analysis types as needed
}

# Call the desired analysis and handle invalid types
def perform_analysis(circuit, analysis_type, result_filename=None, *args, **kwargs):
    
    analysis_function = analysis_functions.get(analysis_type)
    
    if analysis_function:
        if result_filename:
            return analysis_function(circuit, result_filename, *args, **kwargs)
        else:
            return analysis_function(circuit, *args, **kwargs)
    else:
        print("Invalid analysis type. Please choose a valid analysis type.")
        raise ValueError(f"Invalid analysis type: {analysis_type}")

 
# State Space Analysis moved to separate file

# Thevenin Analysis of a linear subcircuit with user defined nodes
def perform_thevenin_analysis(circuit, simplified_circuit_filename=None, equation_filename=None, startNode=None, endNode=None):
    print("This analysis is used to find Thevenin equivalent values between a starting and an end node of a circuit.")
    # Get no value circuit
    empty_circuit_netlist = remove_component_value(circuit.netlist())
    empty_circuit = Circuit(empty_circuit_netlist)
    
    # Take input for start and end node
    if startNode is None:
        startNode = input("Input start node as number: ")
    if endNode is None:
        endNode = input("Input end node as number: ")
    thevenin = circuit.thevenin(startNode, endNode)
    thevenin_empty = empty_circuit.thevenin(startNode, endNode)
    
    # Draw evaluated thevenin network
    thevenin.draw(simplified_circuit_filename)
      
    # Generate LaTeX and PNG image of unevaluated thevenin equations
    s = thevenin_empty.latex()
    # The output of the system where G is representative of Conductance and I is representitive of the current source.
    if equation_filename is None:
        equation_filename = 'temp/thevenin_equations.png'
    return latex_to_png(s, equation_filename), thevenin
    

# Norton Analysis of a linear subcircuit with user defined nodes
def perform_norton_analysis(circuit, simplified_circuit_filename=None, equation_filename=None, startNode=None, endNode=None):
    print("This analysis is used to find Norton equivalent values between a starting and an end node of a circuit.")
    # Get no value circuit
    empty_circuit_netlist = remove_component_value(circuit.netlist())
    empty_circuit = Circuit(empty_circuit_netlist)

    # Take input for start and end node
    if startNode is None:
        startNode = input("Input start node as number: ")
    if endNode is None:
        endNode = input("Input end node as number: ")
    norton = circuit.norton(startNode, endNode)
    norton_empty = empty_circuit.norton(startNode, endNode)

    norton.draw(simplified_circuit_filename)

    # Generate LaTeX and PNG image of unevaluated norton equations
    s = norton_empty.latex()
    # The output of the system where G is representative of Conductance and I is representitive of the current source.
    if equation_filename is None:
        equation_filename = 'temp/norton_equations.png'
    return latex_to_png(s, equation_filename), norton

# Thevenin Transformation to norton equivalent using user defined voltage and resistance
def perform_thevenin_transformation(circuit, png_filename=None):
    print("This function transforms a given Thevenin circuit to its Norton equivalent.")
    
    # Take input for volatge and resistance
    v = input("Input voltage as number: ")
    r = input("Input resistance as number: ")
    T = Vdc(v) + R(r)
    n = T.norton()
    print("These are the new values and drawing for your Norton equivalent circuit.")
    n.pprint()
    n.draw()
    
    # Generate LaTeX and PNG image of norton equations
    s = n.latex()
    # The output of the system where G is representative of Conductance and I is representitive of the current source.

    latex_to_png(s, png_filename)


# Norton Transformation to thevenin equivalent using user defined current and resistance
def perform_norton_transformation(circuit, png_filename=None):
    print("This function transforms a given Norton circuit to its Thevenin equivalent.")
    # Take input for volatge and resistance
    i = input("Input current as number: ")
    r = input("Input resistance as number: ")
    n = Idc(i) | R(r)
    T = n.thevenin()
    print("These are the new values and drawing for your Thevenin equivalent circuit.")
    T.pprint()
    T.draw()

    # Generate LaTeX and PNG image of thevenin equations
    s = T.latex()
    # The output of the system where R is representative of Resistance and V is representitive of the volatge source.

    latex_to_png(s, png_filename)

# Import netlist with pre-defined file path
# file_path = 'D:/Circuit_Analyzer/testing/circuit.net'
# circuit = create_circuit_from_file(file_path)

# Main example circuit: Mesh, Nodal, Loop, Thevenin, Norton
# circuit = Circuit("""
# V1 1 0; down
# R1 1 2; right
# L1 2 3; right
# R2 3 4; right
# L2 2 0_2; down
# C2 3 0_3; down
# R3 4 0_4; down
# W 0 0_2; right
# W 0_2 0_3; right
# W 0_3 0_4; right""")

# Thevenin example circuit, nodes 2 & 0
# circuit = Circuit("""
# ...V1 1 0 V; down
# ...R1 1 2 R; right
# ...C1 2 0_2 C; down
# ...W 0 0_2; right""")

# State-Space example
# circuit = Circuit("""
# V 1 0 {v(t)}; down
# R1 1 2; right
# L 2 3; right=1.5, i={i_L}
# R2 3 0_3; down=1.5, i={i_{R2}}, v={v_{R2}}
# W 0 0_3; right
# W 3 3_a; right
# C 3_a 0_4; down, i={i_C}, v={v_C}
# W 0_3 0_4; right""")

# Display use-cases example
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

# Loop analysis example 
# circuit = Circuit("""
# V1 1 0 {u(t)}; down
# R1 1 2; right=2
# L1 2 3; down=2
# W1 0 3; right
# W 1 5; up
# W 2 6; up
# C1 5 6; right=2""")

# DC volt divider for beginners
circuit = Circuit("""
V 1 0 6; down=1.5
R1 1 2 2; right=1.5
R2 2 0_2 4; down
W 0 0_2; right""")

# Menu for analysis options
def display_menu():
    print("\n\nAvailable analysis types:")
    analysis_options = {
        '1': 'Draw circuit',
        '2': 'Mesh analysis',
        '3': 'Nodal analysis',
        '4': 'Description',
        '5': 'Thevenin Analysis',
        '6': 'Norton Analysis',
        '7': 'Thevenin-Norton Transformation',
        '8': 'Norton-Thevenin Transformation',
        '9': 'State Space Analysis',
        '10': 'For Beginners',
        '11': 'Plotting',
        '12': 'Component Property',
        '13': 'Node Property',
        '0': 'Exit'
    }

    for key, value in analysis_options.items():
        print(f"{key}. {value}")

    return analysis_options

#Modified to prevent running CLI when importing into another python script
if __name__ == "__main__":

    # Modified the user menu to make more sense in python
    while True:
        # Display the menu and get user input
        analysis_options = display_menu()
        analysis_choice = input("Choose the analysis type (enter the corresponding number, 0 to exit): ")
        if analysis_choice == '0':
            print("Exiting the program. Goodbye!\n")
            break

        # Check for user input error
        if analysis_choice in analysis_options.keys():
            print('\n\n')
            perform_analysis(circuit, analysis_options[analysis_choice])
        else:
            print("Invalid input. Please enter a valid analysis number.")
