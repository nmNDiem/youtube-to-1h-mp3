import sys
import os
from pathlib import Path

def get_bundle_dir():
    """Get the directory where the application is running from"""
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle
        return Path(sys._MEIPASS)
    else:
        # Running from source
        return Path(__file__).parent.parent.parent

def get_ffmpeg_path():
    """Get the path to the ffmpeg executable"""
    bundle_dir = get_bundle_dir()
    ffmpeg_exe = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    
    # Check in bin/ directory
    bin_path = bundle_dir / "bin" / ffmpeg_exe
    if bin_path.exists():
        return str(bin_path)
    
    # Fallback to system ffmpeg
    return "ffmpeg"

def get_ffprobe_path():
    """Get the path to the ffprobe executable"""
    bundle_dir = get_bundle_dir()
    ffprobe_exe = "ffprobe.exe" if sys.platform == "win32" else "ffprobe"
    
    # Check in bin/ directory
    bin_path = bundle_dir / "bin" / ffprobe_exe
    if bin_path.exists():
        return str(bin_path)
    
    # Fallback to system ffprobe
    return "ffprobe"
