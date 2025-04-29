"""
OIFFmpeg - A Python wrapper for FFmpeg CLI operations.

This module provides utility functions for common FFmpeg operations.
"""

import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_ffmpeg_installed():
    """Checks if FFmpeg is installed and available in the system PATH.
    
    Returns:
        bool: True if FFmpeg is installed, False otherwise.
    """
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def ensure_directory_exists(file_path):
    """Ensures that the directory for the given file path exists.
    
    Args:
        file_path (str): Path to a file.
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")

def format_time(seconds):
    """Converts seconds to HH:MM:SS.ms format.
    
    Args:
        seconds (float): Time in seconds.
        
    Returns:
        str: Time in HH:MM:SS.ms format.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
