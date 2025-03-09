import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def create_main_graph():
    """Create directed graph with all edge attributes"""
    return nx.from_pandas_edgelist(df,
                                 source='source_name',
                                 target='destination_name',
                                 edge_attr=True,
                                 create_using=nx.DiGraph())

def create_path_subgraph(G, path):
    """Create subgraph containing only nodes and edges in the path"""
    subG = nx.DiGraph()
    subG.add_nodes_from(path)
    
    # Add edges from the path
    for i in range(len(path)-1):
        u, v = path[i], path[i+1]
        if G.has_edge(u, v):
            edge_data = G.get_edge_data(u, v)
            subG.add_edge(u, v, **edge_data)
    
    return subG

def visualize_subgraph(subG):
    """Visualize only the relevant nodes in path"""
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(subG)
    
    nx.draw(subG, pos, with_labels=True,
           node_size=1500,
           node_color='skyblue',
           edge_color='gray',
           width=2,
           arrowsize=20)
    
    plt.title("Optimal Route Visualization")
    plt.show()

def get_shortest_path(G, source, target, weight_attr):
    """Get shortest path with error handling"""
    try:
        path = nx.dijkstra_path(G, source, target, weight=weight_attr)
        length = nx.dijkstra_path_length(G, source, target, weight=weight_attr)
        return path, length
    except (nx.NodeNotFound, nx.NetworkXNoPath) as e:
        print(f"Error: {str(e)}")
        return None, None

# Main execution
if __name__ == "__main__":
    df = pd.read_csv('final2_delhivery.csv')
    main_graph = create_main_graph()
    
    source = input("Enter source city: ").strip().title()
    target = input("Enter destination city: ").strip().title()
    
    if source not in main_graph.nodes or target not in main_graph.nodes:
        print("Error: Invalid city names")
    else:
        choice = input("Choose optimization:\n1. Shortest time\n2. Shortest distance\n")
        
        weight_attr = 'efficiency' if choice == '1' else 'actual_distance_to_destination'
        path, length = get_shortest_path(main_graph, source, target, weight_attr)
        
        if path:
            # Create and visualize subgraph
            subG = create_path_subgraph(main_graph, path)
            visualize_subgraph(subG)
            
            print(f"\nOptimal path ({'time' if choice == '1' else 'distance'}):")
            print(" -> ".join(path))
            print(f"Total {'time' if choice == '1' else 'distance'}: {length}")
