# OIFFmpeg: Một Thư Viện Python Đơn Giản Cho FFmpeg

OIFFmpeg cung cấp một giao diện Python đơn giản cho các tác vụ thường gặp khi sử dụng framework đa phương tiện FFmpeg mạnh mẽ. Thư viện này nhằm đơn giản hóa việc thực thi các lệnh FFmpeg cho các thao tác như chuyển đổi định dạng media, trích xuất âm thanh, cắt video, truy xuất thông tin media và stream, trực tiếp từ các script Python của bạn. Nó sử dụng module `subprocess` tiêu chuẩn để tương tác với các công cụ dòng lệnh FFmpeg (`ffmpeg` và `ffprobe`), yêu cầu chúng phải được cài đặt và có thể truy cập trong PATH của hệ thống.

## Tính Năng

Hiện tại, OIFFmpeg hỗ trợ các chức năng cốt lõi sau:

*   **Chuyển Đổi Media:** Chuyển đổi các file video và âm thanh giữa các định dạng khác nhau (`convert`).
*   **Trích Xuất Âm Thanh:** Dễ dàng trích xuất track âm thanh từ file media (`extract_audio`).
*   **Cắt Video:** Cắt các phần từ file video dựa trên thời gian bắt đầu và kết thúc (`trim_video`).
*   **Truy Xuất Thông Tin Media:** Lấy thông tin chi tiết về các file media sử dụng `ffprobe` (`get_media_info`).
*   **Stream RTMP:** Stream một file video hoặc URL lên một máy chủ RTMP (`stream_video`).
*   **Thực Thi FFmpeg Tổng Quát:** Chạy bất kỳ lệnh FFmpeg tùy chỉnh nào bằng cách cung cấp một danh sách các đối số (`run_ffmpeg`), mang lại sự linh hoạt tối đa cho người dùng nâng cao.

## Cài Đặt

**Yêu cầu tiên quyết:**

Trước khi cài đặt OIFFmpeg, bạn phải có FFmpeg được cài đặt trên hệ thống của mình. FFmpeg bao gồm cả công cụ dòng lệnh `ffmpeg` và `ffprobe`, mà thư viện này phụ thuộc vào. Bạn có thể tải FFmpeg từ trang web chính thức ([https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)) hoặc cài đặt nó bằng trình quản lý gói của hệ thống.

*   **Trên Debian/Ubuntu:**
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```
*   **Trên macOS (sử dụng Homebrew):**
    ```bash
    brew install ffmpeg
    ```
*   **Trên Windows:** Tải các bản build sẵn và thêm thư mục `bin` vào biến môi trường PATH của hệ thống.

**Cài đặt OIFFmpeg:**

Sau khi FFmpeg được cài đặt, bạn có thể cài đặt OIFFmpeg bằng pip:

```bash
pip install oiffmpeg
```

Để cài đặt phiên bản phát triển mới nhất trực tiếp từ GitHub:

```bash
pip install git+https://github.com/tiendung102k3/OIFFmpeg.git
```

## Ví Dụ Sử Dụng

Dưới đây là một số ví dụ minh họa cách sử dụng OIFFmpeg:

```python
import oiffmpeg
import json

# --- Ví dụ Input/Output (thay thế bằng đường dẫn/URL thực tế của bạn) ---
input_video_file = 'local_video.mp4' # Ví dụ file cục bộ
input_video_url = 'http://example.com/stream.m3u8' # Ví dụ URL
output_video_webm = 'output.webm'
output_audio_mp3 = 'output_audio.mp3'
output_trimmed_video = 'trimmed_video.mp4'
rtmp_endpoint = 'rtmp://your-rtmp-server.com/live/stream_key' # Ví dụ URL RTMP

# --- 1. Chuyển Đổi Định Dạng Video (MP4 sang WebM) ---
try:
    print(f"Đang chuyển đổi {input_video_file} sang {output_video_webm}...")
    success = oiffmpeg.convert(input_video_file, output_video_webm, vcodec='libvpx', acodec='libvorbis', overwrite=True)
    print(f"Chuyển đổi {"thành công" if success else "thất bại"}.")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình chuyển đổi: {e}")

# --- 2. Trích Xuất Âm Thanh (từ MP4 sang MP3) ---
try:
    print(f"Đang trích xuất âm thanh từ {input_video_file} sang {output_audio_mp3}...")
    success = oiffmpeg.extract_audio(input_video_file, output_audio_mp3, audio_codec='libmp3lame', overwrite=True)
    print(f"Trích xuất âm thanh {"thành công" if success else "thất bại"}.")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình trích xuất âm thanh: {e}")

