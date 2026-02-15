"""
YouTube audio downloader using yt-dlp
"""
import yt_dlp
from pathlib import Path
from typing import Callable, Optional
import tempfile
from src.core.utils import get_ffmpeg_path


class DownloadProgress:
    """Progress information for download"""
    def __init__(self):
        self.status: str = "idle"
        self.percent: float = 0.0
        self.downloaded_bytes: int = 0
        self.total_bytes: int = 0
        self.speed: float = 0.0


class YouTubeDownloader:
    """Download audio from YouTube videos"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize downloader
        
        Args:
            output_dir: Directory to save temporary files. If None, uses system temp.
        """
        self.output_dir = output_dir or Path(tempfile.gettempdir())
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.progress = DownloadProgress()
        
    def _progress_hook(self, d: dict):
        """Hook called by yt-dlp to report progress"""
        if d['status'] == 'downloading':
            self.progress.status = 'downloading'
            self.progress.downloaded_bytes = d.get('downloaded_bytes', 0)
            self.progress.total_bytes = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            self.progress.speed = d.get('speed', 0) or 0
            
            if self.progress.total_bytes > 0:
                self.progress.percent = (self.progress.downloaded_bytes / self.progress.total_bytes) * 100
        elif d['status'] == 'finished':
            self.progress.status = 'finished'
            self.progress.percent = 100.0
            
    def download(
        self, 
        url: str, 
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None
    ) -> Path:
        """
        Download audio from YouTube URL
        
        Args:
            url: YouTube video URL
            progress_callback: Optional callback function that receives DownloadProgress
            
        Returns:
            Path to downloaded audio file
            
        Raises:
            Exception: If download fails
        """
        output_template = str(self.output_dir / '%(id)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'ffmpeg_location': get_ffmpeg_path(),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                video_id = info.get('id', 'audio')
                
                # Download
                ydl.download([url])
                
                # Call progress callback if provided
                if progress_callback:
                    progress_callback(self.progress)
                
                # Return path to downloaded file and title
                audio_file = self.output_dir / f"{video_id}.mp3"
                title = info.get('title', video_id)
                # Sanitize title for filename: allow alphanumeric, space, and safe punctuation
                safe_chars = set(" -_()[].,")
                safe_title = "".join([c for c in title if c.isalnum() or c in safe_chars]).strip()
                
                if not audio_file.exists():
                    raise FileNotFoundError(f"Download completed but file not found: {audio_file}")
                    
                return audio_file, safe_title
                
        except Exception as e:
            self.progress.status = 'error'
            raise Exception(f"Lỗi khi tải video: {str(e)}")
