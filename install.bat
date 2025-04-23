@echo off
setlocal enabledelayedexpansion

REM Anchor all paths to the folder this script is in
pushd %~dp0

echo ====================================================
echo === SETTING UP YOINXLAB APEX OVERKILL ENVIRONMENT ==
echo ====================================================

REM --- CONFIG ---
set PYTHON_VER=3.12.8
set PYTHON_TAG=python-%PYTHON_VER%-embed-amd64
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VER%/%PYTHON_TAG%.zip
set GET_PIP_URL=https://bootstrap.pypa.io/get-pip.py
set FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
set FFMPEG_ZIP=ffmpeg.zip
set FFMPEG_DIR=ffmpeg_temp

REM --- STEP 1: Download Python embeddable zip ---
echo.
echo [1/7] Downloading Python %PYTHON_VER% Embeddable...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile 'python_embed.zip'"

REM --- STEP 2: Extract Python zip ---
echo.
echo [2/7] Extracting Python to 'python_embed/'...
powershell -Command "Expand-Archive -Path 'python_embed.zip' -DestinationPath 'python_embed' -Force"
del python_embed.zip

REM --- STEP 3: Configure python312._pth ---
echo.
echo [3/7] Configuring python312._pth...
set PTH_FILE=python_embed\python312._pth
(
    echo python312.zip
    echo .
    echo Lib
    echo Lib\site-packages
    echo import site
) > "%PTH_FILE%"

REM --- STEP 4: Download get-pip.py to root dir ---
echo.
echo [4/7] Downloading pip installer script...
powershell -Command "Invoke-WebRequest -Uri '%GET_PIP_URL%' -OutFile 'get-pip.py'"

REM --- STEP 5: Install pip using embedded Python ---
echo.
echo [5/7] Installing pip...
python_embed\python.exe get-pip.py

REM --- STEP 6: Install dependencies from requirements.txt ---
echo.
echo [6/7] Installing dependencies from requirements.txt...
python_embed\python.exe -m pip install -r requirements.txt

REM --- Cleanup ---
del get-pip.py

REM --- STEP 7: Download and extract latest FFmpeg ---
echo.
echo [7/7] Checking for FFmpeg...
if exist ffmpeg\ffmpeg.exe (
    if exist ffmpeg\ffprobe.exe (
        echo.
        echo [7/7] FFmpeg already exists. Skipping download.
        goto :skip_ffmpeg
    )
)

echo.
echo [7/7] Downloading latest FFmpeg release...
powershell -Command "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile '%FFMPEG_ZIP%'"

echo Extracting ffmpeg.zip...
powershell -Command "Expand-Archive -Path '%FFMPEG_ZIP%' -DestinationPath '%FFMPEG_DIR%' -Force"

echo Moving ffmpeg binaries to ./ffmpeg/...
if not exist ffmpeg mkdir ffmpeg
for /d %%i in (%FFMPEG_DIR%\ffmpeg-*) do (
    move /Y "%%i\bin\ffmpeg.exe" ffmpeg\ffmpeg.exe >nul
    move /Y "%%i\bin\ffprobe.exe" ffmpeg\ffprobe.exe >nul
)

REM --- Cleanup ---
rmdir /S /Q %FFMPEG_DIR%
del %FFMPEG_ZIP%

:skip_ffmpeg

echo.
echo ✅ Setup Complete!
echo.
echo You can now run the project with:
echo    python_embed\python.exe apex_overkill.py
echo.
pause

REM Return to original directory if script was launched elsewhere
popd
