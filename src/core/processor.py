"""
Audio processor for looping audio to 60 minutes
"""
from pydub import AudioSegment
from pathlib import Path
from typing import Callable, Optional
import math
from src.core.utils import get_ffmpeg_path, get_ffprobe_path

# Configure pydub to use bundled binaries if possible
AudioSegment.converter = get_ffmpeg_path()
AudioSegment.ffprobe = get_ffprobe_path()


class ProcessProgress:
    """Progress information for audio processing"""
    def __init__(self):
        self.status: str = "idle"
        self.percent: float = 0.0
        self.current_step: str = ""


class AudioProcessor:
    """Process audio files - loop to 60 minutes"""
    
    TARGET_DURATION_MS = 60 * 60 * 1000  # 60 minutes in milliseconds
    
    def __init__(self):
        """Initialize audio processor"""
        self.progress = ProcessProgress()
        
    def loop_to_60min(
        self,
        input_file: Path,
        output_file: Path,
        progress_callback: Optional[Callable[[ProcessProgress], None]] = None
    ) -> Path:
        """
        Loop audio file to exactly 60 minutes
        
        Args:
            input_file: Path to input audio file
            output_file: Path to save output MP3
            progress_callback: Optional callback for progress updates
            
        Returns:
            Path to output file
            
        Raises:
            Exception: If processing fails
        """
        try:
            # Step 1: Load audio
            self.progress.status = "loading"
            self.progress.current_step = "Đang tải file audio..."
            self.progress.percent = 10.0
            if progress_callback:
                progress_callback(self.progress)
                
            audio = AudioSegment.from_file(str(input_file))
            duration_ms = len(audio)
            
            # Step 2: Calculate loops needed
            self.progress.current_step = "Tính toán số lần lặp..."
            self.progress.percent = 20.0
            if progress_callback:
                progress_callback(self.progress)
                
            loops_needed = math.ceil(self.TARGET_DURATION_MS / duration_ms)
            
            # Step 3: Loop audio
            self.progress.status = "processing"
            self.progress.current_step = f"Đang lặp audio ({loops_needed} lần)..."
            self.progress.percent = 30.0
            if progress_callback:
                progress_callback(self.progress)
            
            # Create looped audio
            looped_audio = audio * loops_needed
            
            # Step 4: Trim to exact 60 minutes
            self.progress.current_step = "Cắt audio về đúng 60 phút..."
            self.progress.percent = 60.0
            if progress_callback:
                progress_callback(self.progress)
                
            final_audio = looped_audio[:self.TARGET_DURATION_MS]
            
            # Step 5: Export
            self.progress.status = "exporting"
            self.progress.current_step = "Đang xuất file MP3..."
            self.progress.percent = 80.0
            if progress_callback:
                progress_callback(self.progress)
            
            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Export as MP3 with good quality
            final_audio.export(
                str(output_file),
                format="mp3",
                bitrate="192k",
                parameters=["-q:a", "0"]  # Highest quality
            )
            
            # Done
            self.progress.status = "completed"
            self.progress.current_step = "Hoàn thành!"
            self.progress.percent = 100.0
            if progress_callback:
                progress_callback(self.progress)
                
            return output_file
            
        except Exception as e:
            self.progress.status = "error"
            self.progress.current_step = f"Lỗi: {str(e)}"
            raise Exception(f"Lỗi khi xử lý audio: {str(e)}")
    
    def get_duration_minutes(self, audio_file: Path) -> float:
        """
        Get duration of audio file in minutes
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Duration in minutes
        """
        try:
            audio = AudioSegment.from_file(str(audio_file))
            return len(audio) / 1000 / 60  # Convert ms to minutes
        except Exception:
            return 0.0
