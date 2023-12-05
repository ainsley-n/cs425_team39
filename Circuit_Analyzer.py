#import needed files for analysis
from mesh_analysis import perform_mesh_analysis

# Lcapy Implementation
from lcapy import *
from numpy import logspace

from lcapy import state; state.current_sign_convention = 'passive'

# Import an existing netlist 
def create_circuit_from_file(file_path):
    with open(file_path, 'r') as file:
        netlist = file.read()

    circuit = Circuit(netlist)
    return circuit

#dictionary for analysis by ainsley because this looks nicer and makes more sense
analysis_functions = {
    'Draw circuit': lambda c: c.draw(),
    
    #do we really need this one??|
        #                        v   
    'Frequency response': lambda c: c.plot_freq_response(),
    #????????????????????????????????
    
    #i am going to improve 
    'Mesh analysis': lambda c: perform_mesh_analysis(c),
    'Nodal analysis': lambda c: perform_nodal_analysis(c),
    #these to be more complete 
    
    
    'Description': lambda c: c.describe(),
    'Thevenin Analysis': lambda c: perform_thevenin_analysis(c),
    'Norton Analysis': lambda c: perform_norton_analysis(c),
    'Thevenin-Norton Transformation': lambda c: perform_thevenin_transformation(c),
    'Norton-Thevenin Transformation': lambda c: perform_norton_transformation(c),
    'State Space Analysis': lambda c: perform_state_space_analysis(c),
    'Loop Analysis': lambda c: perform_loop_analysis(c),
    'For Beginners': lambda c: perform_beginner_analysis(),
    'Plotting': lambda c: perform_plot_analysis(),
    # Add more analysis types as needed
}

# Call the desired analysis and handle invalid types
def perform_analysis(circuit, analysis_type):
    
    analysis_function = analysis_functions.get(analysis_type)
    
    if analysis_function:
        analysis_function(circuit)
    else:
        print("Invalid analysis type. Please choose a valid analysis type.")

        
#nodal analysis equations done by ainsley
def perform_nodal_analysis(circuit):
    #time domain
    nodal_result = circuit.nodal_analysis()
    nodal_equations = nodal_result.nodal_equations()

    print("Nodal Equations (Time Domain):")
    #print equations line by line
    for node, equation in nodal_equations.items():
        print(f"V_{node}: {equation}")

    #Laplace domain
    laplace_result = circuit.laplace().nodal_analysis()
    laplace_nodal_equations = laplace_result.nodal_equations()

    print("\nNodal Equations (Laplace Domain):")
    #print Laplace domain equations line by line
    for node, equation in laplace_nodal_equations.items():
        print(f"V_{node}(s): {equation}")


# State Space Analysis
def perform_state_space_analysis(circuit):
    ss = circuit.ss
    ss.state_equations().pprint()

# Thevenin Analysis of a linear subcircuit with user defined nodes
def perform_thevenin_analysis(circuit):
    # Take input for start and end node
    startNode = input("Input start node as number: ")
    endNode = input("Input end node as number: ")
    thevenin = circuit.thevenin(startNode, endNode)
    thevenin.pprint()

# Norton Analysis of a linear subcircuit with user defined nodes
def perform_norton_analysis(circuit):
    # Take input for start and end node
    startNode = input("Input start node as number: ")
    endNode = input("Input end node as number: ")
    norton = circuit.norton(startNode, endNode)
    norton.pprint()

# Thevenin Transformation to norton equivalent using user defined voltage and resistance
def perform_thevenin_transformation(circuit):
    # Take input for volatge and resistance
    v = input("Input voltage as number: ")
    r = input("Input resistance as number: ")
    T = Vdc(v) + R(r)
    n = T.norton()
    n.pprint()

# Norton Transformation to thevenin equivalent using user defined current and resistance
def perform_norton_transformation(circuit):
    # Take input for volatge and resistance
    i = input("Input current as number: ")
    r = input("Input resistance as number: ")
    n = Idc(i) | R(r)
    T = n.thevenin()
    T.pprint()

# Loop Analysis best used for showing equations: Loop, KVL, Mesh
def perform_loop_analysis(circuit):
    # Loop analysis in time domain
    la = LoopAnalysis(circuit)

    # Display KVL equations around each mesh
    la.mesh_equations().pprint()

    # Display system of equations in matrix form
    # la.matrix_equations().pprint()
    # Need to convert from time domain to dc, ac, or laplace
    LoopAnalysis(circuit.laplace()).matrix_equations().pprint()
    
