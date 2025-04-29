# OIFFmpeg: Một Thư Viện Python Đơn Giản Cho FFmpeg

OIFFmpeg cung cấp một giao diện Python đơn giản cho các tác vụ thường gặp khi sử dụng framework đa phương tiện FFmpeg mạnh mẽ. Thư viện này nhằm đơn giản hóa việc thực thi các lệnh FFmpeg cho các thao tác như chuyển đổi định dạng media, trích xuất âm thanh, cắt video và truy xuất thông tin media, trực tiếp từ các script Python của bạn. Nó sử dụng module `subprocess` tiêu chuẩn để tương tác với các công cụ dòng lệnh FFmpeg (`ffmpeg` và `ffprobe`), yêu cầu chúng phải được cài đặt và có thể truy cập trong PATH của hệ thống.

## Tính Năng

Hiện tại, OIFFmpeg hỗ trợ các chức năng cốt lõi sau:

*   **Chuyển Đổi Media:** Chuyển đổi các file video và âm thanh giữa các định dạng khác nhau. Bạn có thể chỉ định codec và các tham số FFmpeg khác khi cần.
*   **Trích Xuất Âm Thanh:** Dễ dàng trích xuất track âm thanh từ file video và lưu nó như một file âm thanh riêng biệt (ví dụ: MP3, AAC).
*   **Cắt Video:** Cắt các phần từ file video dựa trên thời gian bắt đầu và kết thúc. Cung cấp tùy chọn cắt nhanh (sao chép stream) hoặc mã hóa lại để có độ chính xác cao hơn.
*   **Truy Xuất Thông Tin Media:** Lấy thông tin chi tiết về các file media, bao gồm chi tiết định dạng, thời lượng, codec, bitrate và thuộc tính stream, được phân tích thuận tiện thành một từ điển Python sử dụng `ffprobe`.

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

Sau khi FFmpeg được cài đặt, bạn có thể cài đặt OIFFmpeg bằng pip (sau khi nó được xuất bản lên PyPI):

```bash
pip install oiffmpeg
```

Hoặc, bạn có thể cài đặt trực tiếp từ mã nguồn nếu bạn clone repository:

```bash
git clone <repository_url> # Thay thế bằng URL GitHub thực tế sau này
cd OIFFmpeg
pip install .
```

## Ví Dụ Sử Dụng

Dưới đây là một số ví dụ cơ bản minh họa cách sử dụng OIFFmpeg:

```python
import oiffmpeg
import json

# --- Đảm bảo FFmpeg được cài đặt (kiểm tra tùy chọn) ---
# from oiffmpeg.utils import check_ffmpeg_installed
# if not check_ffmpeg_installed():
#     print("Lỗi: FFmpeg không được cài đặt hoặc không có trong PATH.")
#     exit()

# --- Ví dụ Input/Output Files (thay thế bằng đường dẫn thực tế của bạn) ---
input_video = 'input.mp4'
output_video_webm = 'output.webm'
output_audio_mp3 = 'output_audio.mp3'
output_trimmed_video = 'trimmed_video.mp4'

# --- 1. Chuyển Đổi Định Dạng Video (MP4 sang WebM) ---
try:
    print(f"Đang chuyển đổi {input_video} sang {output_video_webm}...")
    success = oiffmpeg.convert(input_video, output_video_webm, vcodec='libvpx', acodec='libvorbis', overwrite=True)
    if success:
        print("Chuyển đổi thành công!")
    else:
        print("Chuyển đổi thất bại.")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình chuyển đổi: {e}")

# --- 2. Trích Xuất Âm Thanh (từ MP4 sang MP3) ---
try:
    print(f"Đang trích xuất âm thanh từ {input_video} sang {output_audio_mp3}...")
    success = oiffmpeg.extract_audio(input_video, output_audio_mp3, audio_codec='libmp3lame', overwrite=True)
    if success:
        print("Trích xuất âm thanh thành công!")
    else:
        print("Trích xuất âm thanh thất bại.")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình trích xuất âm thanh: {e}")

# --- 3. Cắt Video (từ 10s đến 30s) ---
try:
    start = 10  # Thời gian bắt đầu tính bằng giây
    end = 30    # Thời gian kết thúc tính bằng giây
    print(f"Đang cắt {input_video} từ {start}s đến {end}s thành {output_trimmed_video}...")
    # Sử dụng re_encode=True (mặc định) để có độ chính xác cao hơn
    success = oiffmpeg.trim_video(input_video, output_trimmed_video, start_time=start, end_time=end, overwrite=True)
    # Để cắt nhanh hơn, có thể ít chính xác hơn (sao chép codec):
    # success = oiffmpeg.trim_video(input_video, output_trimmed_video, start_time=start, end_time=end, re_encode=False, overwrite=True)
    if success:
        print("Cắt video thành công!")
    else:
        print("Cắt video thất bại.")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình cắt video: {e}")

# --- 4. Lấy Thông Tin Media ---
try:
    print(f"Đang lấy thông tin media cho {input_video}...")
    media_info = oiffmpeg.get_media_info(input_video)
    if media_info:
        print("Lấy thông tin media thành công:")
        # In thông tin JSON đẹp mắt
        print(json.dumps(media_info, indent=4))
        
        # Ví dụ: Truy cập thông tin cụ thể
        duration = float(media_info.get('format', {}).get('duration', 0))
        print(f"\nThời lượng: {duration:.2f} giây")
        
        video_streams = [s for s in media_info.get('streams', []) if s.get('codec_type') == 'video']
        if video_streams:
            print(f"Codec Video: {video_streams[0].get('codec_name')}")
            print(f"Độ phân giải: {video_streams[0].get('width')}x{video_streams[0].get('height')}")
            
    else:
        print("Không thể lấy thông tin media.")
except Exception as e:
    print(f"Đã xảy ra lỗi khi lấy thông tin media: {e}")

```

## Đóng Góp

Đóng góp luôn được chào đón! Nếu bạn tìm thấy lỗi hoặc có yêu cầu tính năng, vui lòng mở một issue trên GitHub repository. Pull request cũng được đánh giá cao.

## Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT - xem file LICENSE để biết chi tiết.