# --- 3. Cắt Video (từ 10s đến 30s) ---
try:
    start = 10
    end = 30
    print(f"Đang cắt {input_video_file} từ {start}s đến {end}s thành {output_trimmed_video}...")
    success = oiffmpeg.trim_video(input_video_file, output_trimmed_video, start_time=start, end_time=end, overwrite=True)
    print(f"Cắt video {"thành công" if success else "thất bại"}.")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình cắt video: {e}")

# --- 4. Lấy Thông Tin Media ---
try:
    print(f"Đang lấy thông tin media cho {input_video_file}...")
    media_info = oiffmpeg.get_media_info(input_video_file)
    if media_info:
        print("Lấy thông tin media thành công:")
        print(json.dumps(media_info, indent=2, ensure_ascii=False))
    else:
        print("Không thể lấy thông tin media.")
except Exception as e:
    print(f"Đã xảy ra lỗi khi lấy thông tin media: {e}")

# --- 5. Stream Video lên RTMP (từ file cục bộ) ---
# Lưu ý: Hàm này sẽ chạy cho đến khi luồng kết thúc hoặc bị gián đoạn (ví dụ: Ctrl+C)
try:
    print(f"Đang stream {input_video_file} lên {rtmp_endpoint}...")
    # Các tùy chọn stream phổ biến: re=True (đọc theo tốc độ gốc), c='copy' (không mã hóa lại), f='flv' (định dạng)
    success = oiffmpeg.stream_video(input_video_file, rtmp_endpoint, re=True, c='copy', f='flv')
    # Nếu cần mã hóa lại (ví dụ: cho bitrate/codec cụ thể):
    # success = oiffmpeg.stream_video(input_video_file, rtmp_endpoint, re=True,
    #                                 vcodec='libx264', preset='veryfast', tune='zerolatency',
    #                                 acodec='aac', ab='128k',
    #                                 f='flv', bufsiz='1000k', maxrate='500k')
    print(f"Stream kết thúc. Thành công: {success}")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình stream: {e}")

# --- 6. Sử dụng run_ffmpeg tổng quát cho các tác vụ nâng cao ---
# Ví dụ: Thêm watermark (hình mờ) vào video
try:
    print("Đang thêm watermark bằng run_ffmpeg...")
    watermark_image = 'logo.png' # Đường dẫn đến file ảnh watermark của bạn
    output_watermarked = 'output_watermarked.mp4'
    ffmpeg_args = [
        '-i', input_video_file,
        '-i', watermark_image,
        '-filter_complex', 'overlay=W-w-10:10', # Vị trí watermark: cách góc trên-phải 10px
        '-codec:a', 'copy', # Sao chép luồng âm thanh
        '-y', # Ghi đè file output nếu tồn tại
        output_watermarked
    ]
    success = oiffmpeg.run_ffmpeg(ffmpeg_args)
    print(f"Thêm watermark {"thành công" if success else "thất bại"}.")
except Exception as e:
    print(f"Đã xảy ra lỗi khi thêm watermark: {e}")

# Ví dụ: Stream từ webcam lên RTMP (yêu cầu quyền truy cập webcam & định dạng input đúng)
# Lưu ý: Định dạng input/tên thiết bị khác nhau tùy hệ điều hành ('/dev/video0' trên Linux, 'avfoundation' trên macOS, 'dshow' trên Windows)
# Ví dụ này chỉ mang tính minh họa và có thể cần điều chỉnh cho hệ thống của bạn.
try:
    print(f"Đang stream từ webcam lên {rtmp_endpoint} (Ví dụ minh họa)...")
    # Ví dụ cho Linux, điều chỉnh '-i' và '-f' cho HĐH/thiết bị của bạn
    webcam_args = [
        '-f', 'v4l2', '-i', '/dev/video0', # Input từ webcam
        # Thêm input âm thanh nếu cần: '-f', 'alsa', '-i', 'default',
        '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
        '-c:a', 'aac', '-b:a', '128k',
        '-f', 'flv',
        rtmp_endpoint
    ]
    # success = oiffmpeg.run_ffmpeg(webcam_args) # Bỏ comment để chạy
    # print(f"Stream webcam kết thúc. Thành công: {success}")
    print("Ví dụ stream webcam bị bỏ qua (yêu cầu cài đặt cụ thể).")
except Exception as e:
    print(f"Đã xảy ra lỗi trong ví dụ stream webcam: {e}")

```

## Đóng Góp

Đóng góp luôn được chào đón! Nếu bạn tìm thấy lỗi hoặc có yêu cầu tính năng, vui lòng mở một issue trên GitHub repository ([https://github.com/tiendung102k3/OIFFmpeg/issues](https://github.com/tiendung102k3/OIFFmpeg/issues)). Pull request cũng được đánh giá cao.

## Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT - xem file LICENSE để biết chi tiết.

