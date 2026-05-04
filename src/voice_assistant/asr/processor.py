# Import necessary libraries for audio processing and ASR
import numpy as np
# Import logging for debugging and information tracking
import logging
# Import threading for concurrent operations
import threading
# Import queue for thread-safe data passing
from queue import Queue
# Import time for timing operations
import time

# Configure logging to track application behavior
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Create a logger instance for this module
logger = logging.getLogger(__name__)


# Define the ASRProcessor class to handle audio processing
class ASRProcessor:
    # Initialize the processor with default parameters
    def __init__(self, sample_rate=16000, chunk_size=1024, timeout=5):
        # Store the audio sample rate (samples per second)
        self.sample_rate = sample_rate
        # Store the size of audio chunks to process
        self.chunk_size = chunk_size
        # Store the timeout duration for processing
        self.timeout = timeout
        # Initialize a queue to store audio chunks
        self.audio_queue = Queue()
        # Initialize a flag to control processing state
        self.is_processing = False
        # Initialize a list to store transcribed text
        self.transcriptions = []
        # Log initialization completion
        logger.info(f"ASRProcessor initialized with sample_rate={sample_rate}, chunk_size={chunk_size}")

    # Method to add audio chunks to the processing queue
    def add_audio_chunk(self, audio_data):
        # Check if the provided audio data is valid
        if audio_data is None or len(audio_data) == 0:
            # Log a warning if no audio data is provided
            logger.warning("Empty audio chunk received")
            # Return early without adding to queue
            return False
        
        # Try to add the audio chunk to the queue
        try:
            # Put the audio data in the queue with a timeout
            self.audio_queue.put(audio_data, timeout=self.timeout)
            # Log successful addition to queue
            logger.debug(f"Audio chunk of size {len(audio_data)} added to queue")
            # Return True to indicate success
            return True
        # Catch any queue-related exceptions
        except Exception as e:
            # Log the error that occurred
            logger.error(f"Error adding audio chunk: {str(e)}")
            # Return False to indicate failure
            return False

    # Method to process audio chunks from the queue
    def process_audio(self):
        # Set the processing flag to True
        self.is_processing = True
        # Log that processing has started
        logger.info("Audio processing started")
        
        # Continue processing while the flag is True
        while self.is_processing:
            # Try to retrieve an audio chunk from the queue
            try:
                # Get audio chunk from queue with timeout
                audio_chunk = self.audio_queue.get(timeout=1)
                # Log the chunk being processed
                logger.debug(f"Processing audio chunk of size {len(audio_chunk)}")
                # Process the audio chunk
                result = self._process_chunk(audio_chunk)
                # Add the result to transcriptions list
                self.transcriptions.append(result)
                # Mark the queue task as done
                self.audio_queue.task_done()
            # Catch timeout exception when queue is empty
            except:
                # Continue the loop if no audio is available
                continue
        
        # Log that processing has stopped
        logger.info("Audio processing stopped")

    # Private method to process individual audio chunks
    def _process_chunk(self, audio_data):
        # Convert audio data to numpy array if needed
        if not isinstance(audio_data, np.ndarray):
            # Convert to numpy array with float32 dtype
            audio_data = np.array(audio_data, dtype=np.float32)
        
        # Normalize audio data to prevent clipping
        max_val = np.max(np.abs(audio_data))
        # Avoid division by zero
        if max_val > 0:
            # Scale audio to range [-1, 1]
            audio_data = audio_data / max_val
        
        # Extract features from the audio chunk
        features = self._extract_features(audio_data)
        # Log feature extraction completion
        logger.debug(f"Features extracted: shape={features.shape}")
        # Return the processed features
        return features

    # Private method to extract audio features
    def _extract_features(self, audio_data):
        # Calculate the short-time Fourier transform (STFT) of audio
        # Use FFT to convert time-domain to frequency-domain
        fft = np.fft.fft(audio_data)
        # Calculate the magnitude spectrum
        magnitude = np.abs(fft)
        # Normalize magnitude values
        magnitude = magnitude / (len(audio_data) / 2)
        # Return the first half of the magnitude spectrum (positive frequencies)
        return magnitude[:len(magnitude)//2]

    # Method to get all transcriptions collected so far
    def get_transcriptions(self):
        # Return a copy of the transcriptions list
        return self.transcriptions.copy()

    # Method to clear all stored transcriptions
    def clear_transcriptions(self):
        # Empty the transcriptions list
        self.transcriptions = []
        # Log the clearing action
        logger.info("Transcriptions cleared")

    # Method to stop audio processing
    def stop_processing(self):
        # Set the processing flag to False
        self.is_processing = False
        # Log that processing is being stopped
        logger.info("Processing stop signal sent")

    # Method to reset the processor to initial state
    def reset(self):
        # Stop any ongoing processing
        self.stop_processing()
        # Wait a short time for processing to finish
        time.sleep(0.5)
        # Clear all transcriptions
        self.clear_transcriptions()
        # Empty the audio queue
        while not self.audio_queue.empty():
            # Remove items from the queue
            try:
                # Get and discard items from queue
                self.audio_queue.get_nowait()
            # Catch exception if queue becomes empty
            except:
                # Break the loop if queue is empty
                break
        # Log the reset action
        logger.info("Processor reset to initial state")
