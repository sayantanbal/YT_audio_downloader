# YouTube Audio Downloader - Backend

Flask-based backend API for downloading YouTube audio using yt-dlp.

## Setup

```bash
pip install -r requirements.txt
```

## Development

```bash
python app.py
```

## Production

```bash
gunicorn -c gunicorn.conf.py wsgi:app
```
