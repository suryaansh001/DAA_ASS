import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QPushButton, QWidget

# directed graph banane ka function jo edge attributes ke saath kaam karta hai
def create_main_graph(file_path):
    df=pd.read_csv(file_path)
    G=nx.from_pandas_edgelist(df, source='source_name', target='destination_name', edge_attr=True, create_using=nx.DiGraph())
    return G

# subgraph visualize karne ka function jo sirf zaroori nodes aur edges ko dikhata hai
def visualize_subgraph(G, path):
    plt.figure(figsize=(10, 6))
    sub_G=G.edge_subgraph(list(zip(path, path[1:])))
    pos=nx.spring_layout(sub_G, k=0.5)
    
    nx.draw(sub_G, pos, with_labels=True, node_size=800, node_color='skyblue', edge_color='grey', font_size=8, arrowsize=20)
    path_edges=list(zip(path, path[1:]))
    nx.draw_networkx_nodes(sub_G, pos, nodelist=path, node_color='red')
    nx.draw_networkx_edges(sub_G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.title("optimized route visualization")
    plt.show()

# dijkstra's algorithm ka use karke shortest path nikalne ka function
def dijkstra_shortest_path(G, source, target, weight_attr):
    try:
        path=nx.dijkstra_path(G, source, target, weight=weight_attr)
        length=nx.dijkstra_path_length(G, source, target, weight=weight_attr)
        return path, length
    except (nx.NodeNotFound, nx.NetworkXNoPath):
        return None, None

# a* algorithm ka use karke shortest path nikalne ka function
# def astar_shortest_path(G, source, target, weight_attr):
#     try:
#         path=nx.astar_path(G, source, target, weight=weight_attr)
#         length=nx.astar_path_length(G, source, target, weight=weight_attr)
#         return path, length
#     except (nx.NodeNotFound, nx.NetworkXNoPath):
#         return None, None

# "find path" button ke click hone par yeh function call hota hai
def on_find_path():
    # check karna ke function call ho raha hai ya nahi
    print("find path button clicked.")
    
    source=source_combobox.currentText()
    target=target_combobox.currentText()
    algo_choice=algo_combobox.currentText()
    
    # selected source, target, aur algorithm check karna
    print(f"selected source: {source}")
    print(f"selected target: {target}")
    print(f"selected algorithm: {algo_choice}")
    
    if source not in main_graph.nodes or target not in main_graph.nodes:
        result_label.setText("error: invalid city names")
        print("invalid source ya target node.")
        return
    
    weight_attr='efficiency'
    
    if 'dijkstra' in algo_choice:
        path, length=dijkstra_shortest_path(main_graph, source, target, weight_attr)
    else:
        path, length=astar_shortest_path(main_graph, source, target, weight_attr)
    
    if path:
        result_label.setText(f"optimized path: {path}\ntotal weight: {length}")
        print(f"path found: {path} with total length: {length}")
        visualize_subgraph(main_graph, path)
    else:
        result_label.setText("no path found.")
        print("no path found.")

# graph load karna
global main_graph
file_path='final2_delhivery.csv'
try:
    main_graph=create_main_graph(file_path)
    print("graph successfully load ho gaya.")
except Exception as e:
    print(f"graph load karne mein error: {e}")
    main_graph=None

# pyqt5 setup
app=QtWidgets.QApplication([])

window=QWidget()
window.setWindowTitle("logistics network optimization")
window.setGeometry(1000, 1000, 1000, 1000)

layout=QVBoxLayout()

# widgets create aur add karna
source_label=QLabel("select source city:")
layout.addWidget(source_label)

source_combobox=QComboBox()
source_combobox.addItems(list(main_graph.nodes) if main_graph else [])
layout.addWidget(source_combobox)

target_label=QLabel("select destination city:")
layout.addWidget(target_label)

target_combobox=QComboBox()
target_combobox.addItems(list(main_graph.nodes) if main_graph else [])
layout.addWidget(target_combobox)

algo_label=QLabel("select algorithm:")
layout.addWidget(algo_label)

algo_combobox=QComboBox()
algo_combobox.addItems(["dijkstra "])

layout.addWidget(algo_combobox)


find_path_button=QPushButton("find path")
find_path_button.clicked.connect(on_find_path)
layout.addWidget(find_path_button)

result_label=QLabel("")
layout.addWidget(result_label)

window.setLayout(layout)
window.show()

app.exec_()
