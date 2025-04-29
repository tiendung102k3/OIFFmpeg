# OIFFmpeg: A Simple Python Wrapper for FFmpeg

OIFFmpeg provides a straightforward Python interface for common tasks performed using the powerful FFmpeg multimedia framework. This library aims to simplify the execution of FFmpeg commands for operations like media format conversion, audio extraction, video trimming, and retrieving media information, directly from your Python scripts. It leverages the standard `subprocess` module to interact with the FFmpeg command-line tools (`ffmpeg` and `ffprobe`), requiring them to be installed and accessible in your system's PATH.

## Features

Currently, OIFFmpeg supports the following core functionalities:

*   **Media Conversion:** Convert video and audio files between various formats. You can specify codecs and other FFmpeg parameters as needed.
*   **Audio Extraction:** Easily extract the audio track from a video file and save it as a separate audio file (e.g., MP3, AAC).
*   **Video Trimming:** Cut sections from video files based on start and end times. Offers options for fast trimming (stream copy) or re-encoding for potentially higher accuracy.
*   **Media Information Retrieval:** Get detailed information about media files, including format details, duration, codecs, bitrates, and stream properties, parsed conveniently into a Python dictionary using `ffprobe`.

## Installation

**Prerequisites:**

Before installing OIFFmpeg, you must have FFmpeg installed on your system. FFmpeg includes both the `ffmpeg` and `ffprobe` command-line tools, which this library relies on. You can download FFmpeg from the official website ([https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)) or install it using your system's package manager.

*   **On Debian/Ubuntu:**
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```
*   **On macOS (using Homebrew):**
    ```bash
    brew install ffmpeg
    ```
*   **On Windows:** Download the pre-built binaries and add the `bin` directory to your system's PATH environment variable.

**Installing OIFFmpeg:**

Once FFmpeg is installed, you can install OIFFmpeg using pip (after it's published to PyPI):

```bash
pip install oiffmpeg
```

Alternatively, you can install it directly from the source code if you clone the repository:

```bash
git clone <repository_url> # Replace with actual GitHub URL later
cd OIFFmpeg
pip install .
```

## Usage Examples

Here are some basic examples demonstrating how to use OIFFmpeg:

```python
import oiffmpeg
import json

# --- Ensure FFmpeg is installed (optional check) ---
# from oiffmpeg.utils import check_ffmpeg_installed
# if not check_ffmpeg_installed():
#     print("Error: FFmpeg is not installed or not in PATH.")
#     exit()

# --- Example Input/Output Files (replace with your actual paths) ---
input_video = 'input.mp4'
output_video_webm = 'output.webm'
output_audio_mp3 = 'output_audio.mp3'
output_trimmed_video = 'trimmed_video.mp4'

# --- 1. Convert Video Format (MP4 to WebM) ---
try:
    print(f"Converting {input_video} to {output_video_webm}...")
    success = oiffmpeg.convert(input_video, output_video_webm, vcodec='libvpx', acodec='libvorbis', overwrite=True)
    if success:
        print("Conversion successful!")
    else:
        print("Conversion failed.")
except Exception as e:
    print(f"An error occurred during conversion: {e}")

# --- 2. Extract Audio (from MP4 to MP3) ---
try:
    print(f"Extracting audio from {input_video} to {output_audio_mp3}...")
    success = oiffmpeg.extract_audio(input_video, output_audio_mp3, audio_codec='libmp3lame', overwrite=True)
    if success:
        print("Audio extraction successful!")
    else:
        print("Audio extraction failed.")
except Exception as e:
    print(f"An error occurred during audio extraction: {e}")

# --- 3. Trim Video (from 10s to 30s) ---
try:
    start = 10  # Start time in seconds
    end = 30    # End time in seconds
    print(f"Trimming {input_video} from {start}s to {end}s into {output_trimmed_video}...")
    # Using re_encode=True (default) for better accuracy
    success = oiffmpeg.trim_video(input_video, output_trimmed_video, start_time=start, end_time=end, overwrite=True)
    # For faster, potentially less accurate trimming (codec copy):
    # success = oiffmpeg.trim_video(input_video, output_trimmed_video, start_time=start, end_time=end, re_encode=False, overwrite=True)
    if success:
        print("Video trimming successful!")
    else:
        print("Video trimming failed.")
except Exception as e:
    print(f"An error occurred during video trimming: {e}")

# --- 4. Get Media Information ---
try:
    print(f"Getting media info for {input_video}...")
    media_info = oiffmpeg.get_media_info(input_video)
    if media_info:
        print("Media information retrieved successfully:")
        # Pretty print the JSON information
        print(json.dumps(media_info, indent=4))
        
        # Example: Access specific information
        duration = float(media_info.get('format', {}).get('duration', 0))
        print(f"\nDuration: {duration:.2f} seconds")
        
        video_streams = [s for s in media_info.get('streams', []) if s.get('codec_type') == 'video']
        if video_streams:
            print(f"Video Codec: {video_streams[0].get('codec_name')}")
            print(f"Resolution: {video_streams[0].get('width')}x{video_streams[0].get('height')}")
            
    else:
        print("Failed to retrieve media information.")
except Exception as e:
    print(f"An error occurred while getting media info: {e}")

```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on the GitHub repository. Pull requests are also appreciated.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

