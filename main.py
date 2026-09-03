#!/usr/bin/env python3
"""
Main entry point for Plastic Material Metrics Extractor
"""
import sys
import os

# Ensure the script can be run from any directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

if __name__ == "__main__":
    try:
        from gui import main
        main()
    except ImportError as e:
        print(f"Error: Failed to import required modules: {e}")
        print("\nPlease install required packages by running:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
