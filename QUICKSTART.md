# Quick Start Guide

## Installation (First Time Only)

### Option 1: Automatic Installation (Windows)
1. Double-click `install.bat`
2. Wait for all packages to install
3. A console window will confirm when complete

### Option 2: Manual Installation
1. Open Command Prompt or PowerShell
2. Navigate to the project folder:
   ```
   cd c:\chimian
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Quick Start (Windows)
Double-click `run.bat`

### Option 2: Command Line
```bash
python main.py
```

### Option 3: Build a Windows EXE
Run `build_exe.bat`. The packaged application will be created at
`dist\Chimian\Chimian.exe` and can be copied to another Windows computer.

## Using the Application

### Step 1: Select PDF Files
1. Click "Select PDF Files" button
2. Choose one or more plastic material datasheets
3. Files are listed in the status area

### Step 2: Choose Output Location
1. Click "Choose Output Path" button
2. Select where to save the Excel file
3. Type a filename (e.g., `materials_comparison.xlsx`)

### Step 3: Extract Data
1. Click "Extract & Generate Excel"
2. Watch the progress in the log window
3. When complete, the Excel file will be automatically saved

### Step 4: Review Results
1. Open the generated Excel file
2. Each material type has its own tab
3. Compare metrics from different manufacturers
4. All values are in standardized units

## Output Format

Each Excel tab contains:

| Column | Contains |
|--------|----------|
| Company | Manufacturer/Supplier name |
| Metric | Property name (e.g., Tensile Strength) |
| Original Value | Value from the datasheet |
| Original Unit | Unit as shown in datasheet |
| Test Method | Testing standard used (ASTM, UL, etc.) |
| Standardized Value | Converted to standard unit |
| Standardized Unit | Standard unit (MPa, g/cm³, etc.) |

## Example Metrics Extracted

### Tensile Strength
- **Original Units**: kg/cm², psi, N/mm², MPa
- **Standardized**: MPa

### Flexural Strength
- **Original Units**: kg/cm², psi, N/mm²
- **Standardized**: MPa

### Density
- **Original Units**: g/cm³, kg/m³, specific gravity
- **Standardized**: g/cm³

### Modulus (Tensile & Flexural)
- **Original Units**: kg/cm², psi, N/mm²
- **Standardized**: MPa

### Elongation
- **Original Units**: % (percentage), dimensionless
- **Standardized**: strain (decimal form)

## Supported PDF Formats

The tool works best with datasheets that contain:
- Structured tables with property names and values
- Clear metric labels (in English or Chinese)
- Consistent unit notation

## Tips for Best Results

1. **PDF Quality**
   - Use clear, readable PDFs
   - Avoid scanned images with poor quality
   - PDFs with selectable text work best

2. **File Organization**
   - Group similar materials before extraction
   - Keep different material types separate
   - Name files clearly with material type

3. **Verification**
   - Always verify extracted values
   - Check for reasonable ranges
   - Compare with original datasheets

## Troubleshooting

### "No files selected" Error
- Click "Select PDF Files" and choose at least one PDF

### "No output location selected" Error
- Click "Choose Output Path" and specify where to save

### "No metrics found" in the Excel
- The PDF may have unusual formatting
- Try converting PDF to a different format
- Check that the PDF contains the metric names

### Application Won't Start
- Ensure Python 3.8+ is installed
- Run `install.bat` to reinstall dependencies
- Check for error messages in the console window

## Demo Mode

To see how the tool works without processing PDFs:

1. Open Command Prompt in the project folder
2. Run: `python demo.py`
3. This shows unit conversions and extraction examples

## Advanced Usage

### Using in Your Code

```python
from advanced_extractor import AdvancedPDFExtractor
from excel_writer import DataOrganizer
from unit_converter import UnitConverter

# Extract from PDF
extractor = AdvancedPDFExtractor("datasheet.pdf")
result = extractor.extract_all()

# Generate Excel
organizer = DataOrganizer()
organizer.add_extraction_result(result)
organizer.generate_excel("output.xlsx", UnitConverter())
```

### Adding New Materials

Edit the `METRIC_KEYWORDS` dictionary in `advanced_extractor.py` to add support for new material types.

## File Structure

```
c:\chimian\
├── main.py                  # Application launcher
├── gui.py                   # GUI interface
├── advanced_extractor.py    # PDF extraction engine
├── unit_converter.py        # Unit conversion utilities
├── excel_writer.py          # Excel file generation
├── demo.py                  # Demonstration script
├── requirements.txt         # Python dependencies
├── install.bat              # Installation script (Windows)
├── run.bat                  # Quick launcher (Windows)
├── README.md                # Full documentation
└── QUICKSTART.md           # This file
```

## Getting Help

1. Check README.md for detailed documentation
2. Run demo.py to understand how extraction works
3. Review the console log for error details
4. Verify PDF has clear metric names and values

## Next Steps

1. **Process Your First PDFs**: Select a few datasheets and extract
2. **Review the Excel Output**: Check the generated file
3. **Customize**: Adjust for your specific materials if needed
4. **Batch Processing**: Process multiple files regularly

---

**Happy extracting!** 📊

For more details, see README.md
