# Data-Extraction


## radarrawdataextractor.py
## This code does the following:
1. Sets up the SDR with specified center frequency and sample rate.
2. Captures a specified number of samples from the SDR.
3. Processes the samples (converts to complex numbers and removes DC offset).
4. Provides a method to plot the I and Q components of the signal.

## To use this code, you'll need to:
1. Install the required libraries: numpy, matplotlib, and pyrtlsdr.
2. Adjust the CENTER_FREQ, SAMPLE_RATE, and NUM_SAMPLES parameters to match your radar system's specifications.
3. Ensure you have the appropriate SDR hardware connected to your system.

## Things in progress oe TODO
- Implement more sophisticated signal processing techniques.
- Handle multiple channels if your radar uses an array of antennas.
- Implement real-time data streaming for continuous operation.
- Add error handling and logging for robustness.
- Implement data saving mechanisms (e.g., to HDF5 files for large datasets).
- Integrate with radar's control system to synchronize data capture with radar operation.

Working with raw radar data often requires specialized knowledge of the specific radar system's characteristics and the - principles of radar signal processing. Need to consult your radar system's documentation or work with a radar engineer to fully interpret and utilize the raw data.


Created on 2020-10-13