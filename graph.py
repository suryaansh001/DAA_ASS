import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('final1_delhivery.csv')
print("Columns:", df.columns)
print("\nFirst 10 rows:")
print(df.head(10))

# Create graph with proper edge attributes
G = nx.from_pandas_edgelist(df, 
                          source='source_name', 
                          target='destination_name', 
                          edge_attr=True,
                          create_using=nx.DiGraph())  # Use DiGraph for directed edges

def visualize_graph(G):
    """Improved visualization with layout and formatting"""
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(G, k=0.5)  # Better layout algorithm
    nx.draw(G, pos, with_labels=True, 
           node_size=800, 
           node_color='skyblue', 
           edge_color='gray',
           font_size=8,
           arrowsize=20)
    plt.title("Logistics Network Graph")
    plt.show()

def analyze_routes(G, source, target):
    """Comprehensive route analysis with error handling"""
    try:
        # Dijkstra's algorithm with weight consideration
        dijkstra_path = nx.dijkstra_path(G, source, target, weight='weight')  # Replace 'weight' with your actual column name
        
        # Shortest path (unweighted)
        shortest_path = nx.shortest_path(G, source, target)
        
        # Path lengths
        dijkstra_length = nx.dijkstra_path_length(G, source, target, weight='weight')
        shortest_length = nx.shortest_path_length(G, source, target)
        
        return {
            'dijkstra_path': dijkstra_path,
            'shortest_path': shortest_path,
            'dijkstra_length': dijkstra_length,
            'shortest_length': shortest_length
        }
    except nx.NodeNotFound as e:
        print(f"Error: {e}")
        return None
    except nx.NetworkXNoPath:
        print("No path exists between these nodes")
        return None

# User input with validation
source = input("Enter the source: ").strip().title()
target = input("Enter the target: ").strip().title()

# Verify nodes exist in graph
if source not in G.nodes:
    print(f"Source node '{source}' not found in graph")
elif target not in G.nodes:
    print(f"Target node '{target}' not found in graph")
else:
    # Visualize the graph
    visualize_graph(G)
    
    # Perform analysis
    results = analyze_routes(G, source, target)
    
    if results:
        print("\nAnalysis Results:")
        print(f"Dijkstra path (weighted): {results['dijkstra_path']}")
        print(f"Shortest path (unweighted): {results['shortest_path']}")
        print(f"Dijkstra path length (weighted): {results['dijkstra_length']}")
        print(f"Shortest path length (unweighted): {results['shortest_length']}")
