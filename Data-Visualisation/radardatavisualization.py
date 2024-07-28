import sys
import numpy as np
import open3d as o3d
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QCheckBox, QLabel
from PyQt5.QtCore import Qt

class RadarPointCloudVisualizer(QMainWindow):
    def __init__(self, point_cloud_path, manual_labels_path, auto_labels_path):
        super().__init__()
        self.point_cloud = self.load_point_cloud(point_cloud_path)
        self.manual_labels = self.load_labels(manual_labels_path)
        self.auto_labels = self.load_labels(auto_labels_path)
        self.current_view = 'manual'
        self.show_differences = False
        self.init_ui()

    def load_point_cloud(self, path):
        # Load point cloud - adjust this based on your data format
        return o3d.io.read_point_cloud(path)

    def load_labels(self, path):
        # Load labels - adjust this based on your label format
        return np.loadtxt(path, dtype=str)

    def init_ui(self):
        self.setWindowTitle('Radar Point Cloud Visualizer')
        self.setGeometry(100, 100, 1000, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Control panel
        control_layout = QHBoxLayout()

        self.view_selector = QComboBox()
        self.view_selector.addItems(['Manual Labels', 'Auto Labels'])
        self.view_selector.currentTextChanged.connect(self.change_view)
        control_layout.addWidget(self.view_selector)

        self.diff_checkbox = QCheckBox('Show Differences')
        self.diff_checkbox.stateChanged.connect(self.toggle_differences)
        control_layout.addWidget(self.diff_checkbox)

        self.label_info = QLabel('Label Info: ')
        control_layout.addWidget(self.label_info)

        layout.addLayout(control_layout)

        # Point cloud visualization
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(self.point_cloud)

        # Set up a custom Qt widget to embed the Open3D visualization
        self.vis_widget = QWidget.createWindowContainer(self.vis.get_render_window())
        layout.addWidget(self.vis_widget)

        self.update_point_cloud_colors()

    def change_view(self, view):
        self.current_view = 'manual' if view == 'Manual Labels' else 'auto'
        self.update_point_cloud_colors()

    def toggle_differences(self, state):
        self.show_differences = state == Qt.Checked
        self.update_point_cloud_colors()

    def update_point_cloud_colors(self):
        colors = []
        unique_labels = set(self.manual_labels) | set(self.auto_labels)
        color_map = {label: np.random.rand(3) for label in unique_labels}

        for i in range(len(self.point_cloud.points)):
            manual_label = self.manual_labels[i]
            auto_label = self.auto_labels[i]

            if self.show_differences and manual_label != auto_label:
                colors.append([1, 0, 0])  # Red for differences
            elif self.current_view == 'manual':
                colors.append(color_map[manual_label])
            else:
                colors.append(color_map[auto_label])

        self.point_cloud.colors = o3d.utility.Vector3dVector(colors)
        self.vis.update_geometry(self.point_cloud)
        self.vis.poll_events()
        self.vis.update_renderer()

        # Update label info
        manual_label_counts = {label: np.sum(self.manual_labels == label) for label in unique_labels}
        auto_label_counts = {label: np.sum(self.auto_labels == label) for label in unique_labels}
        diff_count = np.sum(self.manual_labels != self.auto_labels)
        
        info_text = f"Manual Labels: {manual_label_counts}\n"
        info_text += f"Auto Labels: {auto_label_counts}\n"
        info_text += f"Differences: {diff_count}"
        self.label_info.setText(info_text)

    def closeEvent(self, event):
        self.vis.destroy_window()

def main():
    app = QApplication(sys.argv)
    visualizer = RadarPointCloudVisualizer(
        "path/to/your/point_cloud.pcd",
        "path/to/your/manual_labels.txt",
        "path/to/your/auto_labels.txt"
    )
    visualizer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
