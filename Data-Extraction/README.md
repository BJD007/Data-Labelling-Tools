# Data-Extraction


## radarrawdataextractor.py

## Radar Data Extractor

The provided code defines a class named `RadarDataExtractor` for capturing and processing data from a Software Defined Radio (SDR) device used in a radar system. Here's a breakdown of the code:

### Class Definition
* **RadarDataExtractor:** This class handles all functionalities related to extracting data from the SDR.

### Initialization
* **__init__ function:** This constructor initializes the object with parameters like center frequency, sample rate, number of samples, number of channels, and output file path for saving data.
* **setup_logging:** Sets up logging for informational and error messages.

### SDR Setup and Capture
* **setup_sdr:** Configures the SDR device with the provided center frequency and sample rate.
* **capture_samples:** Reads samples from the SDR device based on the specified number of samples.

### Data Processing
* **process_samples:** Converts the captured samples to complex numbers (IQ data) and removes the mean for further processing.

### Data Extraction and Analysis
* **extract_data:** Combines `setup_sdr`, `capture_samples`, and `process_samples` to capture and process data in one function.
* **plot_data:** Visualizes the real and imaginary components of the captured data using matplotlib.
* **save_data:** Saves the processed data to an HDF5 file for further analysis.

### Closing and Real-time Operation
* **close:** Closes the connection to the SDR device.
* **run_real_time:** Continuously captures and processes samples in a loop, putting them into a queue for real-time processing.
* **start_real_time:** Starts a separate process running `run_real_time` and returns the queue and process object.

### Synchronization (Placeholder)
* **synchronize_with_radar:** This function is a placeholder for implementing any necessary synchronization logic with the radar control system.

### Example Usage
The `if __name__ == "__main__":` block demonstrates how to use the `RadarDataExtractor` class. It defines parameters for the data capture and creates an instance of the extractor. Then, it performs various operations like:
* Extracting raw data using `extract_data`.
* Printing data information (number of samples, shape, data type).
* Plotting the captured data using `plot_data`.
* Saving the data using `save_data`.
* Starting real-time data capture using `start_real_time`.
* Processing real-time data from the queue (placeholder for further analysis).

### Finally Block
Ensures the SDR device is closed, even if exceptions occur. Terminates the real-time data capture process.

This code provides a basic framework for capturing and processing data from an SDR used in a radar system. You can extend this by implementing:

* The synchronization logic in `synchronize_with_radar`.
* Real-time data processing within the `start_real_time` loop (e.g., object detection, filtering).
* Additional functionalities for specific radar applications.


## Usage:
- Install Required Libraries:
    - Ensure you have the necessary libraries installed: numpy, matplotlib, rtlsdr, h5py, logging, multiprocessing.
- Adjust Parameters:
    - Adjust the parameters (center frequency, sample rate, number of samples, number of channels, output file) as needed.
- Run the Script:
    - Run the script to capture, process, and save radar data.
    - The script also supports real-time data streaming and processing.

Created on 2020-10-13