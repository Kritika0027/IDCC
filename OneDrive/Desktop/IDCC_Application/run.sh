#!/bin/bash
# Linux/Mac shell script to run PRATT application
echo "Starting PRATT - IDCC Requirements Assistant..."

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 run.py
elif command -v python &> /dev/null; then
    python run.py
else
    echo "ERROR: Python not found!"
    echo "Please install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi

