#!/usr/bin/env bash
# Convenience runner script for Linux / macOS / Git Bash

IMAGE_PATH=${1:-"data/input_faces/sample.jpg"}

echo "Running Face Identification & Blockchain Verification Pipeline..."
python3 src/pipeline.py "$IMAGE_PATH"
