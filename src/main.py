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


def main():
    """Main entry point"""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
