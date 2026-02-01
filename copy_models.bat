@echo off
echo GutSense Model Copy Script
echo ========================

echo.
echo This script will help you copy .h5 model files to the correct location.
echo.

set "SOURCE_DIR=C:\Users\kmage\OneDrive\Desktop"
set "TARGET_DIR=%~dp0models\h5_models"

echo Source directory: %SOURCE_DIR%
echo Target directory: %TARGET_DIR%
echo.

echo Looking for .h5 files on desktop...
dir "%SOURCE_DIR%\*.h5" /s /b 2>nul

if errorlevel 1 (
    echo No .h5 files found directly on desktop.
    echo Please check if you have a folder containing .h5 files.
    echo.
    echo Manual steps:
    echo 1. Find your .h5 folder on the desktop
    echo 2. Copy all .h5 files from that folder
    echo 3. Paste them into: %TARGET_DIR%
    echo.
) else (
    echo Found .h5 files! Copying to models directory...
    copy "%SOURCE_DIR%\*.h5" "%TARGET_DIR%\" /y
    echo.
    echo Copy completed!
)

echo.
echo To verify your models are loaded correctly, visit:
echo https://gutsense-backend.vercel.app/api/models/list
echo.
pause