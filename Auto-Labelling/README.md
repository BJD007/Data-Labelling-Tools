# Auto-Labelling

## The script does the following:
1. Loads radar point cloud data and a corresponding camera image.
2. Projects the radar points onto the image plane using a calibration matrix.
3. Performs object detection on the camera image using a pre-trained Faster R-CNN model.
4. Clusters the radar points using DBSCAN.
5. Assigns labels to radar points based on their projected location in the image and the detected objects.
6. Visualizes the labeled point cloud.

## To use this code, you'll need to:
- Install required libraries: numpy, opencv-python, open3d, scikit-learn, torch, and torchvision.
- Replace placeholder paths with actual paths to your radar point cloud data and camera image.
- Replace the placeholder calibration matrix with your actual radar-to-camera calibration matrix.
- Adjust the point cloud loading function to match your data format.
- Fine-tune parameters like DBSCAN eps and min_samples based on your data.
- Remember that this is a basic example and may need significant adjustments based on your specific data and requirements. 

## Things in progress or TODO:
- Implement more sophisticated point cloud segmentation algorithms.
- Use a more advanced object detection model or one specifically trained on your data.
- Implement temporal consistency if you're working with a sequence of frames.
- Add error handling and logging.
- Optimize for performance, especially if dealing with large point clouds.
- Implement a user interface for manual verification and correction of labels.
- Consider using 3D object detection models that work directly on point cloud data for more accurate labeling.

This auto-labeling tool provides a starting point, but creating a robust, production-ready system for radar point cloud labeling typically requires significant development and fine-tuning based on the specific characteristics of your radar system and application requirements.


Created on 2021-09-21