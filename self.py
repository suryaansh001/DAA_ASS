import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QComboBox, QLabel, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Logistics Network Optimization')
        self.setGeometry(1000, 1000, 1000, 1000)
        label=QLabel("Select Source City:")
        self.source_combobox = QComboBox()
        self.source_combobox.addItems(list(main_graph.nodes) if main_graph else [])
        label2=QLabel("Select Destination City:")
        self.target_combobox = QComboBox()  
        self.target_combobox.addItems(list(main_graph.nodes) if main_graph else [])
        label3=QLabel("Select Algorithm:")
        self.algo_combobox = QComboBox()
        self.algo_combobox.addItems(["Dijkstra (Efficiency)", "Dijkstra (Distance)", "A* (Efficiency)", "A* (Distance)"])
        self.find_path_button = QPushButton("Find Path")
        self.find_path_button.clicked.connect(self.on_find_path)
        self.result_label = QLabel("")
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.source_combobox)
        layout.addWidget(label2)    
        layout.addWidget(self.target_combobox)
        layout.addWidget(label3)
        layout.addWidget(self.algo_combobox)
        layout.addWidget(self.find_path_button)
        layout.addWidget(self.result_label)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
    def on_find_path(self):
        source = self.source_combobox.currentText()
        target = self.target_combobox.currentText()
        algo_choice = self.algo_combobox.currentText()
        
        if source not in main_graph.nodes or target not in main_graph.nodes:
            self.result_label.setText("Error: Invalid city names")
            return
        
        weight_attr = 'actual_distance_to_destination' if 'Distance' in algo_choice else 'efficiency'
        
        if 'Dijkstra' in algo_choice:
            path, length = dijkstra_shortest_path(main_graph, source, target, weight_attr)
        else:
            path, length = astar_shortest_path(main_graph, source, target, weight_attr)
        
        if path:
            self.result_label.setText(f"Optimized path: {path}\nTotal weight: {length}")
            visualize_subgraph(main_graph, path)
        else:
            self.result_label.setText("No path found.")
            print("No path found.")
if __name__ == '__main__':
    #main graph
    df=pd.read_csv('final2_delhivery.csv')
    main_graph = create_main_graph(df)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


