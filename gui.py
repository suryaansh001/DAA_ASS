import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def create_main_graph(file_path):
    """Create directed graph with all edge attributes"""
    df = pd.read_csv(file_path)
    G = nx.from_pandas_edgelist(df, source='source_name', target='destination_name', edge_attr=True, create_using=nx.DiGraph())
    return G

def visualize_subgraph(G, path):
    """Visualize only the necessary nodes and edges in the path"""
    plt.figure(figsize=(10, 6))
    sub_G = G.edge_subgraph(list(zip(path, path[1:])))
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

def on_find_path():
    source = source_var.get()
    target = target_var.get()
    algo_choice = algo_var.get()
    
    if source not in main_graph.nodes or target not in main_graph.nodes:
        result_label.config(text="Error: Invalid city names")
        return
    
    weight_attr = 'actual_distance_to_destination' if 'Distance' in algo_choice else 'efficiency'
    
    if 'Dijkstra' in algo_choice:
        path, length = dijkstra_shortest_path(main_graph, source, target, weight_attr)
    else:
        path, length = astar_shortest_path(main_graph, source, target, weight_attr)
    
    if path:
        result_label.config(text=f"Optimized path: {path}\nTotal weight: {length}")
        visualize_subgraph(main_graph, path)

# Load graph
global main_graph
file_path = 'final2_delhivery.csv'
main_graph = create_main_graph(file_path)

# GUI Setup
root = tk.Tk()
root.title("Logistics Network Optimization")
root.geometry("500x400")

tk.Label(root, text="Select Source City:").pack()
source_var = ttk.Combobox(root, values=list(main_graph.nodes))
source_var.pack()

tk.Label(root, text="Select Destination City:").pack()
target_var = ttk.Combobox(root, values=list(main_graph.nodes))
target_var.pack()

tk.Label(root, text="Select Algorithm:").pack()
algo_var = ttk.Combobox(root, values=["Dijkstra (Efficiency)", "Dijkstra (Distance)", "A* (Efficiency)", "A* (Distance)"])
algo_var.pack()

tk.Button(root, text="Find Path", command=on_find_path).pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
