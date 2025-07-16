#!/bin/bash
# Production startup script

echo "🚀 Starting YouTube Audio Downloader (Production Mode)"

# Activate virtual environment if it exists
if [ -d "backend/venv" ]; then
    echo "Activating virtual environment..."
    source backend/venv/bin/activate
fi

# Create log directories
sudo mkdir -p /var/log/gunicorn 2>/dev/null || mkdir -p logs
sudo chown $USER:$USER /var/log/gunicorn 2>/dev/null || true

# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False

# Start backend with Gunicorn
echo "Starting backend with Gunicorn..."
cd backend

# Create logs directory
mkdir -p logs

# Start Gunicorn with proper log paths
gunicorn --bind 0.0.0.0:5001 --workers 4 --timeout 120 --access-logfile logs/access.log --error-logfile logs/error.log wsgi:app &
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
