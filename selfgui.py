import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QPushButton, QWidget

def create_main_graph(file_path):
    """Create directed graph with all edge attributes"""
    df=pd.read_csv(file_path)
    G=nx.from_pandas_edgelist(df, source='source_name', target='destination_name', edge_attr=True, create_using=nx.DiGraph())
    return G

def visualize_subgraph(G, path):
    """Visualize only the necessary nodes and edges in the path"""
    plt.figure(figsize=(10, 6))
    sub_G=G.edge_subgraph(list(zip(path, path[1:])))
    pos=nx.spring_layout(sub_G, k=0.5)
    
    nx.draw(sub_G, pos, with_labels=True, node_size=800, node_color='skyblue', edge_color='grey', font_size=8, arrowsize=20)
    path_edges=list(zip(path, path[1:]))
    nx.draw_networkx_nodes(sub_G, pos, nodelist=path, node_color='red')
    nx.draw_networkx_edges(sub_G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.title("Optimized Route Visualization")
    plt.show()

def dijkstra_shortest_path(G, source, target, weight_attr):
    """Find the shortest path using Dijkstra's algorithm"""
    try:
        path=nx.dijkstra_path(G, source, target, weight=weight_attr)
        length=nx.dijkstra_path_length(G, source, target, weight=weight_attr)
        return path, length
    except (nx.NodeNotFound, nx.NetworkXNoPath):
        return None, None

def astar_shortest_path(G, source, target, weight_attr):
    """Find the shortest path using A* algorithm"""
    try:
        path=nx.astar_path(G, source, target, weight=weight_attr)
        length=nx.astar_path_length(G, source, target, weight=weight_attr)
        return path, length
    except (nx.NodeNotFound, nx.NetworkXNoPath):
        return None, None

def on_find_path():
    # Debugging: Check if the function is being called
    print("Find Path button clicked.")
    
    source=source_combobox.currentText()
    target=target_combobox.currentText()
    algo_choice=algo_combobox.currentText()
    
    # Debugging: Check selected source, target, and algorithm
    print(f"Selected Source: {source}")
    print(f"Selected Target: {target}")
    print(f"Selected Algorithm: {algo_choice}")
    
    if source not in main_graph.nodes or target not in main_graph.nodes:
        result_label.setText("Error: Invalid city names")
        print("Invalid source or target node.")
        return
    
    weight_attr='actual_distance_to_destination' if 'Distance' in algo_choice else 'efficiency'
    
    if 'Dijkstra' in algo_choice:
        path, length=dijkstra_shortest_path(main_graph, source, target, weight_attr)
    else:
        path, length=astar_shortest_path(main_graph, source, target, weight_attr)
    
    if path:
        result_label.setText(f"Optimized path: {path}\nTotal weight: {length}")
        print(f"Path found: {path} with total length: {length}")
        visualize_subgraph(main_graph, path)
    else:
        result_label.setText("No path found.")
        print("No path found.")

# Load graph
global main_graph
file_path='final4_delhivery.csv'
try:
    main_graph=create_main_graph(file_path)
    print("Graph loaded successfully.")
except Exception as e:
    print(f"Error loading graph: {e}")
    main_graph=None

# PyQt5 Setup
app=QtWidgets.QApplication([])

window=QWidget()
window.setWindowTitle("Logistics Network Optimization")
window.setGeometry(1000, 1000, 1000, 1000)

layout=QVBoxLayout()

# Create and add widgets
source_label=QLabel("Select Source City:")
layout.addWidget(source_label)

source_combobox=QComboBox()
source_combobox.addItems(list(main_graph.nodes) if main_graph else [])
layout.addWidget(source_combobox)

target_label=QLabel("Select Destination City:")
layout.addWidget(target_label)

target_combobox=QComboBox()
target_combobox.addItems(list(main_graph.nodes) if main_graph else [])
layout.addWidget(target_combobox)

algo_label=QLabel("Select Algorithm:")
layout.addWidget(algo_label)

algo_combobox=QComboBox()
algo_combobox.addItems(["Dijkstra (Efficiency)", "Dijkstra (Distance)", "A* (Efficiency)", "A* (Distance)"])
layout.addWidget(algo_combobox)

find_path_button=QPushButton("Find Path")
find_path_button.clicked.connect(on_find_path)
layout.addWidget(find_path_button)

result_label=QLabel("")
layout.addWidget(result_label)

window.setLayout(layout)
window.show()

app.exec_()
