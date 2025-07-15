#!/bin/bash
# Production startup script

echo "🚀 Starting YouTube Audio Downloader (Production Mode)"

# Create log directories
sudo mkdir -p /var/log/gunicorn
sudo chown $USER:$USER /var/log/gunicorn

# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False

# Start backend with Gunicorn
echo "Starting backend with Gunicorn..."
cd backend
gunicorn --config gunicorn.conf.py wsgi:app &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd ..
serve -s dist -l 3000 &
FRONTEND_PID=$!

echo ""
echo "✅ Services started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5001"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop services:"
echo "kill $BACKEND_PID $FRONTEND_PID"

# Keep script running
wait
