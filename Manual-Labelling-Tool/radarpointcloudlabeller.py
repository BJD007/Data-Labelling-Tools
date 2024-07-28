import sys
import numpy as np
import open3d as o3d
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QLineEdit, QLabel
from PyQt5.QtCore import Qt

class RadarPointCloudLabeler(QMainWindow):
    def __init__(self, point_cloud_path):
        super().__init__()
        self.point_cloud = self.load_point_cloud(point_cloud_path)
        self.labels = ['Unlabeled'] * len(self.point_cloud.points)
        self.selected_points = []
        self.current_label = "Unlabeled"
        self.init_ui()

    def load_point_cloud(self, path):
        # Load point cloud - adjust this based on your data format
        pcd = o3d.io.read_point_cloud(path)
        return pcd

    def init_ui(self):
        self.setWindowTitle('Radar Point Cloud Labeler')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        # Left panel for controls
        left_panel = QVBoxLayout()

        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText("Enter label")
        left_panel.addWidget(self.label_input)

        self.add_label_btn = QPushButton("Add Label")
        self.add_label_btn.clicked.connect(self.add_label)
        left_panel.addWidget(self.add_label_btn)

        self.label_list = QListWidget()
        self.label_list.itemClicked.connect(self.select_label)
        left_panel.addWidget(self.label_list)

        self.apply_label_btn = QPushButton("Apply Label")
        self.apply_label_btn.clicked.connect(self.apply_label)
        left_panel.addWidget(self.apply_label_btn)

        self.save_btn = QPushButton("Save Labels")
        self.save_btn.clicked.connect(self.save_labels)
        left_panel.addWidget(self.save_btn)

        layout.addLayout(left_panel)

        # Right panel for point cloud visualization
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(self.point_cloud)

        # Set up a custom Qt widget to embed the Open3D visualization
        self.vis_widget = QWidget.createWindowContainer(self.vis.get_render_window())
        layout.addWidget(self.vis_widget, stretch=1)

        self.update_point_cloud_colors()

    def add_label(self):
        label = self.label_input.text()
        if label and label not in [self.label_list.item(i).text() for i in range(self.label_list.count())]:
            self.label_list.addItem(label)
            self.label_input.clear()

    def select_label(self, item):
        self.current_label = item.text()

    def apply_label(self):
        for point in self.selected_points:
            self.labels[point] = self.current_label
        self.update_point_cloud_colors()
        self.selected_points.clear()

    def update_point_cloud_colors(self):
        colors = []
        for label in self.labels:
            if label == 'Unlabeled':
                colors.append([0.5, 0.5, 0.5])  # Gray for unlabeled
            else:
                # Generate a unique color for each label
                color = np.random.rand(3)
                colors.append(color)

        self.point_cloud.colors = o3d.utility.Vector3dVector(colors)
        self.vis.update_geometry(self.point_cloud)
        self.vis.poll_events()
        self.vis.update_renderer()

    def save_labels(self):
        # Save labels to a file
        np.savetxt("point_cloud_labels.txt", self.labels, fmt='%s')
        print("Labels saved to point_cloud_labels.txt")

    def closeEvent(self, event):
        self.vis.destroy_window()

def main():
    app = QApplication(sys.argv)
    labeler = RadarPointCloudLabeler("path/to/your/point_cloud.pcd")
    labeler.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
