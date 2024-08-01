import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import h5py
import logging
from multiprocessing import Process, Queue
import time

class RadarDataExtractor:
    def __init__(self, center_freq, sample_rate, num_samples, num_channels=1, output_file='radar_data.h5'):
        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.num_samples = num_samples
        self.num_channels = num_channels
        self.output_file = output_file
        self.sdr = RtlSdr()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename='radar_data_extractor.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def setup_sdr(self):
        try:
            self.sdr.center_freq = self.center_freq
            self.sdr.sample_rate = self.sample_rate
            self.sdr.gain = 'auto'
            logging.info(f'SDR setup: center_freq={self.center_freq}, sample_rate={self.sample_rate}')
        except Exception as e:
            logging.error(f'Error setting up SDR: {e}')
            raise

    def capture_samples(self):
        try:
            samples = self.sdr.read_samples(self.num_samples)
            logging.info(f'Captured {len(samples)} samples')
            return samples
        except Exception as e:
            logging.error(f'Error capturing samples: {e}')
            raise

    def process_samples(self, samples):
        try:
            iq_samples = np.array(samples).astype("complex64")
            iq_samples -= np.mean(iq_samples)
            logging.info(f'Processed samples: mean removed')
            return iq_samples
        except Exception as e:
            logging.error(f'Error processing samples: {e}')
            raise

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

    def save_data(self, samples):
        try:
            with h5py.File(self.output_file, 'w') as f:
                f.create_dataset('radar_samples', data=samples)
            logging.info(f'Saved data to {self.output_file}')
        except Exception as e:
            logging.error(f'Error saving data: {e}')
            raise

    def close(self):
        self.sdr.close()
        logging.info('SDR device closed')

    def run_real_time(self, queue):
        try:
            self.setup_sdr()
            while True:
                raw_samples = self.capture_samples()
                processed_samples = self.process_samples(raw_samples)
                queue.put(processed_samples)
                time.sleep(1)
        except Exception as e:
            logging.error(f'Error in real-time operation: {e}')
        finally:
            self.close()

    def start_real_time(self):
        queue = Queue()
        process = Process(target=self.run_real_time, args=(queue,))
        process.start()
        return queue, process

    def synchronize_with_radar(self):
        # Placeholder for synchronization logic
        logging.info('Synchronizing with radar control system')
        # Implement synchronization logic here

# Usage example
if __name__ == "__main__":
    # Parameters
    CENTER_FREQ = 2.4e9  # 2.4 GHz
    SAMPLE_RATE = 2.4e6  # 2.4 MHz
    NUM_SAMPLES = 256 * 1024  # Number of samples to capture
    NUM_CHANNELS = 1  # Number of channels (antennas)
    OUTPUT_FILE = 'radar_data.h5'

    # Create extractor instance
    extractor = RadarDataExtractor(CENTER_FREQ, SAMPLE_RATE, NUM_SAMPLES, NUM_CHANNELS, OUTPUT_FILE)

    try:
        # Extract raw data
        raw_data = extractor.extract_data()
        print(f"Captured {len(raw_data)} samples")
        print(f"Data shape: {raw_data.shape}")
        print(f"Data type: {raw_data.dtype}")

        # Plot the captured data
        extractor.plot_data(raw_data)

        # Save the data
        extractor.save_data(raw_data)

        # Start real-time data streaming
        queue, process = extractor.start_real_time()
        while True:
            if not queue.empty():
                real_time_data = queue.get()
                print(f"Real-time data shape: {real_time_data.shape}")
                # Process real-time data as needed
                # For example, plot or save real-time data

    finally:
        # Always close the SDR device
        extractor.close()
        process.terminate()
