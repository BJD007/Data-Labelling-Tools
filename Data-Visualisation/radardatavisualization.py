import sys
import numpy as np
import open3d as o3d
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, 
                             QCheckBox, QLabel, QLineEdit, QFileDialog, QSlider, QColorDialog, QListWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence, QShortcut

class RadarPointCloudVisualizer(QMainWindow):
    def __init__(self, point_cloud_path, manual_labels_path, auto_labels_path):
        super().__init__()
        self.point_cloud = self.load_point_cloud(point_cloud_path)
        self.manual_labels = self.load_labels(manual_labels_path)
        self.auto_labels = self.load_labels(auto_labels_path)
        self.current_view = 'manual'
        self.show_differences = False
        self.filtered_labels = set()
        self.point_size = 1
        self.background_color = [0.1, 0.1, 0.1]
        self.init_ui()

    def load_point_cloud(self, path):
        return o3d.io.read_point_cloud(path)

    def load_labels(self, path):
        return np.loadtxt(path, dtype=str)

    def init_ui(self):
        self.setWindowTitle('Radar Point Cloud Visualizer')
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        # Control panel
        control_layout = QVBoxLayout()
        layout.addLayout(control_layout, 1)

        self.view_selector = QComboBox()
        self.view_selector.addItems(['Manual Labels', 'Auto Labels', 'Side-by-Side'])
        self.view_selector.currentTextChanged.connect(self.change_view)
        control_layout.addWidget(self.view_selector)

        self.diff_checkbox = QCheckBox('Show Differences')
        self.diff_checkbox.stateChanged.connect(self.toggle_differences)
        control_layout.addWidget(self.diff_checkbox)

        # Label filter
        self.label_filter = QComboBox()
        self.label_filter.addItems(['All Labels'] + list(set(self.manual_labels) | set(self.auto_labels)))
        self.label_filter.currentTextChanged.connect(self.filter_labels)
        control_layout.addWidget(self.label_filter)

        # Search function
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search labels or coordinates")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_points)
        control_layout.addWidget(self.search_input)
        control_layout.addWidget(self.search_button)

        # Screenshot and export buttons
        self.screenshot_button = QPushButton("Take Screenshot")
        self.screenshot_button.clicked.connect(self.take_screenshot)
        control_layout.addWidget(self.screenshot_button)

        self.export_button = QPushButton("Export Labeled Point Cloud")
        self.export_button.clicked.connect(self.export_point_cloud)
        control_layout.addWidget(self.export_button)

        # Point size control
        self.point_size_slider = QSlider(Qt.Horizontal)
        self.point_size_slider.setMinimum(1)
        self.point_size_slider.setMaximum(10)
        self.point_size_slider.setValue(self.point_size)
        self.point_size_slider.valueChanged.connect(self.change_point_size)
        control_layout.addWidget(QLabel("Point Size:"))
        control_layout.addWidget(self.point_size_slider)

        # Background color control
        self.bg_color_button = QPushButton("Change Background Color")
        self.bg_color_button.clicked.connect(self.change_background_color)
        control_layout.addWidget(self.bg_color_button)

        self.label_info = QLabel('Label Info: ')
        control_layout.addWidget(self.label_info)

        # Legend
        self.legend = QListWidget()
        control_layout.addWidget(QLabel("Legend:"))
        control_layout.addWidget(self.legend)

        # Point cloud visualization
        self.vis_layout = QHBoxLayout()
        layout.addLayout(self.vis_layout, 3)

        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(self.point_cloud)

        self.vis_widget = QWidget.createWindowContainer(self.vis.get_render_window())
        self.vis_layout.addWidget(self.vis_widget)

        # Side-by-side view (initially hidden)
        self.vis2 = o3d.visualization.Visualizer()
        self.vis2.create_window()
        self.vis2.add_geometry(self.point_cloud)
        self.vis2_widget = QWidget.createWindowContainer(self.vis2.get_render_window())
        self.vis2_widget.hide()
        self.vis_layout.addWidget(self.vis2_widget)

        self.update_point_cloud_colors()
        self.setup_shortcuts()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+S"), self, self.take_screenshot)
        QShortcut(QKeySequence("Ctrl+E"), self, self.export_point_cloud)
        QShortcut(QKeySequence("Ctrl+F"), self, self.search_input.setFocus)
        QShortcut(QKeySequence("Ctrl+D"), self, self.toggle_differences)

    def change_view(self, view):
        if view == 'Side-by-Side':
            self.vis2_widget.show()
            self.current_view = 'manual'
            self.update_point_cloud_colors(self.vis)
            self.current_view = 'auto'
            self.update_point_cloud_colors(self.vis2)
        else:
            self.vis2_widget.hide()
            self.current_view = 'manual' if view == 'Manual Labels' else 'auto'
            self.update_point_cloud_colors()

    def toggle_differences(self, state):
        self.show_differences = state == Qt.Checked
        self.update_point_cloud_colors()

    def filter_labels(self, label):
        if label == 'All Labels':
            self.filtered_labels = set()
        else:
            self.filtered_labels = {label}
        self.update_point_cloud_colors()

    def search_points(self):
        query = self.search_input.text().lower()
        matching_indices = []
        for i, (point, manual_label, auto_label) in enumerate(zip(self.point_cloud.points, self.manual_labels, self.auto_labels)):
            if (query in manual_label.lower() or query in auto_label.lower() or
                query in f"{point[0]:.2f},{point[1]:.2f},{point[2]:.2f}"):
                matching_indices.append(i)
        
        if matching_indices:
            # Highlight matching points
            colors = np.asarray(self.point_cloud.colors)
            colors[matching_indices] = [1, 1, 0]  # Yellow for matching points
            self.point_cloud.colors = o3d.utility.Vector3dVector(colors)
            self.vis.update_geometry(self.point_cloud)
            self.vis.poll_events()
            self.vis.update_renderer()
            
            # Reset colors after 3 seconds
            QTimer.singleShot(3000, self.update_point_cloud_colors)

    def take_screenshot(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG Files (*.png)")
        if file_name:
            self.vis.capture_screen_image(file_name)

    def export_point_cloud(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Point Cloud", "", "PCD Files (*.pcd)")
        if file_name:
            o3d.io.write_point_cloud(file_name, self.point_cloud)

    def change_point_size(self, size):
        self.point_size = size
        self.vis.get_render_option().point_size = self.point_size
        self.vis2.get_render_option().point_size = self.point_size
        self.vis.update_renderer()
        self.vis2.update_renderer()

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.background_color = [color.redF(), color.greenF(), color.blueF()]
            self.vis.get_render_option().background_color = self.background_color
            self.vis2.get_render_option().background_color = self.background_color
            self.vis.update_renderer()
            self.vis2.update_renderer()

    def update_point_cloud_colors(self, visualizer=None):
        if visualizer is None:
            visualizer = self.vis

        colors = []
        unique_labels = set(self.manual_labels) | set(self.auto_labels)
        color_map = {label: np.random.rand(3) for label in unique_labels}

        for i in range(len(self.point_cloud.points)):
            manual_label = self.manual_labels[i]
            auto_label = self.auto_labels[i]

            if self.filtered_labels and (manual_label not in self.filtered_labels and auto_label not in self.filtered_labels):
                colors.append([0, 0, 0])  # Black for filtered out points
            elif self.show_differences and manual_label != auto_label:
                colors.append([1, 0, 0])  # Red for differences
            elif self.current_view == 'manual':
                colors.append(color_map[manual_label])
            else:
                colors.append(color_map[auto_label])

        self.point_cloud.colors = o3d.utility.Vector3dVector(colors)
        visualizer.update_geometry(self.point_cloud)
        visualizer.poll_events()
        visualizer.update_renderer()

        # Update label info
        manual_label_counts = {label: np.sum(self.manual_labels == label) for label in unique_labels}
        auto_label_counts = {label: np.sum(self.auto_labels == label) for label in unique_labels}
        diff_count = np.sum(self.manual_labels != self.auto_labels)
        
        info_text = f"Manual Labels: {manual_label_counts}\n"
        info_text += f"Auto Labels: {auto_label_counts}\n"
        info_text += f"Differences: {diff_count}"
        self.label_info.setText(info_text)

        # Update legend
        self.legend.clear()
        for label, color in color_map.items():
            self.legend.addItem(f"{label}: RGB({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})")

    def closeEvent(self, event):
        self.vis.destroy_window()
        self.vis2.destroy_window()

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
