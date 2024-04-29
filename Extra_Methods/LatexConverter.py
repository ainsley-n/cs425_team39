# Set of helper funtions to form latex expressions to be used in the image converter

units = {
    'v': 'V',
    'i': 'A',
    'r': 'R',
    'c': 'G'
}

# Helper function to return expressions in LaTeX
# Ex. expr = circuit.laplace().mesh_analysis().mesh_equations()
def latexExpression(expr):
# Generate LaTeX and PNG image of mesh equations
    s = '\\begin{tabular}{ll}\n'

    for k, v in expr.items():
        if not isinstance(k, str):
            k = k.latex()

        s += '$' + k + '$: & $' + v.latex() + '$\\\\ \n'

    s += '\\end{tabular}\n'

    return s    
    
# Helper function to return a component property and its unit in LaTeX
def latexSingleTerm(term, unit):
    # Generate LaTeX string for a term and its unit
    s = term.latex() + '\\:' + units[unit]
    return s