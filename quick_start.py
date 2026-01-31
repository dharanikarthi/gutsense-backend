#!/usr/bin/env python3
"""
Quick start script for GutSense backend
This script sets up everything needed to run the API
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("🦠 GutSense Backend Quick Start")
    print("=" * 40)
    print("Setting up your gut health API...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_postgresql():
    """Check if PostgreSQL is available"""
    try:
        result = subprocess.run(
            ["psql", "--version"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("✅ PostgreSQL is available")
            return True
        else:
            print("❌ PostgreSQL not found")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL not found in PATH")
        print("   Please install PostgreSQL first")
        return False

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_environment():
    """Set up environment file"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("⚙️  Setting up environment file...")
        # Copy example and modify
        with open(env_example) as f:
            content = f.read()
        
        # Replace with default values for quick start
        content = content.replace(
            "DATABASE_URL=postgresql://username:password@localhost:5432/gutsense_db",
            "DATABASE_URL=postgresql://postgres:password@localhost:5432/gutsense_db"
        )
        content = content.replace(
            "SECRET_KEY=your-secret-key-here-change-in-production",
            "SECRET_KEY=dev-secret-key-change-in-production"
        )
        
        with open(env_file, "w") as f:
            f.write(content)
        
        print("✅ Environment file created")
        print("   📝 Edit .env file with your database credentials")
    else:
        print("ℹ️  Environment file already exists")

def setup_database():
    """Set up database"""
    print("🗄️  Setting up database...")
    try:
        subprocess.run([sys.executable, "setup_db.py"], check=True)
        print("✅ Database setup completed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Database setup failed")
        print("   Make sure PostgreSQL is running and credentials are correct")
        return False

def test_api():
    """Test API endpoints"""
    print("🧪 Testing API...")
    try:
        # Start server in background for testing
        import threading
        import time
        
        def start_server():
            subprocess.run([sys.executable, "main.py"], capture_output=True)
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Run API tests
        subprocess.run([sys.executable, "scripts/test_api.py"], check=True)
        print("✅ API tests passed")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  API tests failed (this is normal for first run)")
        return False

def print_next_steps():
    """Print next steps"""
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Start the server:")
    print("   python main.py")
    print("\n2. Visit the API documentation:")
    print("   http://localhost:8000/docs")
    print("\n3. Test the API:")
    print("   python scripts/test_api.py")
    print("\n4. Connect your frontend:")
    print("   Update frontend API_BASE_URL to http://localhost:8000")

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    check_python_version()
    
    if not check_postgresql():
        print("\n💡 Install PostgreSQL:")
        print("   - macOS: brew install postgresql")
        print("   - Ubuntu: sudo apt install postgresql postgresql-contrib")
        print("   - Windows: Download from postgresql.org")
        sys.exit(1)
    
    # Install dependencies
    if not install_requirements():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Setup database
    if not setup_database():
        print("\n💡 Manual database setup:")
        print("   1. Start PostgreSQL service")
        print("   2. Create database: createdb gutsense_db")
        print("   3. Run: python setup_db.py")
        sys.exit(1)
    
    # Print success message
    print_next_steps()

if __name__ == "__main__":
    main()