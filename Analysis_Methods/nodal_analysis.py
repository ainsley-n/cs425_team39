from lcapy import *

import re
from Extra_Methods.ImageConverter import latex_to_png

def nodal_components(circuit):
    # Perform circuit graph function to collect node stuff
    cg = circuit.circuit_graph()
    
    # Get the number of nodes in the circuit
    num_node = cg.num_nodes
    print(f"There are {num_node} nodes in this Circuit:")
   
    # Create string for node display
    node_str = ' '.join(str(i) for i in range(num_node))
    print(f' {node_str}\n')
        
    print('The Components Connected at each Node are:')
    for i in range(num_node):
        components = cg.connected(i)
        print(f'[{i}]: {components}')
        
# def solve_nodal(circuit):
#     na = NodalAnalysis(circuit.laplace())
#     solution = na.solve()
#     for node, answer in solution:
#         print(f'V_{node}: {answer}')        
        

# Nodal analysis equations done by ainsley
def perform_nodal_analysis(circuit, png_filename=None):

    #Terminal Output, kept for reference
    #nodal_components(circuit)
    #print(' ')
    
    # Laplace domain
    laplace_result = circuit.laplace().nodal_analysis()
    laplace_nodal_equations = laplace_result.nodal_equations()

    print("\nNodal Equations:")
    # Print Laplace domain equations line by line
    for node, equation in laplace_nodal_equations.items():
        expression = equation.lhs
        expression_string = str(expression)
        
        # Define a regular expression pattern to match (s), *s, or s
        pattern = re.compile(r'\(s\)|\*s|s')
        
        expression_string_wo_s = pattern.sub('', expression_string)
        
        print(f"V_{node}: {expression_string_wo_s}")
        
    # solve_nodal(circuit)


    # LaTeX and PNG Output
    if png_filename is not None:
        expr = circuit.nodal_analysis().nodal_equations()
        s = '\\renewcommand{\\arraystretch}{1.3}\n'
        s += '\\begin{array}{ll}\n'

        for k, v in expr.items():
            if not isinstance(k, str):
                k = k.latex()

            s += k + ': & ' + v.latex() + '\\\\ \n'

        s += '\\end{array}\n'

        return latex_to_png(s, png_filename)


