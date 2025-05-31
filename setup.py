"""
Setup script for Smart Inventory Scanner.
This script helps users configure the application and set up the database.
"""
import os
import sys
import subprocess
from pathlib import Path
import secrets
import sqlite3
from dotenv import load_dotenv
import time
import psutil

def is_process_running(process_name):
    """Check if a process is running."""
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def kill_process(process_name):
    """Kill a running process."""
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def generate_secret_key():
    """Generate a secure secret key."""
    return secrets.token_hex(32)

def create_env_file():
    """Create .env file with default configuration."""
    env_path = Path(".env")
    if env_path.exists():
        print(".env file already exists. Skipping creation.")
        return

    # Generate secret key
    secret_key = generate_secret_key()

    # Default configuration
    env_content = f"""# Database configuration
DATABASE_URL=sqlite:///./inventory.db

# Security settings
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application settings
DEBUG=True
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
"""

    # Write to .env file
    with open(env_path, "w") as f:
        f.write(env_content)
    print(".env file created successfully!")

def setup_database():
    """Set up the SQLite database."""
    db_path = Path("inventory.db")
    if db_path.exists():
        print("Database already exists. Skipping creation.")
        return

    # Create database
    conn = sqlite3.connect(db_path)
    conn.close()
    print("Database created successfully!")

def install_dependencies():
    """Install required Python packages."""
    print("Installing Python dependencies...")
    
    # Check for running processes
    if is_process_running('uvicorn'):
        print("Uvicorn is running. Attempting to stop it...")
        kill_process('uvicorn')
        time.sleep(2)  # Wait for process to stop
    
    try:
        # First, try to install with --user flag
        subprocess.run([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "--user",
            "-r", 
            "requirements.txt"
        ], check=True)
    except subprocess.CalledProcessError:
        print("Failed to install with --user flag. Trying without it...")
        try:
            subprocess.run([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "-r", 
                "requirements.txt"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing Python dependencies: {e}")
            print("\nPlease try the following steps manually:")
            print("1. Close any running Python processes")
            print("2. Run: pip install -r requirements.txt")
            print("3. If that fails, try: pip install --user -r requirements.txt")
            sys.exit(1)

    print("Installing frontend dependencies...")
    try:
        os.chdir("frontend")
        subprocess.run("npm install", shell=True, check=True)
        os.chdir("..")
    except subprocess.CalledProcessError as e:
        print(f"Error installing frontend dependencies: {e}")
        print("\nPlease try the following steps manually:")
        print("1. cd frontend")
        print("2. npm install")
        print("3. cd ..")
        sys.exit(1)

def setup_ocr():
    """Set up OCR dependencies."""
    print("Setting up OCR dependencies...")
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    # Download EasyOCR models
    try:
        import easyocr
        reader = easyocr.Reader(['en'])
        print("OCR models downloaded successfully!")
    except Exception as e:
        print(f"Error downloading OCR models: {e}")
        print("Please install Tesseract OCR manually:")
        print("- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("- Linux: sudo apt-get install tesseract-ocr")
        print("- Mac: brew install tesseract")

def main():
    """Main setup function."""
    print("Setting up Smart Inventory Scanner...")
    
    # Create .env file
    create_env_file()
    
    # Set up database
    setup_database()
    
    # Install dependencies
    install_dependencies()
    
    # Set up OCR
    setup_ocr()
    
    print("\nSetup completed successfully!")
    print("\nTo start the application:")
    print("1. Activate your virtual environment:")
    print("   - Windows: venv\\Scripts\\activate")
    print("   - Unix/Mac: source venv/bin/activate")
    print("2. Run the application:")
    print("   python main.py --mode development")
    print("\nDefault admin credentials:")
    print("Email: admin@example.com")
    print("Password: admin123")
    print("\nPlease change these credentials after first login!")

if __name__ == "__main__":
    main() 