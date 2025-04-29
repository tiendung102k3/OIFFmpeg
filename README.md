# OIFFmpeg: A Simple Python Wrapper for FFmpeg

OIFFmpeg provides a straightforward Python interface for common tasks performed using the powerful FFmpeg multimedia framework. This library aims to simplify the execution of FFmpeg commands for operations like media format conversion, audio extraction, video trimming, retrieving media information, and streaming, directly from your Python scripts. It leverages the standard `subprocess` module to interact with the FFmpeg command-line tools (`ffmpeg` and `ffprobe`), requiring them to be installed and accessible in your system's PATH.

## Features

Currently, OIFFmpeg supports the following core functionalities:

*   **Media Conversion:** Convert video and audio files between various formats (`convert`).
*   **Audio Extraction:** Easily extract the audio track from a media file (`extract_audio`).
*   **Video Trimming:** Cut sections from video files based on start and end times (`trim_video`).
*   **Media Information Retrieval:** Get detailed information about media files using `ffprobe` (`get_media_info`).
*   **RTMP Streaming:** Stream a video file or URL to an RTMP server (`stream_video`).
*   **General FFmpeg Execution:** Run any custom FFmpeg command by providing a list of arguments (`run_ffmpeg`), offering maximum flexibility for advanced users.

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

Once FFmpeg is installed, you can install OIFFmpeg using pip:

```bash
pip install oiffmpeg
```

To install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/tiendung102k3/OIFFmpeg.git
```

## Usage Examples

Here are some examples demonstrating how to use OIFFmpeg:

```python
import oiffmpeg
import json

# --- Example Input/Output (replace with your actual paths/URLs) ---
input_video_file = 'local_video.mp4' # Example local file
input_video_url = 'http://example.com/stream.m3u8' # Example URL
output_video_webm = 'output.webm'
output_audio_mp3 = 'output_audio.mp3'
output_trimmed_video = 'trimmed_video.mp4'
rtmp_endpoint = 'rtmp://your-rtmp-server.com/live/stream_key' # Example RTMP URL

# --- 1. Convert Video Format (MP4 to WebM) ---
try:
    print(f"Converting {input_video_file} to {output_video_webm}...")
    success = oiffmpeg.convert(input_video_file, output_video_webm, vcodec='libvpx', acodec='libvorbis', overwrite=True)
    print(f"Conversion {'successful' if success else 'failed'}.")
except Exception as e:
    print(f"An error occurred during conversion: {e}")

# --- 2. Extract Audio (from MP4 to MP3) ---
try:
    print(f"Extracting audio from {input_video_file} to {output_audio_mp3}...")
    success = oiffmpeg.extract_audio(input_video_file, output_audio_mp3, audio_codec='libmp3lame', overwrite=True)
    print(f"Audio extraction {'successful' if success else 'failed'}.")
except Exception as e:
    print(f"An error occurred during audio extraction: {e}")

# --- 3. Trim Video (from 10s to 30s) ---
try:
    start = 10
    end = 30
    print(f"Trimming {input_video_file} from {start}s to {end}s into {output_trimmed_video}...")
    success = oiffmpeg.trim_video(input_video_file, output_trimmed_video, start_time=start, end_time=end, overwrite=True)
    print(f"Video trimming {'successful' if success else 'failed'}.")
except Exception as e:
    print(f"An error occurred during video trimming: {e}")

# --- 4. Get Media Information ---
try:
    print(f"Getting media info for {input_video_file}...")
    media_info = oiffmpeg.get_media_info(input_video_file)
    if media_info:
        print("Media information retrieved successfully:")
        print(json.dumps(media_info, indent=2))
    else:
        print("Failed to retrieve media information.")
except Exception as e:
    print(f"An error occurred while getting media info: {e}")

# --- 5. Stream Video to RTMP (from local file) ---
# Note: This will run until the stream ends or is interrupted (e.g., Ctrl+C)
try:
    print(f"Streaming {input_video_file} to {rtmp_endpoint}...")
    # Common streaming options: re=True (read at native rate), c='copy' (no re-encoding), f='flv' (format)
    success = oiffmpeg.stream_video(input_video_file, rtmp_endpoint, re=True, c='copy', f='flv')
    # If re-encoding is needed (e.g., for specific bitrate/codec):
    # success = oiffmpeg.stream_video(input_video_file, rtmp_endpoint, re=True,
    #                                 vcodec='libx264', preset='veryfast', tune='zerolatency',
    #                                 acodec='aac', ab='128k',
    #                                 f='flv', bufsiz='1000k', maxrate='500k')
    print(f"Streaming finished. Success: {success}")
except Exception as e:
    print(f"An error occurred during streaming: {e}")

# --- 6. Use General run_ffmpeg for Advanced Tasks ---
# Example: Add a watermark image to a video
try:
    print("Adding watermark using run_ffmpeg...")
    watermark_image = 'logo.png' # Path to your watermark image
    output_watermarked = 'output_watermarked.mp4'
    ffmpeg_args = [
        '-i', input_video_file,
        '-i', watermark_image,
        '-filter_complex', 'overlay=W-w-10:10', # Position watermark: 10px from top-right
        '-codec:a', 'copy', # Copy audio stream
        '-y', # Overwrite output if exists
        output_watermarked
    ]
    success = oiffmpeg.run_ffmpeg(ffmpeg_args)
    print(f"Watermarking {'successful' if success else 'failed'}.")
except Exception as e:
    print(f"An error occurred during watermarking: {e}")

# Example: Stream from webcam to RTMP (requires webcam access & correct input format)
# Note: Input format/device name varies by OS ('/dev/video0' on Linux, 'avfoundation' on macOS, 'dshow' on Windows)
# This example is illustrative and might need adjustments for your system.
try:
    print(f"Streaming from webcam to {rtmp_endpoint} (Illustrative Example)...")
    # Example for Linux, adjust '-i' and '-f' for your OS/device
    webcam_args = [
        '-f', 'v4l2', '-i', '/dev/video0', # Input from webcam
        # Add audio input if needed: '-f', 'alsa', '-i', 'default',
        '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
        '-c:a', 'aac', '-b:a', '128k',
        '-f', 'flv',
        rtmp_endpoint
    ]
    # success = oiffmpeg.run_ffmpeg(webcam_args) # Uncomment to run
    # print(f"Webcam streaming finished. Success: {success}")
    print("Webcam streaming example skipped (requires specific setup).")
except Exception as e:
    print(f"An error occurred during webcam streaming example: {e}")

```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on the GitHub repository ([https://github.com/tiendung102k3/OIFFmpeg/issues](https://github.com/tiendung102k3/OIFFmpeg/issues)). Pull requests are also appreciated.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

