"""
Smart Inventory Scanner - Main Entry Point

This script serves as the main entry point for the Smart Inventory Scanner application.
It handles both development and production environments, managing the backend FastAPI server
and the React frontend.
"""

import os
import sys
import subprocess
import webbrowser
from threading import Thread
import time
import argparse
from pathlib import Path

def setup_environment():
    """Set up the environment variables and paths."""
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    # Set environment variables
    os.environ["PROJECT_ROOT"] = str(project_root)
    os.environ["FRONTEND_DIR"] = str(project_root / "frontend")
    os.environ["BACKEND_DIR"] = str(project_root / "app")
    
    # Add the project root to Python path
    sys.path.append(str(project_root))

def run_backend(host="0.0.0.0", port=8000, reload=True):
    """Run the FastAPI backend server."""
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host", host,
        "--port", str(port)
    ]
    if reload:
        cmd.append("--reload")
    
    subprocess.run(cmd)

def run_frontend(port=3000):
    """Run the React frontend development server."""
    os.chdir(os.environ["FRONTEND_DIR"])
    if os.name == "nt":  # Windows
        subprocess.run(f"set PORT={port} && npm start", shell=True)
    else:  # Unix-like
        subprocess.run(f"PORT={port} npm start", shell=True)

def run_production():
    """Run the application in production mode."""
    # Build the frontend
    os.chdir(os.environ["FRONTEND_DIR"])
    subprocess.run("npm run build", shell=True)
    
    # Run the backend server
    run_backend(reload=False)

def run_development():
    """Run the application in development mode."""
    # Start backend server
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Wait for backend to start
    time.sleep(2)

    # Start frontend server
    frontend_thread = Thread(target=run_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()

    # Open browser
    time.sleep(5)  # Wait for frontend to start
    webbrowser.open("http://localhost:3000")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Smart Inventory Scanner")
    parser.add_argument(
        "--mode",
        choices=["development", "production"],
        default="development",
        help="Run mode: development or production"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for the backend server"
    )
    parser.add_argument(
        "--backend-port",
        type=int,
        default=8000,
        help="Port for the backend server"
    )
    parser.add_argument(
        "--frontend-port",
        type=int,
        default=3000,
        help="Port for the frontend server"
    )
    
    args = parser.parse_args()
    
    # Set up environment
    setup_environment()
    
    # Run the application
    if args.mode == "production":
        run_production()
    else:
        run_development()

if __name__ == "__main__":
    main() 