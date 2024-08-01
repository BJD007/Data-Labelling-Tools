# Data-Visualisation

## To use this visualization tool:
- Install the required libraries: pip install numpy open3d PyQt5
- Replace the placeholder paths with the actual paths to your point cloud file, manual labels file, and auto-generated labels file.
- Run the script.


## To implement point selection and information display:
python
def point_picking_callback(self, vis, action, mods):
    if action == 1:  # Left mouse button down
        mouse_pos = self.vis.get_render_window().GetEventPosition()
        picked_point = self.vis.pick_points(mouse_pos[0], mouse_pos[1])
        if picked_point:
            index = picked_point['index']
            point = self.point_cloud.points[index]
            manual_label = self.manual_labels[index]
            auto_label = self.auto_labels[index]
            self.label_info.setText(f"Point {index}: {point}\nManual Label: {manual_label}\nAuto Label: {auto_label}")

# In init_ui method:
self.vis.register_selection_changed_callback(self.point_picking_callback)

# Radar Point Cloud Visualizer

The `RadarPointCloudVisualizer` is a Python application that uses PyQt5 and Open3D to visualize radar point clouds along with manual and automatic labels. The application allows users to interactively view, filter, and compare point clouds with labeled data.

## Features

- **View and Compare Labels:** Switch between manual and automatic labels or display them side-by-side.
- **Highlight Differences:** Identify and highlight discrepancies between manual and automatic labels.
- **Search Functionality:** Search for specific labels or points within the point cloud.
- **Point Size and Background Customization:** Adjust the size of points in the visualization and change the background color.
- **Export and Screenshot:** Export labeled point clouds and take screenshots of the current view.
- **Shortcut Keys:** Use keyboard shortcuts for quick actions.

## Dependencies

The application requires the following Python libraries:

- `numpy`
- `open3d`
- `PyQt5`

You can install these dependencies using `pip`:

```bash
pip install numpy open3d PyQt5


Remember to adjust the point cloud and label loading functions (load_point_cloud and load_labels) to match needed specific data formats. This example assumes the point cloud is in a format readable by Open3D and labels are stored in text files, but might need to modify these functions if the data is in a different format.

This visualization tool provides a comprehensive starting point for comparing and analyzing manually labeled and auto-labeled radar point cloud data. We will further customize and expand its functionality based on the specific requirements and the characteristics of the radar data.



Created on 2020-10-21