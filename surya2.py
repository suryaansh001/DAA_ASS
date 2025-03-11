import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QPushButton, QWidget

def create_main_graph(file_path):
    df = pd.read_csv(file_path)
    # **IMPORTANT:  ADJUST THESE COLUMN NAMES TO MATCH YOUR CSV!**
    source_col = 'Source'       # Assumed source column name
    target_col = 'Destination'  # Assumed destination column name
    
    return nx.from_pandas_edgelist(df,
                                 source=source_col,
                                 target=target_col,
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

def dijkstra_shortest_path(G, source, target, weight_attr):
    try:
        path = nx.dijkstra_path(G, source, target, weight=weight_attr)
        length = nx.dijkstra_path_length(G, source, target, weight=weight_attr)
        return path, length
    except (nx.NodeNotFound, nx.NetworkXNoPath):
        return None, None

def on_find_path():
    source = source_combobox.currentText()
    target = target_combobox.currentText()
    weight_choice = weight_box.currentText().lower()

    if source not in main_graph.nodes or target not in main_graph.nodes:
        result_label.setText("Error: Invalid city names")
        return

    # Map UI labels to dataframe column names
    # **IMPORTANT:  ADJUST THESE COLUMN NAMES TO MATCH YOUR CSV!**
    weight_map = {
        'efficiency': 'efficiency',   # Assumed efficiency column name
        'distance': 'actual_distance'        # Assumed distance column name
    }

    path, length = dijkstra_shortest_path(main_graph, source, target, weight_map[weight_choice])

    if path:
        result_text = f"Optimal Path ({weight_choice.title()}):\n{' → '.join(path)}\n"
        result_text += f"Total {weight_choice.title()}: {length:.2f} {'units' if weight_choice=='efficiency' else 'kms'}"
        result_label.setText(result_text)
        visualize_subgraph(main_graph, path)
    else:
        result_label.setText("No viable path found")

# Graph initialization
global main_graph
file_path = 'final2_delhivery.csv'
try:
    main_graph = create_main_graph(file_path)
    print("Graph loaded successfully")
except Exception as e:
    print(f"Error loading graph: {e}")
    main_graph = None

# PyQt5 GUI Setup
app = QtWidgets.QApplication([])
window = QWidget()
window.setWindowTitle("Logistics Network Optimizer")
window.setGeometry(100, 100, 400, 400)

layout = QVBoxLayout()

# City selection
layout.addWidget(QLabel("Select Source City:"))
source_combobox = QComboBox()
source_combobox.addItems(list(main_graph.nodes) if main_graph else [])
layout.addWidget(source_combobox)

layout.addWidget(QLabel("Select Destination City:"))
target_combobox = QComboBox()
target_combobox.addItems(list(main_graph.nodes) if main_graph else [])
layout.addWidget(target_combobox)

# Metric selection
layout.addWidget(QLabel("Optimize For:"))
weight_box = QComboBox()
weight_box.addItems(["Efficiency", "Distance"])  # Corrected syntax
layout.addWidget(weight_box)

# Action button
find_btn = QPushButton("Find Optimal Path")
find_btn.clicked.connect(on_find_path)
layout.addWidget(find_btn)

# Results display
result_label = QLabel("")
result_label.setWordWrap(True)
layout.addWidget(result_label)

window.setLayout(layout)
window.show()
app.exec_()
