#!/usr/bin/env python3
"""
Helper script to update file paths after directory restructure
"""

import os
import re
import sys

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def update_file(filepath, replacements):
    """Update paths in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        for old, new in replacements.items():
            content = content.replace(old, new)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {filepath}")
            return True
        else:
            print(f"- No changes: {filepath}")
            return False
    except Exception as e:
        print(f"✗ Error in {filepath}: {e}")
        return False

def main():
    print("Updating file paths after directory restructure...")
    print("=" * 60)

    # Path mappings
    replacements = {
        # Config paths
        '"config_extended.json"': '"config/config_extended.json"',
        "'config_extended.json'": "'config/config_extended.json'",
        '"excel_config.json"': '"config/excel_config.json"',
        "'excel_config.json'": "'config/excel_config.json'",

        # Data paths
        '"flights_list.xlsx"': '"data/flights_list.xlsx"',
        "'flights_list.xlsx'": "'data/flights_list.xlsx'",

        # Output paths
        '"kayak_text_data"': '"output/kayak_text_data"',
        "'kayak_text_data'": "'output/kayak_text_data'",
        '"kayak_excel_data"': '"output/kayak_excel_data"',
        "'kayak_excel_data'": "'output/kayak_excel_data'",
        '"kayak_json_data"': '"output/kayak_json_data"',
        "'kayak_json_data'": "'output/kayak_json_data'",
    }

    # Files to update
    files_to_update = [
        'src/scrap_only_extended.py',
        'src/kayak_excel_scraper.py',
        'src/simple_kayak_extractor.py',
        'src/FlightTool_Simple.py',
        'scripts/setup_venv.py',
    ]

    updated_count = 0
    for filepath in files_to_update:
        if os.path.exists(filepath):
            if update_file(filepath, replacements):
                updated_count += 1
        else:
            print(f"✗ File not found: {filepath}")

    print("=" * 60)
    print(f"Updated {updated_count} files")

if __name__ == "__main__":
    main()
