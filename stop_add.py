import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QPushButton, QWidget

def create_main_graph(file_path):
    df = pd.read_csv(file_path)
    return nx.from_pandas_edgelist(df, 
                                 source='source_name', 
                                 target='destination_name', 
                                 edge_attr=True, 
                                 create_using=nx.DiGraph())

def visualize_subgraph(G, path):
    plt.figure(figsize=(10, 6))
    sub_G = G.edge_subgraph(list(zip(path, path[1:])))
    pos = nx.spring_layout(sub_G, k=0.5)
    
    nx.draw(sub_G, pos, with_labels=True,
           node_size=800, node_color='skyblue',
           edge_color='grey', font_size=8, arrowsize=20)
    
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(sub_G, pos, nodelist=path, node_color='red')
    nx.draw_networkx_edges(sub_G, pos, edgelist=path_edges, 
                          edge_color='red', width=2)
    
    plt.title("Optimized Route Visualization")
    plt.show()

def via_path_optimization(G, source, via, target, weight_attr):
    """Find optimal path through intermediate city using Dijkstra's"""
    try:
        path1 = nx.dijkstra_path(G, source, via, weight=weight_attr)
        path2 = nx.dijkstra_path(G, via, target, weight=weight_attr)
        return path1 + path2[1:], nx.dijkstra_path_length(G, source, via, weight=weight_attr) + nx.dijkstra_path_length(G, via, target, weight=weight_attr)
    except (nx.NodeNotFound, nx.NetworkXNoPath):
        return None, None

def on_find_path():
    source = source_combobox.currentText()
    via = via_combobox.currentText()
    target = target_combobox.currentText()
    weight_choice = weight_box.currentText().lower()
    
    if not all([source, target]) or via == "":
        result_label.setText("Error: Select all required cities")
        return
    
    weight_map = {
        'efficiency': 'efficiency',
        'distance': 'actual_distance_to_destination'
    }
    
    path, length = via_path_optimization(main_graph, source, via, target, weight_map[weight_choice])
    
    if path:
        result_text = f"Optimal Path via {via} ({weight_choice.title()}):\n{' → '.join(path)}\n"
        result_text += f"Total {weight_choice.title()}: {length:.2f} {'units' if weight_choice=='efficiency' else 'kms'}"
        result_label.setText(result_text)
        visualize_subgraph(main_graph, path)
    else:
        result_label.setText("No viable path through selected via city")

# Graph initialization
global main_graph
try:
    main_graph = create_main_graph('final2_delhivery.csv')
    print("Graph loaded successfully")
except Exception as e:
    print(f"Error loading graph: {e}")
    main_graph = None

# PyQt5 GUI Setup
app = QtWidgets.QApplication([])
window = QWidget()
window.setWindowTitle("Logistics Network Optimizer with Via-City Routing")
window.setGeometry(100, 100, 500, 500)

layout = QVBoxLayout()

# City selection
layout.addWidget(QLabel("Select Source City:"))
source_combobox = QComboBox()
source_combobox.addItems(list(main_graph.nodes) if main_graph else [])
layout.addWidget(source_combobox)

layout.addWidget(QLabel("Select Via City:"))
via_combobox = QComboBox()
via_combobox.addItems([""] + list(main_graph.nodes) if main_graph else [])
layout.addWidget(via_combobox)

layout.addWidget(QLabel("Select Destination City:"))
target_combobox = QComboBox()
target_combobox.addItems(list(main_graph.nodes) if main_graph else [])
layout.addWidget(target_combobox)

# Metric selection
layout.addWidget(QLabel("Optimize For:"))
weight_box = QComboBox()
weight_box.addItems(["Efficiency", "Distance"])
layout.addWidget(weight_box)

# Action button
find_btn = QPushButton("Find Optimal Via Path")
find_btn.clicked.connect(on_find_path)
layout.addWidget(find_btn)

# Results display
result_label = QLabel("")
result_label.setWordWrap(True)
layout.addWidget(result_label)

window.setLayout(layout)
window.show()
app.exec_()
