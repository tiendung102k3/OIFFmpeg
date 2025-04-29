"""
OIFFmpeg - A Python wrapper for FFmpeg CLI operations.

This library provides a simple interface to common FFmpeg operations.
"""

from .core import convert, extract_audio, trim_video, get_media_info

__version__ = '0.1.0'
__all__ = ['convert', 'extract_audio', 'trim_video', 'get_media_info']
