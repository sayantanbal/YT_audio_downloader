#!/bin/bash
# Start script for development
echo "🚀 Starting YouTube Audio Downloader (Development Mode)"
echo "Backend: http://localhost:5001"
echo "Frontend: http://localhost:5173"
echo ""

# Start backend
cd backend
python app.py
