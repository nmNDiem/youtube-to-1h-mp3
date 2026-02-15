# YouTube to 60min MP3 Converter

Ứng dụng desktop để tải audio từ YouTube và tự động lặp thành file MP3 dài 60 phút.

## Tính năng

- ✅ Tải audio chất lượng cao từ YouTube
- ✅ Tự động lặp audio đến đúng 60 phút
- ✅ Giao diện đẹp, hiện đại với CustomTkinter
- ✅ Hiển thị tiến trình download và convert
- ✅ Hiệu suất cao (~50MB memory usage)

## Yêu cầu hệ thống

- Python 3.11 trở lên
- FFmpeg (sẽ được tự động tải về)

## Cài đặt

1. Clone repository
2. Tạo virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Sử dụng

```bash
python src/main.py
```

## Build executable

```bash
pyinstaller build.spec
```

Executable sẽ nằm trong thư mục `dist/`.
