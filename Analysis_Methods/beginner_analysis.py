from lcapy import *
from Extra_Methods.LatexConverter import latexSingleTerm
from Extra_Methods.ImageConverter import latex_to_png

#listed to test search '#test#'

# Beginner Analysis for introducing new users
def perform_beginner_analysis(png_filename=None):
    print("This analysis demonstrates the avalible functionalities and how they operate with different circuits.")
    
    # DC volt divider for beginners
    circuit = Circuit("""
    V 1 0 6; down=1.5
    R1 1 2 2; right=1.5
    R2 2 0_2 4; down
    W 0 0_2; right""")
    print(" * Circuit has been replaced for demonstration.")
    
    # Draw circuit for user
    print("Circuits given as netlists can be analyzed and drawn.")
    circuit.draw()

    # Display voltage at node 1
    print("Node voltages can be displayed given the node. This is the voltage at node 1.")
    circuit[1].v.pprint()
    ###test####
    latex_to_png(latexSingleTerm(circuit[1].V(t), 'v'), png_filename)
    
    # Display voltage at node 2
    print("This is the voltage at node 2.")
    circuit[2].v.pprint()
    ##test##
    #latex_to_png(latexSingleTerm(circuit[2].V(t), 'v'), png_filename)


    # Display voltage accross each component
    print("Component voltages can be displayed given the component name. This is the voltage at the voltage source.")
    circuit.V.v.pprint()
    ##test##
    latex_to_png(latexSingleTerm(circuit['V'].V(t), 'v'), png_filename)

    print("This is the voltage at resistor 1.")
    circuit.R1.v.pprint()
    ##test##
    #latex_to_png(latexSingleTerm(circuit['R1'].V(t), 'v'), png_filename)

    print("This is the voltage at resistor 2.")
    circuit.R2.v.pprint()
    ##test##
    #latex_to_png(latexSingleTerm(circuit['R2'].V(t), 'v'), png_filename)

    # Display current accross each component
    print("Component current can be displayed given the component name. This is the current at the voltage source.")
    circuit.V.i.pprint()
    ##test##
    latex_to_png(latexSingleTerm(circuit['V'].I(t), 'i'), png_filename)

    print("This is the current at resistor 1.")
    circuit.R1.i.pprint()
    ##test##
    #latex_to_png(latexSingleTerm(circuit['R1'].I(t), 'i'), png_filename)

    print("This is the current at resistor 2.")
    circuit.R2.i.pprint()
    ##test##
    #latex_to_png(latexSingleTerm(circuit['R2'].I(t), 'i'), png_filename)

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
    ##test##
    latex_to_png(latexSingleTerm(circuit['V'].V(t), 'v'), png_filename)

    print("This is the voltage at the resistor.")
    circuit.R.v.pprint()
    ##test##
    latex_to_png(latexSingleTerm(circuit['R'].V(t), 'v'), png_filename)


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