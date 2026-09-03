#!/usr/bin/env python3
"""
Setup verification script
Checks if all dependencies are installed and system is ready
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("\n" + "="*60)
    print("PYTHON VERSION CHECK")
    print("="*60)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Current Python: {version_str}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version is compatible (3.8+)")
        return True
    else:
        print("✗ Python version is too old. Python 3.8+ required")
        return False


def check_modules():
    """Check if required modules are installed"""
    print("\n" + "="*60)
    print("DEPENDENCY CHECK")
    print("="*60)
    
    required_modules = {
        'pdfplumber': 'PDF text and table extraction',
        'openpyxl': 'Excel file generation',
        'pandas': 'Data organization',
        'PIL': 'Image processing (from pillow)',
        'tkinter': 'GUI framework',
    }
    
    all_ok = True
    
    for module_name, description in required_modules.items():
        try:
            __import__(module_name)
            print(f"✓ {module_name:15} - {description}")
        except ImportError:
            print(f"✗ {module_name:15} - MISSING")
            all_ok = False
    
    return all_ok


def check_files():
    """Check if all required files exist"""
    print("\n" + "="*60)
    print("PROJECT FILES CHECK")
    print("="*60)
    
    required_files = {
        'main.py': 'Application launcher',
        'gui.py': 'GUI interface',
        'enhanced_extractor.py': 'PDF extraction engine',
        'unit_converter.py': 'Unit conversion',
        'excel_writer.py': 'Excel generation',
        'config.py': 'Configuration',
        'requirements.txt': 'Dependencies list',
        'README.md': 'Documentation',
        'QUICKSTART.md': 'Quick start guide',
    }
    
    base_dir = Path(__file__).parent
    all_ok = True
    
    for filename, description in required_files.items():
        filepath = base_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✓ {filename:25} ({size:>8} bytes) - {description}")
        else:
            print(f"✗ {filename:25} MISSING - {description}")
            all_ok = False
    
    return all_ok


def check_directories():
    """Check if required directories exist"""
    print("\n" + "="*60)
    print("DIRECTORY STRUCTURE CHECK")
    print("="*60)
    
    base_dir = Path(__file__).parent
    
    # Check if it's in a proper location
    if base_dir.name != 'chimian':
        print(f"⚠ Project directory name: {base_dir.name} (usually should be 'chimian')")
    
    print(f"✓ Project location: {base_dir}")
    
    # Check for optional directories
    optional_dirs = ['test_files', 'samples', 'output']
    
    for dirname in optional_dirs:
        dirpath = base_dir / dirname
        if dirpath.exists():
            print(f"✓ {dirname:20} - exists")
        else:
            print(f"- {dirname:20} - not found (optional)")
    
    return True


def test_imports():
    """Test importing all modules"""
    print("\n" + "="*60)
    print("IMPORT FUNCTIONALITY TEST")
    print("="*60)
    
    try:
        print("Importing core modules...", end=" ")
        from enhanced_extractor import EnhancedPDFExtractor
        from excel_writer import ExcelWriter
        from unit_converter import UnitConverter
        from gui import MaterialExtractorGUI
        print("✓ All core modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {str(e)}")
        return False


def check_write_permissions():
    """Check if we can write files"""
    print("\n" + "="*60)
    print("FILE SYSTEM PERMISSIONS CHECK")
    print("="*60)
    
    try:
        test_file = Path(__file__).parent / ".test_write"
        test_file.write_text("test")
        test_file.unlink()
        print("✓ Write permissions OK - can create files")
        return True
    except Exception as e:
        print(f"✗ Write permission denied: {str(e)}")
        print("  Solution: Run with administrator privileges or use a different directory")
        return False


def system_info():
    """Display system information"""
    print("\n" + "="*60)
    print("SYSTEM INFORMATION")
    print("="*60)
    
    import platform
    
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.prefix}")
    print(f"Current working directory: {os.getcwd()}")


def main():
    """Run all checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "SETUP VERIFICATION SCRIPT" + " "*19 + "║")
    print("╚" + "="*58 + "╝")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Modules", check_modules),
        ("Project Files", check_files),
        ("Directories", check_directories),
        ("Write Permissions", check_write_permissions),
        ("Module Imports", test_imports),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n✗ Error during {check_name}: {str(e)}")
            results[check_name] = False
    
    system_info()
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {check_name}")
    
    print("\n" + "-"*60)
    print(f"Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ SYSTEM IS READY!")
        print("You can now run the application:")
        print("  python main.py")
        return 0
    else:
        print("\n✗ SETUP INCOMPLETE")
        print("Please fix the issues above before running the application.")
        print("\nCommon fixes:")
        print("1. Install Python 3.8+: https://www.python.org")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run as administrator if permission denied")
        return 1


if __name__ == "__main__":
    sys.exit(main())