# Beginner Analysis for introducing new users
def perform_beginner_analysis():
    # DC volt divider for beginners
    circuit = Circuit("""
    V 1 0 6; down=1.5
    R1 1 2 2; right=1.5
    R2 2 0_2 4; down
    W 0 0_2; right""")
    print(" * Circuit has been replaced for demonstartion.")
    
    # Draw circuit for user
    print("Circuits given as netlists can be analyzed and drawn.")
    circuit.draw()

    # Display voltage at noode 1
    print("Node voltages can be displayed given the node. This is the voltage at node 1.")
    circuit[1].v.pprint()
    # Display voltage at node 2
    print("This is the voltage at node 2.")
    circuit[1].v.pprint()

    # Display voltage accross each component
    print("Component voltages can be displayed given the component name. This is the voltage at the voltage source.")
    circuit.V.v.pprint()
    print("This is the voltage at resistor 1.")
    circuit.R1.v.pprint()
    print("This is the voltage at resistor 2.")
    circuit.R2.v.pprint()

    # Display current accross each component
    print("Component current can be displayed given the component name. This is the current at the voltage source.")
    circuit.V.i.pprint()
    print("This is the current at resistor 1.")
    circuit.R1.i.pprint()
    print("This is the current at resistor 2.")
    circuit.R2.i.pprint()

    # Display AC circuit 
    print("AC circuits can also be analyzed and drawn")
    circuit = Circuit("""
    V 1 0 ac 6; down=1.5
    R 1 2 2; right=1.5
    C 2 0_2 4; down
    W 0 0_2; right""")
    circuit.draw()

    print("AC components can be displayed the same as DC components. This is the voltage at the voltage source.")
    circuit.V.v.pprint()

    print("This is the voltage at the resistor.")
    circuit.R.v.pprint()
    
    print("This is a simplifed version of the voltage at the resistor.")
    circuit.R.v.simplify_sin_cos().pprint()

    print("The voltage accross the resisitor can be plotted given a value for omega, w = 3.")
    circuit.R.v.subs(omega0, 3).plot((-1, 10))

    # Display circuit with voltage source that has a step change to show transient voltages
    print("Circuits with step changes in the voltage can also be analyzed and drawn.")
    circuit = Circuit("""
    V 1 0 step 6; down=1.5
    R 1 2 2; right=1.5
    C 2 0_2 4; down
    W 0 0_2; right""")
    circuit.draw()

    print("This is the transient voltage at the voltage source.")
    circuit.V.v

    print("This is the transient voltage at the resistor.")
    circuit.R.v

    print("This is the transient voltage at the capacitor.")
    circuit.C.v

    print("This is the plotted transient voltage across the resitor.")
    circuit.R.v.plot((-1, 10))

