"""
============================================================
PHASE 1: Offline Speech Recognition System
Model Download Script
============================================================

Script to download Whisper models for offline use.
Run this script once to download models before deployment.

Usage:
    python download_models.py --model base --device cpu
    python download_models.py --model large --device cuda

Author: ASR Development Team
Version: 1.0
Date: May 30, 2026
"""

import os
import sys
import logging
import argparse
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


class ModelDownloader:
    """Handle downloading and verifying Whisper models."""
    
    VALID_MODELS = ['tiny', 'base', 'small', 'medium', 'large']
    MODEL_SIZES = {
        'tiny': '39MB',
        'base': '140MB',
        'small': '244MB',
        'medium': '769MB',
        'large': '1550MB'
    }
    
    def __init__(self, model_dir: str = './offline_models'):
        """
        Initialize the ModelDownloader.
        
        Args:
            model_dir (str): Directory to store models
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
    def download_model(self, model_size: str, device: str = 'cpu') -> bool:
        """
        Download a Whisper model.
        
        Args:
            model_size (str): Size of model (tiny, base, small, medium, large)
            device (str): Computing device (cpu or cuda)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if model_size not in self.VALID_MODELS:
            logger.error(
                f"Invalid model size: {model_size}. "
                f"Valid options: {', '.join(self.VALID_MODELS)}"
            )
            return False
        
        try:
            logger.info(f"Starting download of '{model_size}' model...")
            logger.info(f"Approximate size: {self.MODEL_SIZES.get(model_size, 'Unknown')}")
            logger.info(f"Destination: {self.model_dir}")
            
            # Set cache directory
            os.environ['WHISPER_CACHE'] = str(self.model_dir)
            
            # Download model
            logger.info("This may take a few minutes depending on your internet speed...")
            model = whisper.load_model(model_size, device=device)
            
            logger.info(f"✓ Successfully downloaded '{model_size}' model!")
            logger.info(f"✓ Model saved to: {self.model_dir}")
            
            # List all downloaded models
            self._list_downloaded_models()
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to download model: {str(e)}")
            return False
    
    def download_multiple_models(
        self,
        model_sizes: list,
        device: str = 'cpu'
    ) -> dict:
        """
        Download multiple models.
        
        Args:
            model_sizes (list): List of model sizes to download
            device (str): Computing device
            
        Returns:
            dict: Dictionary with results for each model
        """
        results = {}
        total = len(model_sizes)
        
        logger.info(f"Downloading {total} model(s)...")
        
        for idx, model_size in enumerate(model_sizes, 1):
            logger.info(f"\n[{idx}/{total}] Processing: {model_size}")
            results[model_size] = self.download_model(model_size, device)
        
        return results
    
    def verify_model(self, model_size: str) -> bool:
        """
        Verify that a model is properly downloaded and loadable.
        
        Args:
            model_size (str): Size of model to verify
            
        Returns:
            bool: True if model is valid, False otherwise
        """
        try:
            logger.info(f"Verifying '{model_size}' model...")
            os.environ['WHISPER_CACHE'] = str(self.model_dir)
            
            # Try to load the model
            model = whisper.load_model(model_size, device='cpu')
            logger.info(f"✓ '{model_size}' model verified successfully!")
            return True
            
        except Exception as e:
            logger.error(f"✗ Model verification failed: {str(e)}")
            return False
    
    def verify_all_models(self) -> dict:
        """
        Verify all downloaded models.
        
        Returns:
            dict: Verification results for each model
        """
        results = {}
        for model_size in self.VALID_MODELS:
            results[model_size] = self.verify_model(model_size)
        return results
    
    def _list_downloaded_models(self) -> None:
        """List all downloaded models in the model directory."""
        models = list(self.model_dir.glob('*.pt'))
        if models:
            logger.info(f"Downloaded models in {self.model_dir}:")
            for model_file in models:
                size_mb = model_file.stat().st_size / (1024 * 1024)
                logger.info(f"  - {model_file.name} ({size_mb:.1f} MB)")
        else:
            logger.info(f"No models found in {self.model_dir}")
    
    def get_available_models(self) -> list:
        """
        Get list of available models in the model directory.
        
        Returns:
            list: List of model files
        """
        return [str(m) for m in self.model_dir.glob('*.pt')]
    
    def get_model_size_on_disk(self, model_file: str) -> str:
        """
        Get the size of a model file on disk.
        
        Args:
            model_file (str): Path to model file
            
        Returns:
            str: Human-readable file size
        """
        try:
            size_bytes = Path(model_file).stat().st_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024
            return f"{size_bytes:.1f} TB"
        except Exception:
            return "Unknown"


def main():
    """Main entry point for the download script."""
    parser = argparse.ArgumentParser(
        description='Download Whisper models for offline speech recognition'
    )
    parser.add_argument(
        '--model',
        choices=ModelDownloader.VALID_MODELS,
        default='base',
        help='Model size to download (default: base)'
    )
    parser.add_argument(
        '--models',
        nargs='+',
        help='Download multiple models (e.g., tiny base small)'
    )
    parser.add_argument(
        '--device',
        choices=['cpu', 'cuda'],
        default='cpu',
        help='Computing device (default: cpu)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify downloaded models'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List downloaded models'
    )
    parser.add_argument(
        '--model-dir',
        default='./offline_models',
        help='Directory to store models (default: ./offline_models)'
    )
    
    args = parser.parse_args()
    
    downloader = ModelDownloader(model_dir=args.model_dir)
    
    # List downloaded models
    if args.list:
        logger.info("Available downloaded models:")
        downloader._list_downloaded_models()
        return
    
    # Verify models
    if args.verify:
        logger.info("Verifying downloaded models...")
        results = downloader.verify_all_models()
        logger.info("\nVerification Results:")
        for model, is_valid in results.items():
            status = "✓ Valid" if is_valid else "✗ Invalid"
            logger.info(f"  {model}: {status}")
        return
    
    # Download models
    if args.models:
        results = downloader.download_multiple_models(args.models, args.device)
        logger.info("\nDownload Summary:")
        for model, success in results.items():
            status = "✓ Success" if success else "✗ Failed"
            logger.info(f"  {model}: {status}")
    else:
        downloader.download_model(args.model, args.device)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nDownload interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
