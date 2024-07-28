# Manual-Labelling-Tool

To use this tool:
Install the required libraries: pip install numpy open3d PyQt5
Replace "path/to/your/point_cloud.pcd" with the actual path to your point cloud file.
Run the script.
This tool provides the following functionality:
Load and visualize a point cloud.
Add custom labels through a text input.
Select a label from the list to apply to points.
Click on points in the visualization to select them (Note: This functionality needs to be implemented using Open3D's picking feature).
Apply the selected label to the selected points.
Save the labels to a file.
To improve this tool, consider adding the following features:
Implement point selection in the 3D view:
python
def point_picking_callback(self, vis, action, mods):
    if action == 1:  # Left mouse button down
        mouse_pos = self.vis.get_render_window().GetEventPosition()
        picked_point = self.vis.pick_points(mouse_pos[0], mouse_pos[1])
        if picked_point:
            self.selected_points.append(picked_point['index'])
            # Highlight selected point
            self.point_cloud.colors[picked_point['index']] = [1, 0, 0]  # Red
            self.vis.update_geometry(self.point_cloud)

# In init_ui method:
self.vis.register_selection_changed_callback(self.point_picking_callback)

Add undo/redo functionality.
Implement different selection modes (e.g., box selection for multiple points).
Add a search function for labels.
Implement filtering to show only points with specific labels.
Add the ability to load pre-existing labels.
Implement keyboard shortcuts for common actions.
Add a status bar to show current selection and label information.
Remember to adjust the point cloud loading function (load_point_cloud) to match your specific data format. This example assumes the point cloud is in a format readable by Open3D, but you might need to modify it if your radar data is in a custom format.
This manual labeling tool provides a starting point for creating a more comprehensive solution tailored to your specific radar point cloud data and labeling requirements.



Created on 2021-05-14