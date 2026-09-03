@echo off
REM Convenience runner script for Windows CMD / PowerShell

set IMAGE_PATH=%1
if "%IMAGE_PATH%"=="" set IMAGE_PATH=data\input_faces\sample.jpg

echo Running Face Identification & Blockchain Verification Pipeline...
python src\pipeline.py %IMAGE_PATH%
