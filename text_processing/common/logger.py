"""
Logging Configuration for Smart Document Assistant
Centralized logging for all modules
"""

import logging
import sys
from pathlib import Path
from config.settings import LOGGING_CONFIG

def setup_logger(module_name: str) -> logging.Logger:
    """
    Setup logger for a specific module
    
    Args:
        module_name: Name of the module (e.g., 'text_extraction', 'text_preprocessing')
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(module_name)
    
    if not logger.handlers:  # Avoid duplicate handlers
        logger.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
        
        # File Handler
        log_file = Path(LOGGING_CONFIG["log_file"])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
        
        # Formatter
        formatter = logging.Formatter(LOGGING_CONFIG["format"])
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# Create root logger
root_logger = setup_logger("SmartDocumentAssistant")
