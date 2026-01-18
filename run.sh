#!/bin/bash
# ============================================================
# Flight Tool - Universal Launcher with Auto-venv
# Automatically checks/creates venv and runs tools
# ============================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Define venv path
VENV_DIR="venv"
VENV_PYTHON="$VENV_DIR/bin/python"

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  Flight Tool - Smart Launcher${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${YELLOW}! Virtual environment not found${NC}"
    echo -e "${BLUE}+ Creating virtual environment...${NC}"
    echo ""

    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}ERROR: Python 3 not found!${NC}"
        echo "Please install Python 3.7+ from your package manager"
        exit 1
    fi

    # Create venv
    echo -e "${BLUE}+ Running setup_venv.py...${NC}"
    python3 setup_venv.py

    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}ERROR: Failed to create virtual environment!${NC}"
        exit 1
    fi

    echo ""
    echo -e "${GREEN}✓ Virtual environment created successfully!${NC}"
    echo ""
else
    echo -e "${GREEN}✓ Virtual environment found${NC}"
    echo ""
fi

# Check which tool to run
if [ -z "$1" ]; then
    echo -e "${BLUE}Usage:${NC}"
    echo "  ./run.sh test          - Run system tests"
    echo "  ./run.sh gui           - Launch Flight Tool GUI"
    echo "  ./run.sh scraper       - Run extended scraper"
    echo "  ./run.sh excel         - Run Excel scraper"
    echo "  ./run.sh extractor     - Run data extractor"
    echo ""
    echo -e "${YELLOW}No arguments provided - launching GUI by default...${NC}"
    echo ""
    "$VENV_PYTHON" FlightTool_Simple.py
    exit 0
fi

# Route to appropriate tool
case "$1" in
    test)
        echo -e "${BLUE}+ Running system tests...${NC}"
        echo ""
        "$VENV_PYTHON" test_system.py
        ;;
    gui)
        echo -e "${BLUE}+ Launching Flight Tool GUI...${NC}"
        echo ""
        "$VENV_PYTHON" FlightTool_Simple.py
        ;;
    scraper)
        echo -e "${BLUE}+ Running extended scraper...${NC}"
        echo ""
        "$VENV_PYTHON" scrap_only_extended.py
        ;;
    excel)
        echo -e "${BLUE}+ Running Excel scraper...${NC}"
        echo ""
        "$VENV_PYTHON" kayak_excel_scraper.py
        ;;
    extractor)
        echo -e "${BLUE}+ Running data extractor...${NC}"
        echo ""
        if [ -z "$2" ]; then
            echo -e "${RED}ERROR: Please provide folder path${NC}"
            echo "Example: ./run.sh extractor kayak_text_data/txt_session_20250118"
            exit 1
        fi
        "$VENV_PYTHON" simple_kayak_extractor.py "$2"
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        echo -e "${BLUE}Available commands:${NC}"
        echo "  test          - Run system tests"
        echo "  gui           - Launch Flight Tool GUI"
        echo "  scraper       - Run extended scraper"
        echo "  excel         - Run Excel scraper"
        echo "  extractor     - Run data extractor"
        echo ""
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  Done!${NC}"
echo -e "${GREEN}============================================================${NC}"
