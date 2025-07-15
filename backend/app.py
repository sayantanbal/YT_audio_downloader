from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import tempfile
import uuid
import threading
import time
from pathlib import Path
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global dictionary to store download progress
download_progress = {}

# User agents pool to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


def get_random_user_agent():
    """Get a random user agent to avoid detection"""
    return random.choice(USER_AGENTS)


class ProgressHook:
    def __init__(self, download_id):
        self.download_id = download_id

    def __call__(self, d):
        if d["status"] == "downloading":
            if "total_bytes" in d and d["total_bytes"]:
                percent = (d["downloaded_bytes"] / d["total_bytes"]) * 100
            elif "_percent_str" in d:
                percent_str = d["_percent_str"].replace("%", "")
                try:
                    percent = float(percent_str)
                except ValueError:
                    percent = 0
            else:
                percent = 0

            download_progress[self.download_id] = {
                "status": "downloading",
                "progress": min(percent, 99),  # Cap at 99% until complete
                "speed": d.get("_speed_str", ""),
                "eta": d.get("_eta_str", ""),
            }
        elif d["status"] == "finished":
            download_progress[self.download_id] = {
                "status": "finished",
                "progress": 100,
                "filename": d["filename"],
            }


def get_video_info(url):
    """Extract video information without downloading"""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "user_agent": get_random_user_agent(),
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
        "extractor_retries": 3,
        "fragment_retries": 3,
        "retry_sleep_functions": {
            "http": lambda n: min(2**n, 30),
            "fragment": lambda n: min(2**n, 30),
        },
        # Additional options for better compatibility
        "extract_flat": False,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "success": True,
                "title": info.get("title", "Unknown"),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Unknown"),
                "thumbnail": info.get("thumbnail", ""),
                "view_count": info.get("view_count", 0),
                "upload_date": info.get("upload_date", ""),
            }
    except Exception as e:
        logger.error(f"Error extracting video info: {str(e)}")
        return {"success": False, "error": str(e)}


def download_audio_thread(url, download_id, output_path):
    """Download audio in a separate thread"""
    try:
        # Create a unique filename
        filename = f"{download_id}.%(ext)s"
        full_path = os.path.join(output_path, filename)

        ydl_opts = {
            "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best[height<=720]",
            "outtmpl": full_path,
            "progress_hooks": [ProgressHook(download_id)],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "quiet": True,
            "no_warnings": True,
            # Enhanced anti-detection measures
            "user_agent": get_random_user_agent(),
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
            # Retry settings
            "extractor_retries": 3,
            "fragment_retries": 3,
            "retry_sleep_functions": {
                "http": lambda n: min(2**n, 30),
                "fragment": lambda n: min(2**n, 30),
            },
            # Additional options to avoid rate limiting
            "sleep_interval": 1,
            "max_sleep_interval": 3,
            "sleep_interval_subtitles": 1,
            # YouTube-specific options
            "youtube_include_dash_manifest": False,
            "youtube_include_hls_manifest": False,
            # Network options
            "socket_timeout": 30,
            "retries": 5,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Update final status
        download_progress[download_id]["status"] = "completed"
        download_progress[download_id]["progress"] = 100

    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        # More detailed error handling
        error_msg = str(e)
        if "403" in error_msg or "Forbidden" in error_msg:
            error_msg = "⚠️ YouTube has temporarily blocked this request. This is likely due to rate limiting. Please wait a few minutes and try again, or try a different video."
        elif "404" in error_msg:
            error_msg = "❌ Video not found. The video might be private, deleted, or the URL is incorrect."
        elif "unavailable" in error_msg.lower():
            error_msg = "🚫 Video is unavailable in your region or has been removed."
        elif "Sign in to confirm your age" in error_msg:
            error_msg = "🔞 This video is age-restricted and cannot be downloaded without authentication."
        elif "Private video" in error_msg:
            error_msg = "🔒 This is a private video and cannot be downloaded."
        elif "Video unavailable" in error_msg:
            error_msg = (
                "📹 Video is unavailable. It may have been removed or made private."
            )
        elif "network" in error_msg.lower() or "timeout" in error_msg.lower():
            error_msg = "🌐 Network error occurred. Please check your internet connection and try again."
        else:
            error_msg = f"💥 Download failed: {error_msg}"

        download_progress[download_id] = {
            "status": "error",
            "progress": 0,
            "error": error_msg,
        }


@app.route("/api/video-info", methods=["POST"])
def video_info():
    """Get video information endpoint"""
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"success": False, "error": "URL is required"}), 400

        info = get_video_info(url)
        return jsonify(info)

    except Exception as e:
        logger.error(f"Video info error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/download", methods=["POST"])
