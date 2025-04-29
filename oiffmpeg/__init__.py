"""
OIFFmpeg - A Python wrapper for FFmpeg CLI operations.

This library provides a simple interface to common FFmpeg operations,
plus a general function to run arbitrary FFmpeg commands.
"""

from .core import convert, extract_audio, trim_video, get_media_info, stream_video, run_ffmpeg

__version__ = '0.2.0'
__all__ = [
    'convert',
    'extract_audio',
    'trim_video',
    'get_media_info',
    'stream_video',
    'run_ffmpeg'
]

