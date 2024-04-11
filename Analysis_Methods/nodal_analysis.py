from lcapy import NodalAnalysis
import re
from lcapy.system import tmpfilename, LatexRunner, PDFConverter

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
def perform_nodal_analysis(circuit):

    #Terminal Output, kept for reference
    nodal_components(circuit)
    print(' ')
    
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
    expr = circuit.laplace().nodal_analysis().nodal_equations()
    s = '\\begin{tabular}{ll}\n'

    for k, v in expr.items():
        if not isinstance(k, str):
            k = k.latex()

        s += '$' + k + '$: & $' + v.latex() + '$\\\\ \n'

    s += '\\end{tabular}\n'

    tex_filename = tmpfilename('.tex')

    # Need amsmath for operatorname
    template = ('\\documentclass[a4paper]{standalone}\n'
                '\\usepackage{amsmath}\n'
                '\\begin{document}\n$%s$\n'
                '\\end{document}\n')
    content = template % s

    open(tex_filename, 'w').write(content)
    pdf_filename = tex_filename.replace('.tex', '.pdf')
    latexrunner = LatexRunner()
    latexrunner.run(tex_filename)

    png_filename = "temp/nodal_analysis.png"
    pdfconverter = PDFConverter()
    pdfconverter.to_png(pdf_filename, png_filename, dpi=300)

    return png_filename


