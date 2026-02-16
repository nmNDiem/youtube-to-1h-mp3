"""
YouTube to 60min MP3 Converter
Entry point for the application
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to enable imports
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui.app import App
from src.core.utils import init_ffmpeg_env


import subprocess

def patch_subprocess_on_windows():
    """Patch subprocess.Popen to hide console windows on Windows"""
    if sys.platform == "win32":
        # Save original Popen
        original_popen = subprocess.Popen
        
        def new_popen(*args, **kwargs):
            # Check if it's already set
            if 'startupinfo' not in kwargs:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                kwargs['startupinfo'] = startupinfo

            
            # Hide console window
            kwargs['creationflags'] = kwargs.get('creationflags', 0) | subprocess.CREATE_NO_WINDOW
            
            return original_popen(*args, **kwargs)
        
        # Monkey patch
        subprocess.Popen = new_popen

def main():
    """Main entry point"""
    # Hide console for subprocesses on Windows
    patch_subprocess_on_windows()
    
    # Initialize environment
    init_ffmpeg_env()
    
    app = App()
    app.mainloop()




if __name__ == "__main__":
    main()
