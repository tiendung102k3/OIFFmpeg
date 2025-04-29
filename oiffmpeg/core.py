# -*- coding: utf-8 -*-
"""Core FFmpeg command execution logic."""

import subprocess
import json
import shlex
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _run_ffmpeg_command(command_list):
    """Runs an FFmpeg command using subprocess.

    Args:
        command_list: A list of strings representing the command and its arguments.

    Returns:
        A tuple (return_code, stdout, stderr).
    """
    command_str = shlex.join(command_list) # Use shlex.join for safer command string representation
    logging.info(f"Running FFmpeg command: {command_str}")
    try:
        process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True # Decode stdout/stderr as text
        )
        stdout, stderr = process.communicate()
        logging.info(f"FFmpeg command finished with code: {process.returncode}")
        if process.returncode != 0:
            logging.error(f"FFmpeg Error Output:\n{stderr}")
        # else:
            # logging.debug(f"FFmpeg Output:\n{stdout}") # Avoid logging potentially large stdout
        return process.returncode, stdout, stderr
    except FileNotFoundError:
        logging.error("FFmpeg command not found. Make sure FFmpeg is installed and in your PATH.")
        raise RuntimeError("FFmpeg not found. Please install FFmpeg.")
    except Exception as e:
        logging.error(f"An error occurred while running FFmpeg: {e}")
        raise

def convert(input_file, output_file, **kwargs):
    """Converts a media file to a different format.

    Args:
        input_file: Path to the input media file.
        output_file: Path to the desired output media file.
        **kwargs: Additional FFmpeg options (e.g., vcodec='libx264', acodec='aac').
                  Boolean flags should be passed as True (e.g., overwrite=True for -y).

    Returns:
        True if conversion was successful (exit code 0), False otherwise.
    """
    command = ['ffmpeg']
    if kwargs.pop('overwrite', True): # Default to overwrite
        command.append('-y')
    command.extend(['-i', input_file])

    # Add custom options
    for key, value in kwargs.items():
        if isinstance(value, bool) and value:
             command.append(f'-{key}') # Handle boolean flags like -an, -vn
        elif value is not None:
            command.extend([f'-{key}', str(value)])

    command.append(output_file)

    ret_code, _, stderr = _run_ffmpeg_command(command)
    return ret_code == 0

def extract_audio(input_file, output_file, audio_codec='aac', overwrite=True):
    """Extracts the audio stream from a media file.

    Args:
        input_file: Path to the input media file.
        output_file: Path to the desired output audio file.
        audio_codec: The audio codec to use for the output (default: 'aac').
        overwrite: Whether to overwrite the output file if it exists (default: True).

    Returns:
        True if extraction was successful (exit code 0), False otherwise.
    """
    command = ['ffmpeg']
    if overwrite:
        command.append('-y')
    command.extend(['-i', input_file, '-vn', '-acodec', audio_codec, output_file])
    ret_code, _, stderr = _run_ffmpeg_command(command)
    return ret_code == 0

def trim_video(input_file, output_file, start_time, end_time, re_encode=True, overwrite=True, **kwargs):
    """Trims a video file to the specified time range.

    Args:
        input_file: Path to the input video file.
        output_file: Path to the desired output trimmed video file.
        start_time: Start time in seconds or HH:MM:SS.ms format.
        end_time: End time in seconds or HH:MM:SS.ms format.
        re_encode: If True (default), re-encodes the video. If False, attempts
                   to copy codecs (-c copy) for faster trimming, which might be less accurate.
        overwrite: Whether to overwrite the output file if it exists (default: True).
        **kwargs: Additional FFmpeg options passed during re-encoding (ignored if re_encode=False).

    Returns:
        True if trimming was successful (exit code 0), False otherwise.
    """
    command = ['ffmpeg']
    if overwrite:
        command.append('-y')

    command.extend(['-i', input_file, '-ss', str(start_time), '-to', str(end_time)])

    if re_encode:
        # Add custom options if re-encoding
        for key, value in kwargs.items():
             if isinstance(value, bool) and value:
                 command.append(f'-{key}')
             elif value is not None:
                command.extend([f'-{key}', str(value)])
    else:
        command.extend(['-c', 'copy']) # Use stream copy for speed if not re-encoding

    command.append(output_file)

    ret_code, _, stderr = _run_ffmpeg_command(command)
    return ret_code == 0

def get_media_info(input_file):
    """Retrieves media information using ffprobe.

    Args:
        input_file: Path to the input media file.

    Returns:
        A dictionary containing media information, or None if an error occurs.
    """
    command = [
        'ffprobe',
        '-v', 'quiet',             # Suppress logging
        '-print_format', 'json',   # Output format
        '-show_format',            # Show format information
        '-show_streams',           # Show stream information
        input_file
    ]
    command_str = shlex.join(command)
    logging.info(f"Running ffprobe command: {command_str}")
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse ffprobe JSON output: {e}\nOutput:\n{stdout}")
                return None
        else:
            logging.error(f"ffprobe command failed with code {process.returncode}. Error:\n{stderr}")
            return None
    except FileNotFoundError:
        logging.error("ffprobe command not found. Make sure FFmpeg (which includes ffprobe) is installed and in your PATH.")
        raise RuntimeError("ffprobe not found. Please install FFmpeg.")
    except Exception as e:
        logging.error(f"An error occurred while running ffprobe: {e}")
        raise

