import numpy as np
from rtlsdr import RtlSdr
import matplotlib.pyplot as plt

class RadarDataExtractor:
    def __init__(self, center_freq, sample_rate, num_samples):
        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.num_samples = num_samples
        self.sdr = RtlSdr()

    def setup_sdr(self):
        self.sdr.center_freq = self.center_freq
        self.sdr.sample_rate = self.sample_rate
        self.sdr.gain = 'auto'

    def capture_samples(self):
        samples = self.sdr.read_samples(self.num_samples)
        return samples

    def process_samples(self, samples):
        # Convert to complex numpy array
        iq_samples = np.array(samples).astype("complex64")
        
        # Perform any necessary preprocessing
        # For example, remove DC offset
        iq_samples -= np.mean(iq_samples)
        
        return iq_samples

    def extract_data(self):
        self.setup_sdr()
        raw_samples = self.capture_samples()
        processed_samples = self.process_samples(raw_samples)
        return processed_samples

    def plot_data(self, samples):
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(np.real(samples))
        plt.title('I (Real) Component')
        plt.subplot(2, 1, 2)
        plt.plot(np.imag(samples))
        plt.title('Q (Imaginary) Component')
        plt.tight_layout()
        plt.show()

    def close(self):
        self.sdr.close()

# Usage example
if __name__ == "__main__":
    # Parameters
    CENTER_FREQ = 2.4e9  # 2.4 GHz
    SAMPLE_RATE = 2.4e6  # 2.4 MHz
    NUM_SAMPLES = 256 * 1024  # Number of samples to capture

    # Create extractor instance
    extractor = RadarDataExtractor(CENTER_FREQ, SAMPLE_RATE, NUM_SAMPLES)

    try:
        # Extract raw data
        raw_data = extractor.extract_data()

        print(f"Captured {len(raw_data)} samples")
        print(f"Data shape: {raw_data.shape}")
        print(f"Data type: {raw_data.dtype}")

        # Plot the captured data
        extractor.plot_data(raw_data)

        # Here you would typically save the data or pass it to your processing pipeline
        # np.save('raw_radar_data.npy', raw_data)

    finally:
        # Always close the SDR device
        extractor.close()
