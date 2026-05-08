"""
Custom exceptions for the ASR (Automatic Speech Recognition) module.

This module defines custom exception classes for handling various error scenarios
in the ASR pipeline, including audio processing, model loading, transcription,
and configuration errors.

Exception Hierarchy:
    ASRException (base)
    ├── AudioException
    │   ├── InvalidAudioFormatError
    │   ├── AudioProcessingError
    │   └── AudioQueueError
    ├── ModelException
    │   ├── ModelNotFoundError
    │   ├── ModelLoadError
    │   └── UnsupportedModelError
    ├── TranscriptionException
    │   ├── TranscriptionError
    │   ├── TranscriptionTimeoutError
    │   └── LanguageDetectionError
    ├── ConfigurationException
    │   ├── InvalidConfigurationError
    │   └── ConfigurationFileError
    └── ProcessingException
        ├── ProcessingTimeoutError
        ├── ProcessingStateError
        └── ProcessingError
"""


class ASRException(Exception):
    """
    Base exception class for all ASR-related errors.
    
    This is the parent class for all custom exceptions in the ASR module.
    It can be used to catch any ASR-related exception.
    
    Example:
        try:
            transcriber.transcribe("audio.wav")
        except ASRException as e:
            logger.error(f"ASR error occurred: {e}")
    """
    
    def __init__(self, message: str, error_code: str = None):
        """
        Initialize the ASRException.
        
        Args:
            message (str): Human-readable error message
            error_code (str, optional): Machine-readable error code for programmatic handling
        """
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Return formatted error message with error code."""
        return f"[{self.error_code}] {self.message}"


# Audio-related exceptions

class AudioException(ASRException):
    """Base exception for audio processing errors."""
    pass


class InvalidAudioFormatError(AudioException):
    """
    Raised when audio data is in an unsupported format or has invalid properties.
    
    This exception is raised when:
    - Audio file format is not supported (not in SUPPORTED_FORMATS)
    - Audio encoding is incorrect
    - Audio sample rate doesn't match expected rate
    - Audio data structure is invalid
    
    Example:
        try:
            processor.add_audio_chunk(invalid_audio)
        except InvalidAudioFormatError as e:
            logger.error(f"Audio format error: {e}")
    """
    
    def __init__(
        self,
        message: str,
        format_received: str = None,
        format_expected: str = None,
        error_code: str = "INVALID_AUDIO_FORMAT"
    ):
        """
        Initialize InvalidAudioFormatError.
        
        Args:
            message (str): Error message
            format_received (str, optional): The received audio format
            format_expected (str, optional): The expected audio format
            error_code (str): Error code for identification
        """
        self.format_received = format_received
        self.format_expected = format_expected
        super().__init__(message, error_code)


class AudioProcessingError(AudioException):
    """
    Raised when there's an error during audio processing or normalization.
    
    This exception is raised when:
    - Audio data normalization fails
    - Audio chunk processing encounters errors
    - Audio buffer operations fail
    - Resampling or format conversion fails
    
    Example:
        try:
            processor.process_audio()
        except AudioProcessingError as e:
            logger.error(f"Processing failed: {e}")
    """
    
    def __init__(
        self,
        message: str,
        chunk_size: int = None,
        error_code: str = "AUDIO_PROCESSING_ERROR"
    ):
        """
        Initialize AudioProcessingError.
        
        Args:
            message (str): Error message
            chunk_size (int, optional): Size of the audio chunk that failed
            error_code (str): Error code for identification
        """
        self.chunk_size = chunk_size
        super().__init__(message, error_code)


class AudioQueueError(AudioException):
    """
    Raised when there's an error with the audio queue operations.
    
    This exception is raised when:
    - Queue operations timeout
    - Queue capacity is exceeded
    - Queue is in an invalid state
    - Adding/retrieving audio chunks fails
    
    Example:
        try:
            processor.add_audio_chunk(audio_data)
        except AudioQueueError as e:
            logger.error(f"Queue error: {e}")
    """
    
    def __init__(
        self,
        message: str,
        queue_size: int = None,
        error_code: str = "AUDIO_QUEUE_ERROR"
    ):
        """
        Initialize AudioQueueError.
        
        Args:
            message (str): Error message
            queue_size (int, optional): Current queue size when error occurred
            error_code (str): Error code for identification
        """
        self.queue_size = queue_size
        super().__init__(message, error_code)


# Model-related exceptions

class ModelException(ASRException):
    """Base exception for model-related errors."""
    pass


class ModelNotFoundError(ModelException):
    """
    Raised when a required model file cannot be found.
    
    This exception is raised when:
    - Model file doesn't exist at the specified path
    - Model cache directory is missing
    - Pre-trained model cannot be downloaded
    
    Example:
        try:
            transcriber = Transcriber(model_path="/nonexistent/path")
        except ModelNotFoundError as e:
            logger.error(f"Model not found: {e}")
    """
    
    def __init__(
        self,
        message: str,
        model_name: str = None,
        model_path: str = None,
        error_code: str = "MODEL_NOT_FOUND"
    ):
        """
        Initialize ModelNotFoundError.
        
        Args:
            message (str): Error message
            model_name (str, optional): Name of the missing model
            model_path (str, optional): Path where model was expected
            error_code (str): Error code for identification
        """
        self.model_name = model_name
        self.model_path = model_path
        super().__init__(message, error_code)


class ModelLoadError(ModelException):
    """
    Raised when there's an error loading or initializing a model.
    
    This exception is raised when:
    - Model file is corrupted or incomplete
    - Model initialization fails
    - Required dependencies for model are missing
    - Model checksum validation fails
    
    Example:
        try:
            transcriber.load_model()
        except ModelLoadError as e:
            logger.error(f"Failed to load model: {e}")
    """
    
    def __init__(
        self,
        message: str,
        model_name: str = None,
        root_cause: Exception = None,
        error_code: str = "MODEL_LOAD_ERROR"
    ):
        """
        Initialize ModelLoadError.
        
        Args:
            message (str): Error message
            model_name (str, optional): Name of the model that failed to load
            root_cause (Exception, optional): The original exception that caused this
            error_code (str): Error code for identification
        """
        self.model_name = model_name
        self.root_cause = root_cause
        super().__init__(message, error_code)


class UnsupportedModelError(ModelException):
    """
    Raised when an unsupported model type or version is requested.
    
    This exception is raised when:
    - Model type is not recognized
    - Model version is not supported
    - Model size is not available
    - Requested model is deprecated
    
    Example:
        try:
            transcriber = Transcriber(model_name="unknown-model")
        except UnsupportedModelError as e:
            logger.error(f"Unsupported model: {e}")
    """
    
    def __init__(
        self,
        message: str,
        model_name: str = None,
        supported_models: list = None,
        error_code: str = "UNSUPPORTED_MODEL"
    ):
        """
        Initialize UnsupportedModelError.
        
        Args:
            message (str): Error message
            model_name (str, optional): Name of the unsupported model
            supported_models (list, optional): List of supported models
            error_code (str): Error code for identification
        """
        self.model_name = model_name
        self.supported_models = supported_models or []
        super().__init__(message, error_code)


# Transcription-related exceptions

class TranscriptionException(ASRException):
    """Base exception for transcription-related errors."""
    pass


class TranscriptionError(TranscriptionException):
    """
    Raised when transcription of audio fails.
    
    This exception is raised when:
    - Whisper model fails to transcribe audio
    - Audio is too noisy or unclear
    - Transcription process encounters an error
    - Model inference fails
    
    Example:
        try:
            result = transcriber.transcribe("audio.wav")
        except TranscriptionError as e:
            logger.error(f"Transcription failed: {e}")
    """
    
    def __init__(
        self,
        message: str,
        audio_duration: float = None,
        audio_file: str = None,
        error_code: str = "TRANSCRIPTION_ERROR"
    ):
        """
        Initialize TranscriptionError.
        
        Args:
            message (str): Error message
            audio_duration (float, optional): Duration of audio that failed to transcribe (in seconds)
            audio_file (str, optional): Path to the audio file
            error_code (str): Error code for identification
        """
        self.audio_duration = audio_duration
        self.audio_file = audio_file
        super().__init__(message, error_code)


class TranscriptionTimeoutError(TranscriptionException):
    """
    Raised when transcription takes longer than the configured timeout.
    
    This exception is raised when:
    - Transcription processing exceeds maximum allowed time
    - Model inference takes too long
    - Audio processing timeout is exceeded
    - Network request for model download times out
    
    Example:
        try:
            result = transcriber.transcribe("long_audio.wav", timeout=30)
        except TranscriptionTimeoutError as e:
            logger.error(f"Transcription timed out: {e}")
    """
    
    def __init__(
        self,
        message: str,
        timeout_seconds: float = None,
        audio_file: str = None,
        error_code: str = "TRANSCRIPTION_TIMEOUT"
    ):
        """
        Initialize TranscriptionTimeoutError.
        
        Args:
            message (str): Error message
            timeout_seconds (float, optional): The timeout value that was exceeded
            audio_file (str, optional): Path to the audio file being transcribed
            error_code (str): Error code for identification
        """
        self.timeout_seconds = timeout_seconds
        self.audio_file = audio_file
        super().__init__(message, error_code)


class LanguageDetectionError(TranscriptionException):
    """
    Raised when language detection fails during transcription.
    
    This exception is raised when:
    - Language cannot be detected from audio
    - Detected language confidence is too low
    - Language detection model fails
    - Specified language is not supported
    
    Example:
        try:
            result = transcriber.transcribe("audio.wav")
        except LanguageDetectionError as e:
            logger.error(f"Language detection failed: {e}")
    """
    
    def __init__(
        self,
        message: str,
        detected_language: str = None,
        confidence: float = None,
        supported_languages: list = None,
        error_code: str = "LANGUAGE_DETECTION_ERROR"
    ):
        """
        Initialize LanguageDetectionError.
        
        Args:
            message (str): Error message
            detected_language (str, optional): The language code that was detected
            confidence (float, optional): Confidence score of detection (0-1)
            supported_languages (list, optional): List of supported languages
            error_code (str): Error code for identification
        """
        self.detected_language = detected_language
        self.confidence = confidence
        self.supported_languages = supported_languages or []
        super().__init__(message, error_code)


# Configuration-related exceptions

class ConfigurationException(ASRException):
    """Base exception for configuration-related errors."""
    pass


class InvalidConfigurationError(ConfigurationException):
    """
    Raised when configuration values are invalid or incompatible.
    
    This exception is raised when:
    - Configuration parameter is out of valid range
    - Required configuration is missing
    - Configuration values are incompatible
    - Type validation fails
    
    Example:
        try:
            processor = ASRProcessor(sample_rate=-1)
        except InvalidConfigurationError as e:
            logger.error(f"Invalid configuration: {e}")
    """
    
    def __init__(
        self,
        message: str,
        parameter_name: str = None,
        invalid_value: any = None,
        valid_range: tuple = None,
        error_code: str = "INVALID_CONFIGURATION"
    ):
        """
        Initialize InvalidConfigurationError.
        
        Args:
            message (str): Error message
            parameter_name (str, optional): Name of the invalid parameter
            invalid_value (any, optional): The invalid value that was provided
            valid_range (tuple, optional): Tuple of (min, max) valid values
            error_code (str): Error code for identification
        """
        self.parameter_name = parameter_name
        self.invalid_value = invalid_value
        self.valid_range = valid_range
        super().__init__(message, error_code)


class ConfigurationFileError(ConfigurationException):
    """
    Raised when there's an error reading or parsing a configuration file.
    
    This exception is raised when:
    - Configuration file doesn't exist
    - Configuration file is malformed (invalid JSON/YAML)
    - Required config file keys are missing
    - Configuration file encoding is invalid
    
    Example:
        try:
            config = load_config("config.yaml")
        except ConfigurationFileError as e:
            logger.error(f"Configuration file error: {e}")
    """
    
    def __init__(
        self,
        message: str,
        config_file: str = None,
        root_cause: Exception = None,
        error_code: str = "CONFIGURATION_FILE_ERROR"
    ):
        """
        Initialize ConfigurationFileError.
        
        Args:
            message (str): Error message
            config_file (str, optional): Path to the configuration file
            root_cause (Exception, optional): The original exception that caused this
            error_code (str): Error code for identification
        """
        self.config_file = config_file
        self.root_cause = root_cause
        super().__init__(message, error_code)


# Processing-related exceptions

class ProcessingException(ASRException):
    """Base exception for processing-related errors."""
    pass


class ProcessingTimeoutError(ProcessingException):
    """
    Raised when audio processing exceeds the timeout limit.
    
    This exception is raised when:
    - Processing of audio chunks takes too long
    - Worker thread processing timeout is exceeded
    - No progress is made within timeout period
    
    Example:
        try:
            processor.process_audio()
        except ProcessingTimeoutError as e:
            logger.error(f"Processing timed out: {e}")
    """
    
    def __init__(
        self,
        message: str,
        timeout_seconds: float = None,
        chunks_processed: int = None,
        error_code: str = "PROCESSING_TIMEOUT"
    ):
        """
        Initialize ProcessingTimeoutError.
        
        Args:
            message (str): Error message
            timeout_seconds (float, optional): The timeout value that was exceeded
            chunks_processed (int, optional): Number of chunks processed before timeout
            error_code (str): Error code for identification
        """
        self.timeout_seconds = timeout_seconds
        self.chunks_processed = chunks_processed
        super().__init__(message, error_code)


class ProcessingStateError(ProcessingException):
    """
    Raised when processing is attempted in an invalid state.
    
    This exception is raised when:
    - Processing is already running
    - Trying to process without initialization
    - Processing state is inconsistent
    - Operations are attempted on stopped processor
    
    Example:
        try:
            processor.start()
            processor.start()  # Error: already started
        except ProcessingStateError as e:
            logger.error(f"Invalid processing state: {e}")
    """
    
    def __init__(
        self,
        message: str,
        current_state: str = None,
        expected_state: str = None,
        error_code: str = "PROCESSING_STATE_ERROR"
    ):
        """
        Initialize ProcessingStateError.
        
        Args:
            message (str): Error message
            current_state (str, optional): The current processor state
            expected_state (str, optional): The expected processor state
            error_code (str): Error code for identification
        """
        self.current_state = current_state
        self.expected_state = expected_state
        super().__init__(message, error_code)


class ProcessingError(ProcessingException):
    """
    Raised when a general error occurs during audio processing.
    
    This exception is raised when:
    - Unexpected error during processing loop
    - Worker thread encounters an error
    - Resource allocation fails
    - Unknown processing error
    
    Example:
        try:
            processor.process_audio()
        except ProcessingError as e:
            logger.error(f"Processing error: {e}")
    """
    
    def __init__(
        self,
        message: str,
        root_cause: Exception = None,
        error_code: str = "PROCESSING_ERROR"
    ):
        """
        Initialize ProcessingError.
        
        Args:
            message (str): Error message
            root_cause (Exception, optional): The original exception that caused this
            error_code (str): Error code for identification
        """
        self.root_cause = root_cause
        super().__init__(message, error_code)
