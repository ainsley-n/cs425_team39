import networkx as nx
import re

def parse_netlist(netlist):
    components = []
    for line in netlist:
        if line.startswith("*"):
            continue 
        components.append(line)
    return components

def extract_nodes(components):
    nodes = set()
    for component in components:
        matches = re.findall(r'\b(?:\d+)\b', component)
        nodes.update(matches)
    return sorted(list(nodes))

def build_circuit_graph(components):
    circuit_graph = nx.Graph()
    for component in components:
        if component.startswith("*"):
            continue  
        nodes = re.findall(r'\b(?:\d+)\b', component)
        if len(nodes) == 2:  
            circuit_graph.add_edge(nodes[0], nodes[1])
        else:
            print(f"Warning: Invalid component found - {component}")
    return circuit_graph

def find_loops(circuit_graph):
    loops = list(nx.cycle_basis(circuit_graph))
    return loops

def main():
    spice_netlist = [
        "* Circuit with Multiple Loops",
        "V1 1 0 DC 10V",
        "R1 1 2 5k",
        "R2 2 3 3k",
        "R3 3 0 2k",
        "R4 2 4 4k",
        "R5 4 0 1k",
    ]

    components = parse_netlist(spice_netlist)
    nodes = extract_nodes(components)
    circuit_graph = build_circuit_graph(components)
    loops = find_loops(circuit_graph)

    print("Nodes:", nodes)
    print("Loops:", loops)

if __name__ == "__main__":
    main()
