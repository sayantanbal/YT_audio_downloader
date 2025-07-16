#!/bin/bash
# Simple production startup script - no log files

echo "🚀 Starting YouTube Audio Downloader (Production Mode)"

# Activate virtual environment if it exists
if [ -d "backend/venv" ]; then
    echo "Activating virtual environment..."
    source backend/venv/bin/activate
fi

# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False

# Start backend with Gunicorn (logs to console)
echo "Starting backend with Gunicorn..."
cd backend
gunicorn --bind 0.0.0.0:5001 --workers 4 --timeout 120 wsgi:app &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd ..
serve -s dist -l 3000 &
FRONTEND_PID=$!

echo ""
echo "✅ Services started!"
echo "🌐 Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3000"
echo "🔧 Backend API: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5001"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop services:"
echo "kill $BACKEND_PID $FRONTEND_PID"

# Keep script running
wait
