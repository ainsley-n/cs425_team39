from lcapy import Circuit
from sympy import sympify

#this was from the lcapy documentation
def perform_lcapy_mesh(circuit):
    # mesh equations using LaPlace Domain
    l = circuit.laplace().mesh_analysis()
    laplace_mesh_equations = l.mesh_equations()

    print("\nMesh Equations :")
    #print Laplace domain equations line by line
    for variable, equation in laplace_mesh_equations.items():
        print(f"{variable}: {sympify(str(equation))}")
        
    # laplace_matrix_equations = l.matrix_equations(form='A y = b')
    # print(laplace_matrix_equations)
    
    # laplace_solutions = l.solve_laplace()
    # print('SOLUTIONSS')
    # print(laplace_solutions)

def parse_netlist(netlist):
    components = []
    current_component = None

    for line in str(netlist).split('\n'):
        if line.strip(): 
            parts = line.split()
            component_type = parts[0]
            print(f'component_type: {component_type}')

            #extract nodes, exclude the semicolon
            nodes_str = ' '.join(parts[1:-1]).rstrip(';')
            print(f'nodes_str: {nodes_str}')

            #split the combined string based on semicolon
            nodes = tuple(int(node) if node.isdigit() else node for node in nodes_str.split())
            print(f'nodes: {nodes}')

            #if it's a new component start new tuple
            if current_component is None:
                current_component = nodes
            else:
                #if it's the same component update end node
                current_component = (current_component[0], nodes[1])
                
            print(f'current component: {current_component}')

            #if it's the last line add it to list
            if parts[-1][-1] != ';':
                components.append((component_type, current_component))
                current_component = None
    print(f'components: {components}')
    return components


def organize_components(components):
    node_dict = {}
    for component_type, nodes in components:
        #'W' doesn't count as a component
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
            #handle integer and string nodes
            normalized_nodes = [str(node).split('_')[0] if '_' in str(node) else str(node) for node in nodes]
            sorted_components_list.append({component_type: normalized_nodes})
        sorted_components_dict[node] = sorted_components_list

    return sorted_components_dict





def perform_mesh_analysis(circuit):
    #organize components
    components = parse_netlist(circuit)
    organized_components = organize_components(components)
    print(f'Organized Components {organized_components}\n')

    sorted_components = sort_by_node(organized_components)
    #print sorted components
    print(f'Sorted Components')
    for node, components_list in sorted_components.items():
        print(f"{node}:")
        for component_dict in components_list:
            for component_type, nodes in component_dict.items():
                print(f"  {component_type} {', '.join(map(str, nodes))}")
        print()
        
    perform_lcapy_mesh(circuit)