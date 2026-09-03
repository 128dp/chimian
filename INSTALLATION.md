# Installation Guide

## System Requirements

- **Windows 10/11** or **Linux/macOS** with Python installed
- **Python 3.8 or higher**
- **4 GB RAM** (minimum)
- **500 MB free disk space**

## Step-by-Step Installation

### Method 1: Automatic Installation (Windows - Recommended)

1. **Download and Extract**
   - Extract the project files to a folder (e.g., `C:\chimian`)

2. **Run Installation Script**
   - Double-click `install.bat`
   - Wait for all packages to download and install
   - A message will appear when complete

3. **Launch Application**
   - Double-click `run.bat`
   - The GUI should open

### Method 2: Manual Installation (All Platforms)

#### Step 1: Install Python
1. Download Python 3.8+ from https://www.python.org
2. During installation, **CHECK** "Add Python to PATH"
3. Click "Install Now"
4. Verify installation:
   ```bash
   python --version
   pip --version
   ```

#### Step 2: Install Dependencies
1. Open Command Prompt or PowerShell
2. Navigate to project folder:
   ```bash
   cd c:\chimian
   ```
3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```

#### Step 3: Run Application
```bash
python main.py
```

### Method 3: Using Virtual Environment (Advanced)

For isolated installation:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run app
python main.py
```

## Troubleshooting Installation

### Python Not Found
**Error**: `'python' is not recognized`

**Solution**:
1. Reinstall Python and check "Add Python to PATH"
2. Or use full path: `C:\Python312\python.exe main.py`
3. Restart Command Prompt after installing Python

### pip Command Not Found
**Error**: `'pip' is not recognized`

**Solution**:
```bash
# Use Python to run pip
python -m pip install -r requirements.txt
```

### Permission Denied
**Error**: `Permission denied` when running install.bat

**Solution**:
1. Right-click `install.bat`
2. Select "Run as administrator"
3. Or manually run the pip command as shown above

### Module Import Error
**Error**: `ModuleNotFoundError: No module named 'pdfplumber'`

**Solution**:
1. Make sure pip install completed without errors
2. Try reinstalling:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Port Already in Use
**Error**: `Address already in use`

**Solution**:
This shouldn't occur with the GUI app. If it does:
1. Close any other Python windows
2. Restart your computer

## Verifying Installation

After installation, verify everything works:

```bash
# Test imports
python -c "import pdfplumber, openpyxl, pandas; print('✓ All modules loaded')"

# Run demo
python demo.py

# Test extraction (if you have PDFs in test_files folder)
python test_extraction.py
```

## First Run

1. **Launch GUI**: Double-click `run.bat` (Windows) or run `python main.py`

2. **Select PDF Files**:
   - Click "Select PDF Files"
   - Choose plastic material datasheets
   - Files appear in the status area

3. **Choose Output Location**:
   - Click "Choose Output Path"
   - Select where to save the Excel file

4. **Extract Data**:
   - Click "Extract & Generate Excel"
   - Watch progress in the log window
   - Excel file will be saved when complete

## Updating the Program

To update to a newer version:

1. Backup your Excel output files
2. Replace the Python files with new versions
3. Run `install.bat` or `pip install -r requirements.txt` again

## Uninstallation

To remove the program:

1. **Windows**: Simply delete the folder
   ```bash
   rmdir /s c:\chimian
   ```

2. **Python packages** (if needed):
   ```bash
   pip uninstall pdfplumber openpyxl pandas pillow
   ```

## Getting Help

If you encounter issues:

1. **Check the log window** in the GUI for error messages
2. **Run demo.py** to test basic functionality
3. **Review QUICKSTART.md** for usage tips
4. **Check README.md** for detailed documentation

### Common Issues

| Problem | Solution |
|---------|----------|
| No metrics found | Check PDF has clear metric names |
| Wrong values extracted | Verify PDF format is supported |
| Excel file won't open | Ensure output location is writable |
| Application crashes | Update Python and dependencies |

## Advanced Configuration

To customize the extraction:

1. Edit `config.py` to add keywords
2. Modify `unit_converter.py` for new unit types
3. Update `enhanced_extractor.py` for extraction logic

## System Paths

On different systems, project might be located at:

- Windows: `C:\chimian\`
- Linux: `/home/user/chimian/`
- macOS: `/Users/user/chimian/`

Replace paths in instructions as needed.

## Next Steps

1. **Try the demo**: `python demo.py`
2. **Extract sample data**: Use provided test PDFs
3. **Customize settings**: Edit `config.py`
4. **Process your data**: Use GUI to extract metrics

---

**Congratulations!** You've successfully installed the Plastic Material Metrics Extractor. 

For detailed usage, see **QUICKSTART.md** or **README.md**.
