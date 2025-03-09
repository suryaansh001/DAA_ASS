import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from heapq import heappop, heappush

def create_main_graph(file_path):
    """Create directed graph with all edge attributes"""
    df = pd.read_csv(file_path)
    G = nx.from_pandas_edgelist(df, source='source_name', target='destination_name', edge_attr=True, create_using=nx.DiGraph())
    return G

def visualize_subgraph(G, path):
    """Visualize only the necessary nodes and edges in the path"""
    plt.figure(figsize=(10, 6))
    sub_G = G.subgraph(path)
    pos = nx.spring_layout(sub_G, k=0.5)
    
    nx.draw(sub_G, pos, with_labels=True, node_size=800, node_color='skyblue', edge_color='grey', font_size=8, arrowsize=20)
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(sub_G, pos, nodelist=path, node_color='red')
    nx.draw_networkx_edges(sub_G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.title("Optimized Route Visualization")
    plt.show()

def dijkstra_shortest_path(G, source, target, weight_attr):
    """Find the shortest path using Dijkstra's algorithm"""
    try:
        path = nx.dijkstra_path(G, source, target, weight=weight_attr)
        length = nx.dijkstra_path_length(G, source, target, weight=weight_attr)
        return path, length
    except (nx.NodeNotFound, nx.NetworkXNoPath):
        return None, None

def astar_shortest_path(G, source, target, weight_attr):
    """Find the shortest path using A* algorithm"""
    try:
        path = nx.astar_path(G, source, target, weight=weight_attr)
        length = nx.astar_path_length(G, source, target, weight=weight_attr)
        return path, length
    except (nx.NodeNotFound, nx.NetworkXNoPath):
        return None, None

if __name__ == "__main__":
    file_path = 'final2_delhivery.csv'
    main_graph = create_main_graph(file_path)
    
    source = input("Enter source city: ").strip().title()
    target = input("Enter destination city: ").strip().title()
    
    if source not in main_graph.nodes or target not in main_graph.nodes:
        print("Error: Invalid city names")
    else:
        choice = input("Choose optimization:\n1. Shortest time (Dijkstra)\n2. Shortest distance (Dijkstra)\n3. Shortest time (A*)\n4. Shortest distance (A*)\n")
        
        if choice == '1':
            path, length = dijkstra_shortest_path(main_graph, source, target, 'efficiency')
            algo = "Dijkstra (Efficiency)"
        elif choice == '2':
            path, length = dijkstra_shortest_path(main_graph, source, target, 'actual_distance_to_destination')
            algo = "Dijkstra (Distance)"
        elif choice == '3':
            path, length = astar_shortest_path(main_graph, source, target, 'efficiency')
            algo = "A* (Efficiency)"
        elif choice == '4':
            path, length = astar_shortest_path(main_graph, source, target, 'actual_distance_to_destination')
            algo = "A* (Distance)"
        else:
            print("Invalid choice")
            path = None
        
        if path:
            print(f"Optimized path ({algo}): {path}\nTotal weight: {length}")
            visualize_subgraph(main_graph, path)