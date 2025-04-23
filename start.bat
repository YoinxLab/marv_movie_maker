@echo off
setlocal enabledelayedexpansion

REM Anchor to the directory this script is in
pushd %~dp0

echo ====================================================
echo === LAUNCHING APEX OVERKILL FROM YOINXLAB ==========
echo ====================================================

REM --- Add embedded Python and tools to PATH ---
set PATH=%CD%\python_embed;%CD%\python_embed\Scripts;%CD%\ffmpeg;%PATH%

REM --- Run the main script using embedded Python ---
echo Running apex_overkill.py...
python_embed\python.exe apex_overkill.py

REM Return to original folder
popd
pause
