#!/bin/bash
# Check if venv exists, if not create it
if [ ! -f "venv/bin/python" ]; then
    echo "Virtual environment not found. Creating..."
    python3 setup_venv.py
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment!"
        exit 1
    fi
fi
"venv/bin/python" scrap_only_extended.py "$@"
