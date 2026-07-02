import os
import logging
from pathlib import Path
from typing import Optional
import whisper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WhisperModelManager:
    """
    Manages Whisper model loading, caching, and transcription.
    
    Attributes:
        model_size (str): Size of the model (tiny, base, small, medium, large)
        device (str): Computing device (cpu or cuda)
        language (str): Target language for transcription
        model (whisper.Whisper): Loaded Whisper model instance
        model_dir (Path): Directory for storing models
    """
    
    # Valid model sizes and their approximate sizes
    VALID_MODELS = {
        'tiny': {'size': '39M', 'params': 39_000_000},
        'base': {'size': '140M', 'params': 140_000_000},
        'small': {'size': '244M', 'params': 244_000_000},
        'medium': {'size': '769M', 'params': 769_000_000},
        'large': {'size': '1550M', 'params': 1_550_000_000},
    }
    
    def __init__(
        self,
        model_size: str = None,
        device: str = None,
        language: str = None,
        model_dir: str = './offline_models'
    ):
       
        # Load from environment if not provided
        self.model_size = model_size or os.getenv('MODEL_SIZE', 'medium')
        self.device = device or os.getenv('DEVICE', 'cpu')
        self.language = language or os.getenv('LANGUAGE', 'en')
        self.model_dir = Path(model_dir)
        self.model = None
        
        # Validate model size
        if self.model_size not in self.VALID_MODELS:
            logger.warning(
                f"Invalid model size '{self.model_size}'. "
                f"Valid options: {list(self.VALID_MODELS.keys())}. "
                f"Using 'base' as default."
            )
            self.model_size = 'base'
        
        # Create model directory if it doesn't exist
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(
            f"WhisperModelManager initialized: "
            f"model={self.model_size}, device={self.device}, language={self.language}"
        )
    
    def load_model(self) -> whisper.Whisper:
        
        if self.model is not None:
            logger.info("Model already loaded, returning cached instance.")
            return self.model
        
        try:
            logger.info(f"Loading Whisper model: {self.model_size} on {self.device}...")
            
            # Set offline mode (use locally downloaded models)
            os.environ['WHISPER_CACHE'] = str(self.model_dir)
            
            # Load model
            self.model = whisper.load_model(
                self.model_size,
                device=self.device
            )
            
            model_info = self.VALID_MODELS[self.model_size]
            logger.info(
                f"Successfully loaded {self.model_size} model "
                f"(~{model_info['size']}) on {self.device}"
            )
            
            return self.model
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise RuntimeError(f"Model loading failed: {str(e)}")
    
    def unload_model(self) -> None:
        """Unload the model and free memory."""
        if self.model is not None:
            self.model = None
            logger.info("Model unloaded from memory")
    
    def get_model_info(self) -> dict:
        """
        Get information about the current model configuration.
        
        Returns:
            dict: Model configuration information
        """
        model_info = self.VALID_MODELS.get(self.model_size, {})
        
        return {
            'model_size': self.model_size,
            'approximate_size': model_info.get('size', 'Unknown'),
            'parameters': model_info.get('params', 0),
            'device': self.device,
            'language': self.language,
            'model_dir': str(self.model_dir),
            'model_loaded': self.model is not None
        }
    
    def list_downloaded_models(self) -> list:
        """
        List all downloaded models in the model directory.
        
        Returns:
            list: List of downloaded model files
        """
        if not self.model_dir.exists():
            return []
        
        models = list(self.model_dir.glob('*.pt'))
        logger.info(f"Found {len(models)} downloaded model(s)")
        return [str(m) for m in models]
    
    def get_device_info(self) -> dict:
        """
        Get information about the computing device.
        
        Returns:
            dict: Device configuration information
        """
        import torch
        
        device_info = {
            'device': self.device,
            'torch_version': torch.__version__,
            'cuda_available': torch.cuda.is_available(),
        }
        
        if torch.cuda.is_available() and self.device == 'cuda':
            device_info.update({
                'cuda_version': torch.version.cuda,
                'gpu_name': torch.cuda.get_device_name(0),
                'gpu_memory_gb': torch.cuda.get_device_properties(0).total_memory / 1e9
            })
        
        return device_info


def get_default_model() -> whisper.Whisper:
    """
    Get or create a default Whisper model instance.
    
    Returns:
        whisper.Whisper: Default Whisper model
    """
    manager = WhisperModelManager()
    return manager.load_model()


# Module-level model manager for convenience
_model_manager: Optional[WhisperModelManager] = None


def initialize_model_manager(
    model_size: str = None,
    device: str = None,
    language: str = None
) -> WhisperModelManager:
    """
    Initialize the module-level model manager.
    
    Args:
        model_size (str): Size of model
        device (str): Computing device
        language (str): Target language
        
    Returns:
        WhisperModelManager: Initialized model manager
    """
    global _model_manager
    _model_manager = WhisperModelManager(
        model_size=model_size,
        device=device,
        language=language
    )
    return _model_manager


def get_model_manager() -> WhisperModelManager:
    """
    Get the module-level model manager.
    
    Returns:
        WhisperModelManager: Model manager instance
    """
    global _model_manager
    if _model_manager is None:
        _model_manager = initialize_model_manager()
    return _model_manager


if __name__ == '__main__':
    # Example usage
    logger.info("Testing WhisperModelManager...")
    
    manager = WhisperModelManager()
    logger.info(f"Model info: {manager.get_model_info()}")
    logger.info(f"Device info: {manager.get_device_info()}")
    
    # Load model
    model = manager.load_model()
    logger.info("Model loaded successfully!")
    
    # List downloaded models
    downloaded = manager.list_downloaded_models()
    logger.info(f"Downloaded models: {downloaded}")