# Display diagrams of plotted data
def perform_plot_analysis():
    # Each domain has different behavior for plotting
    # Range of time values can be defined as a tuple

    print("Available plotting types:")
    print("1. Pole-Zero Plot")
    print("2. Frequency Domain Plot")
    print("3. Bode Plot")
    print("4. Nyquist Plot")
    print("5. Nichols Plot")
    print("6. Phasor Plot")
    print("7. Discrete-Time Plot")

    # Get user input for plot type
    plot_choice = input("Choose the analysis type (enter the corresponding number): ")

    # Perform the selected plot
    if plot_choice == '1':
        # Pole zero plot, laplace
        expr = input("Input your expression using the units s and j: ")
        transExpr = transfer(expr)
        # H = transfer((s - 2) * (s + 3) / (s * (s - 2 * j) * (s + 2 * j)))
        transExpr.plot()
        
    elif plot_choice == '2':
        # Frequency domain plot, fourier
        # Note, this has a marginally stable impulse response since it has a pole at s = 0.
        # Returns the axes used in the plot, returns tuple if multiple
        expr = input("Input your expression using the units s and j: ")
        transExpr = transfer(expr)
        # H = transfer((s - 2) * (s + 3) / (s * (s - 2 * j) * (s + 2 * j)))
        fv = logspace(-1, 3, 400)
        transExpr(j2pif).dB.plot(fv, log_scale=True)
        
    elif plot_choice == '3':
        # Bode plot
        # Plots magnitude and phase as a log freq
        expr = input("Input your expression using the unit s: ")
        # expr = 1 / (s**2 + 20*s + 10000)
        transExpr = transfer(expr)
        transExpr.bode_plot((1, 1000))
        
    elif plot_choice == '4':
        # Nyquist plot
        # Plots imaginary and real frequency response
        expr = input("Input your expression using the unit s: ")
        #expr = 10 * (s + 1) * (s + 2) / ((s - 3) * (s - 4))
        transExpr = transfer(expr)
        transExpr.nyquist_plot((-100, 100))
        
    elif plot_choice == '5':
        expr = input("Input your expression using the unit s: ")
        # expr = 10 * (s + 1) * (s + 2) / ((s - 3) * (s - 4))
        transExpr = transfer(expr)
        transExpr.nichols_plot((-100, 100))
        
    elif plot_choice == '6':
        expr = input("Input your expression using the unit j: ")
        #phasor(1 + j).plot()
        transExpr = transfer(expr)
        phasor(transExpr).plot()
        
    elif plot_choice == '7':
        expr = input("Input your expression using the unit n: ")
        # cos(2 * n * 0.2).plot()
        transExpr = transfer(expr)
        cos(transExpr).plot()

        expr = input("Input your complex expression using the unit n: ")
        # x = 0.9**n * exp(j * n * 0.5)
        transExpr = transfer(expr)
        transExpr.plot((1, 10), polar=True)

# Import netlist with pre-defined file path
# file_path = 'D:/Circuit_Analyzer/testing/circuit.net'
# circuit = create_circuit_from_file(file_path)

# Main example circuit: Mesh, Nodal, Loop, Thevenin, Norton
circuit = Circuit("""
V1 1 0; down
R1 1 2; right
L1 2 3; right
R2 3 4; right
L2 2 0_2; down
C2 3 0_3; down
R3 4 0_4; down
W 0 0_2; right
W 0_2 0_3; right
W 0_3 0_4; right""")

# Thevenin example circuit, nodes 2 & 0
'''circuit = Circuit("""
...V1 1 0 V; down
...R1 1 2 R; right
...C1 2 0_2 C; down
...W 0 0_2; right""")'''

# State-Space example
'''circuit = Circuit("""
V 1 0 {v(t)}; down
R1 1 2; right
L 2 3; right=1.5, i={i_L}
R2 3 0_3; down=1.5, i={i_{R2}}, v={v_{R2}}
W 0 0_3; right
W 3 3_a; right
C 3_a 0_4; down, i={i_C}, v={v_C}
W 0_3 0_4; right""")'''

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
'''circuit = Circuit("""
V1 1 0 {u(t)}; down
R1 1 2; right=2
L1 2 3; down=2
W1 0 3; right
W 1 5; up
W 2 6; up
C1 5 6; right=2""")'''

# DC volt divider for beginners
'''circuit = Circuit("""
V 1 0 6; down=1.5
R1 1 2 2; right=1.5
R2 2 0_2 4; down
W 0 0_2; right""")'''

#menu for analysis options
def display_menu():
    print("\n\nAvailable analysis types:")
    analysis_options = {
        '1': 'Draw circuit',
        '2': 'Frequency response',
        '3': 'Mesh analysis',
        '4': 'Nodal analysis',
        '5': 'Description',
        '6': 'Thevenin Analysis',
        '7': 'Norton Analysis',
        '8': 'Thevenin-Norton Transformation',
        '9': 'Norton-Thevenin Transformation',
        '10': 'State Space Analysis',
        '11': 'Loop Analysis',
        '12': 'For Beginners',
        '13': 'Plotting',
        '0': 'Exit'
    }

    for key, value in analysis_options.items():
        print(f"{key}. {value}")

    return analysis_options

#ainsley modified the user menu to make more sense in python
while True:
    #display the menu and get user input
    analysis_options = display_menu()
    analysis_choice = input("Choose the analysis type (enter the corresponding number, 0 to exit): ")
    if analysis_choice == '0':
        print("Exiting the program. Goodbye!\n")
        break

    #check for user input error
    if analysis_choice in analysis_options.keys():
        print('\n\n')
        perform_analysis(circuit, analysis_options[analysis_choice])
    else:
        print("Invalid input. Please enter a valid analysis number.")