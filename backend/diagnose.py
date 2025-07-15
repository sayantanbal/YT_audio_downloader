#!/usr/bin/env python3
"""
Alternative YouTube downloader using different approach
This script tests various methods to download YouTube audio
"""

import yt_dlp


def test_simple_extraction():
    """Test simple yt-dlp extraction"""
    print("🧪 Testing simple yt-dlp extraction...")

    # Test URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    # Most basic options
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "format": "bestaudio/best",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"✅ Basic extraction successful: {info.get('title', 'Unknown')}")
            return True
    except Exception as e:
        print(f"❌ Basic extraction failed: {e}")
        return False


def test_with_headers():
    """Test with enhanced headers"""
    print("🧪 Testing with enhanced headers...")

    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "format": "bestaudio/best",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "referer": "https://www.youtube.com/",
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Upgrade-Insecure-Requests": "1",
        },
        "cookiefile": None,
        "extract_cookies": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(
                f"✅ Enhanced headers extraction successful: {info.get('title', 'Unknown')}"
            )
            return True
    except Exception as e:
        print(f"❌ Enhanced headers extraction failed: {e}")
        return False


def test_different_url():
    """Test with a different, known working video"""
    print("🧪 Testing with different video...")

    # Try a different video that's more likely to work
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # Official video

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "format": "worst",  # Try worst quality to see if it works
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(
                f"✅ Different video extraction successful: {info.get('title', 'Unknown')}"
            )
            return True
    except Exception as e:
        print(f"❌ Different video extraction failed: {e}")
        return False


def check_yt_dlp_version():
    """Check yt-dlp version"""
    print(f"📦 yt-dlp version: {yt_dlp.version.__version__}")


if __name__ == "__main__":
    print("🔧 YouTube Download Diagnostics")
    print("=" * 50)

    check_yt_dlp_version()
    print()

    tests = [
        ("Simple Extraction", test_simple_extraction),
        ("Enhanced Headers", test_with_headers),
        ("Different Video", test_different_url),
    ]

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        print("-" * 30)

    print("\n💡 If all tests fail, YouTube may have updated their anti-bot measures.")
    print(
        "   Consider using yt-dlp directly from command line or updating to the latest version."
    )
