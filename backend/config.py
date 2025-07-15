"""
YouTube Audio Downloader Backend Service
Configuration and utility functions
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

    # Download settings
    MAX_DOWNLOAD_SIZE = int(
        os.environ.get("MAX_DOWNLOAD_SIZE", 100 * 1024 * 1024)
    )  # 100MB
    TEMP_DIR = os.environ.get("TEMP_DIR", "temp")
    CLEANUP_INTERVAL = int(os.environ.get("CLEANUP_INTERVAL", 3600))  # 1 hour

    # Rate limiting
    MAX_CONCURRENT_DOWNLOADS = int(os.environ.get("MAX_CONCURRENT_DOWNLOADS", 5))

    # CORS settings
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")


def validate_youtube_url(url):
    """Validate if URL is a valid YouTube URL"""
    import re

    youtube_patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/shorts\/)([^&\n?#]+)",
        r"youtube\.com\/watch\?.*v=([^&\n?#]+)",
        r"m\.youtube\.com\/watch\?.*v=([^&\n?#]+)",
    ]

    for pattern in youtube_patterns:
        if re.search(pattern, url):
            return True
    return False


def sanitize_filename(filename):
    """Sanitize filename for safe file system operations"""
    import re

    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove extra whitespace and dots
    filename = re.sub(r"\s+", " ", filename).strip(" .")
    # Limit length
    return filename[:200] if len(filename) > 200 else filename
