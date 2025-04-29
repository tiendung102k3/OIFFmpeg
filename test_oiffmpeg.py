"""
Test script for OIFFmpeg library functionality.
This script creates a simple test video and tests the core functions.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Define project root directory relative to this script's location
PROJECT_ROOT = Path(__file__).parent.resolve()

# Add the project root to sys.path to import the package
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from oiffmpeg import convert, extract_audio, trim_video, get_media_info
    print("Successfully imported OIFFmpeg library")
except ImportError as e:
    print(f"Error importing OIFFmpeg: {e}")
    sys.exit(1)

def create_test_video(output_dir):
    """Create a simple test video using FFmpeg in the specified directory."""
    print("Creating test video...")
    test_video = output_dir / "test_video.mp4"

    # Create a 10-second test video with color bars AND a silent audio track
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc=duration=10:size=640x480:rate=30", # Video source
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", # Silent audio source
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", # Add AAC audio codec
        "-shortest", # Finish encoding when the shortest input stream ends
        str(test_video)
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Created test video: {test_video}")
        return test_video
    except subprocess.CalledProcessError as e:
        print(f"Error creating test video: {e}")
        print(f"Stderr: {e.stderr.decode()}")
        return None

def test_convert(input_file, output_dir):
    """Test the convert function."""
    print("\nTesting convert function...")
    output_file = output_dir / "test_converted.webm"

    try:
        result = convert(str(input_file), str(output_file), vcodec="libvpx", acodec="libvorbis")
        if result and output_file.exists():
            print(f"✓ Convert test passed: {output_file} created successfully")
            return True
        else:
            print("✗ Convert test failed")
            return False
    except Exception as e:
        print(f"✗ Convert test failed with error: {e}")
        return False

def test_extract_audio(input_file, output_dir):
    """Test the extract_audio function."""
    print("\nTesting extract_audio function...")
    output_file = output_dir / "test_audio.mp3"

    try:
        result = extract_audio(str(input_file), str(output_file), audio_codec="libmp3lame")
        if result and output_file.exists():
            print(f"✓ Extract audio test passed: {output_file} created successfully")
            return True
        else:
            print("✗ Extract audio test failed")
            return False
    except Exception as e:
        print(f"✗ Extract audio test failed with error: {e}")
        return False

def test_trim_video(input_file, output_dir):
    """Test the trim_video function."""
    print("\nTesting trim_video function...")
    output_file = output_dir / "test_trimmed.mp4"

    try:
        result = trim_video(str(input_file), str(output_file), start_time=2, end_time=5)
        if result and output_file.exists():
            print(f"✓ Trim video test passed: {output_file} created successfully")
            return True
        else:
            print("✗ Trim video test failed")
            return False
    except Exception as e:
        print(f"✗ Trim video test failed with error: {e}")
        return False

def test_get_media_info(input_file):
    """Test the get_media_info function."""
    print("\nTesting get_media_info function...")

    try:
        media_info = get_media_info(str(input_file))
        if media_info:
            print("✓ Get media info test passed")
            print(f"  Format: {media_info.get('format', {}).get('format_name')}")
            print(f"  Duration: {media_info.get('format', {}).get('duration')} seconds")

            # Print stream info
            for i, stream in enumerate(media_info.get('streams', [])):
                print(f"  Stream {i}: {stream.get('codec_type')} - {stream.get('codec_name')}")

            return True
        else:
            print("✗ Get media info test failed")
            return False
    except Exception as e:
        print(f"✗ Get media info test failed with error: {e}")
        return False

def test_build_package():
    """Test building the package from the project root."""
    print("\nTesting package build...")

    try:
        # Ensure we are in the project root directory
        print(f"Building package in directory: {PROJECT_ROOT}")

        # Build the package using the build module
        result = subprocess.run(
            [sys.executable, "-m", "build", "--wheel"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=PROJECT_ROOT # Explicitly set the working directory
        )

        # Check if the wheel file was created in the dist directory
        dist_dir = PROJECT_ROOT / "dist"
        if dist_dir.exists() and list(dist_dir.glob("*.whl")):
            print(f"✓ Package build test passed. Wheel file created in: {dist_dir}")
            return True
        else:
            print("✗ Package build test failed: No wheel file found in dist directory")
            print(f"  stdout: {result.stdout}")
            print(f"  stderr: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Package build test failed with error: {e}")
        print(f"  stdout: {e.stdout}")
        print(f"  stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ Package build test failed with unexpected error: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting OIFFmpeg tests...")

    # Create test directory inside project root
    test_dir = PROJECT_ROOT / "test_output"
    test_dir.mkdir(exist_ok=True)
    print(f"Test output directory: {test_dir}")

    # Create test video with audio
    test_video_path = create_test_video(test_dir)
    if not test_video_path:
        print("Failed to create test video. Exiting tests.")
        return False

    # Run tests
    tests = [
        test_convert(test_video_path, test_dir),
        test_extract_audio(test_video_path, test_dir),
        test_trim_video(test_video_path, test_dir),
        test_get_media_info(test_video_path),
        test_build_package()
    ]

    # Print summary
    print("\nTest Summary:")
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {tests.count(True)}")
    print(f"Failed: {tests.count(False)}")

    # Clean up test files (optional)
    # print("\nCleaning up test files...")
    # for item in test_dir.iterdir():
    #     item.unlink()
    # test_dir.rmdir()

    return all(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

