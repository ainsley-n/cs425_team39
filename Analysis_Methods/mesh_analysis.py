from lcapy import *
import re
from Extra_Methods.ImageConverter import latex_to_png

# This was from the lcapy documentation
def perform_lcapy_mesh(circuit):
    la = LoopAnalysis(circuit)
        
    # Function to find loops in Circuit
    mesh_currents = la.mesh_currents()
    num_loops = len(mesh_currents)
    print(f'There are {num_loops} loop(s) within this circuit')
    print('\nMesh Currents:')
    num_loops_str = ' '.join(f'I_{i + 1};' for i in range(num_loops))
    print(f'{num_loops_str}')
    
    # for i in range(num_loops):
    #     print(f'I_{i + 1}')

    print('\nLoops: ')
    # Get the list of loops
    loops = la.loops()
    
    # Print nodal loops and their nodes
    for i, loop in enumerate(loops):
        loop_str = ' -> '.join(str(node) for node in loop)
        loop_str += f" -> {loop[0]}"  # Add the return to the original node
        print(f'I_{i + 1}: {loop_str}')
        
    # Extract components in the correct order
    components_list = la.loops_by_cpt_name()
    components_dict = {i + 1: components_list[i] for i in range(len(loops))}
    
    # print(f'Component Dictionary: {components_dict}')

    print('\nComponents in Each Loop: ')
    for i, loop in enumerate(loops):
        loop_index = i + 1
        component_str = '  '.join(str(component) for component in components_dict[loop_index])
        print(f"I_{loop_index}: {component_str}")

    # Mesh equations using LaPlace Domain
    l = circuit.laplace().mesh_analysis()
    laplace_mesh_equations = l.mesh_equations()

    print("\nMesh Equations :")
    # Print Laplace domain equations line by line
    for variable, equation in laplace_mesh_equations.items():
        expression = equation.lhs
        expression_string = str(expression)
        variable_string = str(variable)
        
        # Define a regular expression pattern to match (s), *s, or s
        pattern = re.compile(r'\(s\)|\*s|s')
        
        expression_string_wo_s = pattern.sub('', expression_string)
        variable_string_wo_s = pattern.sub('', variable_string)
        print(f"{variable_string_wo_s}: {expression_string_wo_s}")
        
        
    # laplace_matrix_equations = l.matrix_equations(form='A y = b')
    # print(laplace_matrix_equations)
    
    
    # # Create a list of Laplace domain equations
    # laplace_equations = [equation.lhs - equation.rhs for equation in laplace_mesh_equations.values()]

    # # Solve Laplace domain equations using SymPy's solve function
    # laplace_solution = solve(laplace_equations, laplace_vars.values())

    # print('\nLaplace Domain Solutions:')
    # for node, solution in zip(laplace_vars.keys(), laplace_solution):
    #     print(f"V{node}(s): {solution}")
        
        
def parse_netlist(netlist):
    components = []
    current_component = None

    for line in str(netlist).split('\n'):
        if line.strip(): 
            parts = line.split()
            component_type = parts[0]
            # print(f'component_type: {component_type}')

            # Extract nodes, exclude the semicolon
            nodes_str = ' '.join(parts[1:-1]).rstrip(';')
            # print(f'nodes_str: {nodes_str}')

            # Split the combined string based on semicolon
            nodes = tuple(int(node) if node.isdigit() else node for node in nodes_str.split())
            # print(f'nodes: {nodes}')

            # If it's a new component start new tuple
            if current_component is None:
                current_component = nodes
            else:
                # If it's the same component update end node
                current_component = (current_component[0], nodes[1])
                
            # print(f'current component: {current_component}')

            # If it's the last line add it to list
            if parts[-1][-1] != ';':
                components.append((component_type, current_component))
                current_component = None
    # print(f'components: {components}')
    return components


def organize_components(components):
    node_dict = {}
    for component_type, nodes in components:
        # 'W' doesn't count as a component
        if component_type != 'W':
            for node in nodes:
                normalized_node = str(node).split('_')[0] if '_' in str(node) else str(node)
                if normalized_node not in node_dict:
                    node_dict[normalized_node] = []
                node_dict[normalized_node].append((component_type, nodes))

    return node_dict

def sort_by_node(organized_components):
    sorted_components_dict = {}
    for node, components in organized_components.items():
        sorted_components_list = []
        for component_type, nodes in components:
            # Handle integer and string nodes
            normalized_nodes = [str(node).split('_')[0] if '_' in str(node) else str(node) for node in nodes]
            sorted_components_list.append({component_type: normalized_nodes})
        sorted_components_dict[node] = sorted_components_list

    return sorted_components_dict



def perform_mesh_analysis(circuit, png_filename=None):
    # Organize components
    components = parse_netlist(circuit)
    organized_components = organize_components(components)
    # print(f'Organized Components {organized_components}\n')
    

    sorted_components = sort_by_node(organized_components)
    #print sorted components
    # print(f'Sorted Components')
    # for node, components_list in sorted_components.items():
    #     print(f"{node}:")
    #     for component_dict in components_list:
    #         for component_type, nodes in component_dict.items():
    #             print(f"  {component_type} {', '.join(map(str, nodes))}")
    #     print()

    #perform_lcapy_mesh(circuit): Terminal output, kept for reference    
    perform_lcapy_mesh(circuit)


    # Generate LaTeX and PNG image of mesh equations
    if png_filename is not None:
        expr = circuit.mesh_analysis().mesh_equations()
        s = '\\renewcommand{\\arraystretch}{1.3}\n'
        s = '\\begin{array}{ll}\n'

        for k, v in expr.items():
            if not isinstance(k, str):
                k = k.latex()

            s += k + ': & ' + v.latex() + '\\\\ \n'

        s += '\\end{array}\n'

        latex_to_png(s, png_filename)