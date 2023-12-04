from lcapy import Circuit

# def perform_mesh_analysis(circuit):
#     #time domain
#     l = circuit.mesh_analysis()
#     mesh_equations = l.mesh_equations()

#     print("Mesh Equations (Time Domain):")
#     #print equations line by line
#     for variable, equation in mesh_equations.items():
#         print(f"{variable}: {equation}")

#     #LaPlace Domain
#     l = circuit.laplace().mesh_analysis()
#     laplace_mesh_equations = l.mesh_equations()

#     print("\nMesh Equations (Laplace Domain):")
#     #print Laplace domain equations line by line
#     for variable, equation in laplace_mesh_equations.items():
#         print(f"{variable}: {equation}")

def parse_netlist(netlist):
    components = []
    current_component = None

    for line in str(netlist).split('\n'):
        if line.strip():  # Check if the line is not empty
            parts = line.split()
            component_type = parts[0]
            print(f'component_type: {component_type}')

            # Extract nodes, excluding the semicolon
            nodes_str = ' '.join(parts[1:-1]).rstrip(';')
            print(f'nodes_str: {nodes_str}')

            # Split the combined string into nodes based on semicolon
            nodes = tuple(int(node) if node.isdigit() else node for node in nodes_str.split())
            print(f'nodes: {nodes}')

            # If it's a new component, start a new tuple
            if current_component is None:
                current_component = nodes
            else:
                # If it's the same component, update the end node
                current_component = (current_component[0], nodes[1])
                
            print(f'current component: {current_component}')

            # If it's the last line of the component, add it to the list
            if parts[-1][-1] != ';':
                components.append((component_type, current_component))
                current_component = None
    print(f'components: {components}')
    return components


def organize_components(components):
    node_dict = {}
    for component_type, nodes in components:
        if component_type != 'W':  # Exclude 'W' components
            for node in nodes:
                if node not in node_dict:
                    node_dict[node] = []
                node_dict[node].append((component_type, nodes))

    return node_dict

def sort_by_node(organized_components):
    sorted_components_list = []
    for node, components in organized_components.items():
        for component_type, nodes in components:
            # Handle both integer and string nodes
            normalized_nodes = [str(node).split('_')[0] if '_' in str(node) else str(node) for node in nodes]
            sorted_components_list.append({component_type: normalized_nodes})
        
    return sorted_components_list




def perform_mesh_analysis(circuit):
    # Parse and organize components
    components = parse_netlist(circuit)
    organized_components = organize_components(components)
    print(f'Organized Components {organized_components}')

    # Print organized components
    sorted_components = sort_by_node(organized_components)
    print(f'Sorted Components {sorted_components}')