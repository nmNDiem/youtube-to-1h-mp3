"""
YouTube URL validator using pydantic
"""
from pydantic import BaseModel, HttpUrl, field_validator
import re


class YouTubeURL(BaseModel):
    """YouTube URL validator"""
    url: str
    
    @field_validator('url')
    @classmethod
    def validate_youtube_url(cls, v: str) -> str:
        """Validate that the URL is a valid YouTube URL"""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        
        match = re.match(youtube_regex, v)
        if not match:
            raise ValueError('URL không hợp lệ. Vui lòng nhập link YouTube.')
        
        return v
    
    def get_video_id(self) -> str:
        """Extract YouTube video ID from URL"""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        match = re.match(youtube_regex, self.url)
        if match:
            return match.group(6)
        return ""


def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate YouTube URL
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        yt_url = YouTubeURL(url=url)
        return True, ""
    except Exception as e:
        return False, str(e)
