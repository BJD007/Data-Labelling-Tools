# Auto-Labelling

## Functionality:
- Monitors radar data from multiple positions around a port.
- Processes the radar data to detect potential locations of people or objects.
- Generates critical or warning alerts based on the proximity of detected objects to the crane.
- Visualizes the port environment, crane location, radar positions, and detected objects on a graphical user interface (GUI).

## Components:
- Radar Data: The system can handle simulated radar data or potentially be configured to work with real radar data input (placeholder function included).
- 3D Object Detection: The system utilizes a pre-trained PointRCNN model (needs to be implemented) to identify objects within the radar data. PointRCNN is a 3D object detection model that can classify and localize objects based on point cloud data.
- Alerts: The system generates critical or warning alerts based on the distance between detected objects and the crane. Critical alerts are triggered for objects very close to the crane, while warnings are issued for objects within a larger radius. Alerts are displayed on the GUI and logged for record-keeping purposes. Additionally, a sound notification can be played for critical alerts.
- User Interface (GUI):
- Control the crane's position (X, Y coordinates) and arm angle.
- Adjust the zoom level of the visualization.
- Choose between simulated or real data (if available).
- Set the update rate for data visualization and alerts.
- Access functionalities like calibration and manual correction (implementation details not provided).
- Overall, this Python application offers a user-friendly interface for monitoring a port area using radar data and receiving critical alerts regarding nearby objects that could potentially pose a safety hazard to the crane's operation.

## Note:
The script relies on external libraries like PyQt5 for the GUI and PyTorch for the 3D object detection model (PointRCNN). These libraries would need to be installed for the application to run.
The implementation of the 3D object detection model (PointRCNN) and functionalities like calibration and manual correction are not provided in the script.



## Usage:
- Install Required Libraries:
    - Ensure you have the necessary libraries installed: PyQt5, torch, numpy, sklearn, and any dependencies for PointRCNN.
- Implement Specific Logic:
    - Implement the specific logic for different radar data formats in the get_real_radar_data method.
    - Implement the calibration logic in the calibrate_radar method.
- Adjust Model and Resources:
    - Adjust the 3D object detection model and its usage according to your specific requirements and available GPU resources.
- Fine-Tune Data Augmentation:
    - Fine-tune the data augmentation methods based on your data characteristics.

Created on 2021-09-21