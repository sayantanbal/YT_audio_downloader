import os
import sys

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the Flask app after adding to path
try:
    from app import app as application
except ImportError:
    # Fallback for different deployment scenarios
    from backend.app import app as application

# Ensure temp directory exists
temp_dir = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(temp_dir, exist_ok=True)

if __name__ == "__main__":
    application.run(debug=False)
