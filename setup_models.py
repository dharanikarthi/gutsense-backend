"""
Setup script to copy .h5 models from desktop to backend
"""

import os
import shutil
import sys
from pathlib import Path

def setup_models():
    """Copy .h5 models from desktop to backend models directory"""
    
    # Paths
    desktop_path = Path.home() / "OneDrive" / "Desktop"
    models_dir = Path(__file__).parent / "models" / "h5_models"
    
    print("🔍 GutSense Model Setup")
    print("=" * 30)
    print(f"Desktop path: {desktop_path}")
    print(f"Models directory: {models_dir}")
    
    # Create models directory if it doesn't exist
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Look for .h5 files on desktop
    h5_files = []
    
    # Search in desktop root
    for file in desktop_path.glob("*.h5"):
        h5_files.append(file)
    
    # Search in subdirectories
    for folder in desktop_path.iterdir():
        if folder.is_dir():
            for file in folder.glob("*.h5"):
                h5_files.append(file)
    
    if not h5_files:
        print("❌ No .h5 files found on desktop")
        print("\nManual steps:")
        print("1. Find your .h5 folder on desktop")
        print("2. Copy all .h5 files")
        print(f"3. Paste them into: {models_dir}")
        return False
    
    print(f"\n✅ Found {len(h5_files)} .h5 files:")
    for file in h5_files:
        print(f"  - {file.name}")
    
    # Copy files
    copied = 0
    for file in h5_files:
        try:
            destination = models_dir / file.name
            shutil.copy2(file, destination)
            print(f"✅ Copied: {file.name}")
            copied += 1
        except Exception as e:
            print(f"❌ Failed to copy {file.name}: {e}")
    
    print(f"\n🎉 Successfully copied {copied} model files!")
    
    # List final contents
    print(f"\nModels directory contents:")
    for file in models_dir.iterdir():
        if file.is_file():
            print(f"  - {file.name}")
    
    return copied > 0

if __name__ == "__main__":
    success = setup_models()
    if success:
        print("\n✅ Model setup complete!")
        print("Next steps:")
        print("1. git add models/h5_models/*.h5")
        print("2. git commit -m 'Add ML model files'")
        print("3. git push")
    else:
        print("\n⚠️ Please copy .h5 files manually")
    
    input("\nPress Enter to continue...")