def start_download():
    """Start audio download endpoint"""
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"success": False, "error": "URL is required"}), 400

        # Generate unique download ID
        download_id = str(uuid.uuid4())

        # Create temporary directory for this download
        temp_dir = tempfile.mkdtemp(prefix=f"yt_download_{download_id}_")

        # Initialize progress tracking
        download_progress[download_id] = {
            "status": "started",
            "progress": 0,
            "temp_dir": temp_dir,
        }

        # Start download in background thread
        thread = threading.Thread(
            target=download_audio_thread, args=(url, download_id, temp_dir)
        )
        thread.daemon = True
        thread.start()

        return jsonify(
            {"success": True, "download_id": download_id, "message": "Download started"}
        )

    except Exception as e:
        logger.error(f"Download start error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/progress/<download_id>", methods=["GET"])
def get_progress(download_id):
    """Get download progress endpoint"""
    try:
        if download_id not in download_progress:
            return jsonify({"success": False, "error": "Download not found"}), 404

        progress_data = download_progress[download_id].copy()
        return jsonify({"success": True, "progress": progress_data})

    except Exception as e:
        logger.error(f"Progress check error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/download/<download_id>", methods=["GET"])
def download_file(download_id):
    """Download the completed audio file"""
    try:
        # First check if we have progress data
        if download_id in download_progress:
            progress_data = download_progress[download_id]

            if progress_data["status"] != "completed":
                return jsonify(
                    {"success": False, "error": "Download not completed yet"}
                ), 400

            # Find the downloaded file
            if "temp_dir" in progress_data:
                temp_dir = progress_data["temp_dir"]

                # Look for any audio file with the download_id prefix
                files = list(Path(temp_dir).glob(f"{download_id}.*"))

                if files:
                    file_path = files[0]

                    # Clean up progress tracking after successful download
                    def cleanup():
                        time.sleep(300)  # Wait 5 minutes before cleanup
                        try:
                            if download_id in download_progress:
                                del download_progress[download_id]
                            # Clean up temp directory
                            import shutil

                            shutil.rmtree(temp_dir, ignore_errors=True)
                        except Exception:
                            pass

                    cleanup_thread = threading.Thread(target=cleanup)
                    cleanup_thread.daemon = True
                    cleanup_thread.start()

                    return send_file(
                        file_path,
                        as_attachment=True,
                        download_name=f"{file_path.stem}.mp3",
                        mimetype="audio/mpeg",
                    )

        # Fallback: Search all temp directories for this download_id
        # This handles cases where Flask server restarted and lost progress data
        temp_base = tempfile.gettempdir()
        temp_dirs = [
            d
            for d in Path(temp_base).iterdir()
            if d.is_dir() and d.name.startswith(f"yt_download_{download_id}_")
        ]

        for temp_dir in temp_dirs:
            # Look for any audio file with the download_id prefix
            audio_extensions = ["*.mp3", "*.m4a", "*.webm", "*.ogg", "*.wav"]
            files = []
            for ext in audio_extensions:
                files.extend(list(temp_dir.glob(ext)))

            if files:
                file_path = files[0]

                # Clean up temp directory after download
                def cleanup():
                    time.sleep(300)  # Wait 5 minutes before cleanup
                    try:
                        import shutil

                        shutil.rmtree(temp_dir, ignore_errors=True)
                    except Exception:
                        pass

                cleanup_thread = threading.Thread(target=cleanup)
                cleanup_thread.daemon = True
                cleanup_thread.start()

                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=f"{file_path.stem}.mp3",
                    mimetype="audio/mpeg",
                )

        # If nothing found
        return jsonify(
            {"success": False, "error": "Downloaded file not found or expired"}
        ), 404

    except Exception as e:
        logger.error(f"File download error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "success": True,
            "message": "YouTube Audio Downloader API is running",
            "active_downloads": len(download_progress),
        }
    )


@app.route("/api/cleanup", methods=["POST"])
def cleanup_downloads():
    """Cleanup old downloads (admin endpoint)"""
    try:
        # Clean up completed or errored downloads older than 1 hour
        current_time = time.time()
        to_remove = []

        for download_id, data in download_progress.items():
            # Add timestamp if not present
            if "timestamp" not in data:
                data["timestamp"] = current_time

            # Remove if older than 1 hour and completed/errored
            if (current_time - data.get("timestamp", current_time)) > 3600:
                if data["status"] in ["completed", "error"]:
                    to_remove.append(download_id)

        for download_id in to_remove:
            del download_progress[download_id]

        return jsonify(
            {
                "success": True,
                "cleaned_up": len(to_remove),
                "active_downloads": len(download_progress),
            }
        )

    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)

    # Check if running in production
    if os.environ.get("FLASK_ENV") == "production":
        # Production: Let Gunicorn handle this
        app.run(debug=False, host="0.0.0.0", port=5001)
    else:
        # Development server
        app.run(debug=True, host="0.0.0.0", port=5001)
