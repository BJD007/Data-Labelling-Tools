# Manual-Labelling-Tool

## To use this tool:

- Install the required libraries: pip install numpy open3d PyQt5
- Replace the placeholder paths with the actual paths to your point cloud file, manual labels file, and auto-generated labels file.
- Run the script.

## This tool provides the following functionality:
- Load and visualize a point cloud with both manually and automatically assigned labels.
- Toggle between viewing manual labels and auto-generated labels.
- Option to highlight differences between manual and auto-generated labels.
- Display label statistics, including counts for each label type and the number of differences.

## Things todo in future or in progress
- Implement point selection and information display:

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

- Add filtering options to show only points with specific labels.
- Implement a search function to find points with specific labels or coordinates.
- Add the ability to save screenshots or export labeled point clouds.
- Implement a side-by-side view of manual and auto-labeled point clouds.
- Add controls for point size and background color.
- Implement keyboard shortcuts for common actions.
- Add a legend showing the color mapping for different labels.

Remember to adjust the point cloud and label loading functions (load_point_cloud and load_labels) to match needed specific data formats. This example assumes the point cloud is in a format readable by Open3D and labels are stored in text files, but might need to modify these functions if the data is in a different format.

This visualization tool provides a comprehensive starting point for comparing and analyzing manually labeled and auto-labeled radar point cloud data. We will further customize and expand its functionality based on the specific requirements and the characteristics of the radar data.



Created on 2021-05-14