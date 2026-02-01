@echo off
echo ========================================
echo    GutSense .h5 Model Copy Script
echo ========================================
echo.

set "DESKTOP_PATH=C:\Users\%USERNAME%\OneDrive\Desktop"
set "MODELS_PATH=%~dp0models\h5_models"

echo Desktop path: %DESKTOP_PATH%
echo Models path: %MODELS_PATH%
echo.

echo Creating models directory...
if not exist "%MODELS_PATH%" mkdir "%MODELS_PATH%"

echo.
echo Looking for .h5 files on desktop...
echo.

REM Search for .h5 files in desktop root
for %%f in ("%DESKTOP_PATH%\*.h5") do (
    if exist "%%f" (
        echo Found: %%~nxf
        copy "%%f" "%MODELS_PATH%\" /Y
        echo Copied: %%~nxf
        echo.
    )
)

REM Search for .h5 files in desktop subfolders
for /d %%d in ("%DESKTOP_PATH%\*") do (
    for %%f in ("%%d\*.h5") do (
        if exist "%%f" (
            echo Found in %%~nd: %%~nxf
            copy "%%f" "%MODELS_PATH%\" /Y
            echo Copied: %%~nxf
            echo.
        )
    )
)

echo.
echo ========================================
echo Current models directory contents:
echo ========================================
dir "%MODELS_PATH%" /b

echo.
echo ========================================
echo Manual Instructions (if no files found):
echo ========================================
echo 1. Find your .h5 folder on desktop
echo 2. Copy all .h5 files from that folder
echo 3. Paste them into: %MODELS_PATH%
echo 4. Run this script again to verify
echo.

echo ========================================
echo Next Steps:
echo ========================================
echo 1. git add models/h5_models/*.h5
echo 2. git commit -m "Add ML model files"
echo 3. git push
echo.

pause