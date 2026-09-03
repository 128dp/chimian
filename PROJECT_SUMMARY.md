# Project Summary

## Plastic Material Metrics Extractor

A comprehensive Python application for extracting key material properties from plastic datasheet PDFs and consolidating them into standardized Excel reports.

## What It Does

### Input
- Accepts multiple PDF files from different plastic manufacturers
- Supports datasheets in English and Chinese
- Works with various PDF formats (table-based, text-based)

### Processing
1. **Extracts 6 Key Metrics**:
   - Tensile Strength
   - Flexural Strength  
   - Density (with specific gravity conversion)
   - Tensile Modulus
   - Flexural Modulus
   - Elongation

2. **Standardizes Units**:
   - Converts all measurements to consistent units
   - Preserves original values for reference
   - Handles multiple unit types (metric, imperial, etc.)

3. **Organizes Data**:
   - Groups results by material type
   - Separates by manufacturer
   - Creates comparison tables

### Output
- **Excel File** with:
  - One tab per material type
  - Original values and units
  - Standardized values and units
  - Test method information
  - Professional formatting

## Key Features

✓ **Simple GUI** - No technical knowledge required  
✓ **Batch Processing** - Extract from multiple PDFs at once  
✓ **Unit Conversion** - Automatic standardization to SI units  
✓ **Material Comparison** - Compare specs across manufacturers  
✓ **Configurable** - Customize keywords and conversions  
✓ **Extensible** - Add new materials and metrics  
✓ **Demo Mode** - Understand how it works  
✓ **Test Suite** - Validate extraction accuracy

## Files Included

### Core Application
- `main.py` - Application launcher
- `gui.py` - User interface
- `enhanced_extractor.py` - Advanced PDF extraction engine
- `unit_converter.py` - Unit conversion utilities
- `excel_writer.py` - Excel file generation
- `config.py` - Configuration and customization

### Testing & Documentation
- `demo.py` - Demonstration of features
- `test_extraction.py` - Extract testing
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `INSTALLATION.md` - Installation instructions
- `CHANGELOG.md` - Version history

### Utilities
- `requirements.txt` - Python dependencies
- `install.bat` - Automatic installation (Windows)
- `run.bat` - Quick launcher (Windows)

## Supported Formats

### PDF Layouts
- ✓ Table-based datasheets
- ✓ Structured text documents
- ✓ Mixed format (tables + text)
- ✓ Multi-page documents
- ✗ Image-only PDFs (scanned)

### Materials
- ABS (Acrylonitrile-Butadiene-Styrene)
- PP (Polypropylene)
- PE (Polyethylene)
- PETG (Polyethylene Terephthalate Glycol)
- PLA (Polylactic Acid)
- *Extensible for other materials*

### Manufacturers
- Eastern Ever International
- Kingfa
- Lavergne
- FCFC Plastics
- Formosa
- *And many more*

## Technical Details

### Architecture
```
GUI (Tkinter)
    ↓
Enhanced PDF Extractor (pdfplumber)
    ↓
Unit Converter
    ↓
Excel Writer (openpyxl)
    ↓
Output File
```

### Dependencies
- **pdfplumber** - PDF text and table extraction
- **openpyxl** - Excel file generation
- **pandas** - Data organization
- **pillow** - Image processing support
- **Python 3.8+** - Runtime environment

### Unit Support

**Stress/Modulus**: MPa, GPa, kPa, Pa, psi, kg/cm²  
**Density**: g/cm³, kg/m³  
**Length**: mm, cm, m, inch  
**Time**: s, min, hr  
**Mass**: tonne, kg, g, lb  
**Force**: N, kN, kgf, lbf  
**Elongation**: %, strain  

## Usage Workflow

1. **Install** - Run `install.bat` or `pip install -r requirements.txt`
2. **Launch** - Run `main.py` or double-click `run.bat`
3. **Select** - Choose PDF files to process
4. **Configure** - Set output location
5. **Extract** - Click "Extract & Generate Excel"
6. **Review** - Open and analyze results

## Performance

- **Single PDF**: ~1-5 seconds
- **Batch (10 files)**: ~10-30 seconds
- **Memory Usage**: ~50-100 MB
- **Output File Size**: ~100-500 KB

## Customization

### Adding Keywords
Edit `config.py` and add to `METRIC_KEYWORDS`:
```python
'my_metric': {
    'en': ['keyword1', 'keyword2'],
    'zh': ['中文关键字']
}
```

### Adding Units
Edit `unit_converter.py` and add conversion factors:
```python
STRESS_TO_MPA = {
    'custom_unit': 0.5,  # conversion factor
}
```

### Adjusting Value Ranges
Edit `config.py` and modify `VALUE_RANGES`:
```python
VALUE_RANGES = {
    'tensile_strength': (1, 200),  # min, max
}
```

## Limitations

- PDFs must have selectable text (not scanned images)
- Metric names must be clearly labeled
- Units should follow standard notation
- Works best with structured table layouts
- Chinese support for common material terms only

## Future Enhancements

- [ ] Support for more material types
- [ ] Range value extraction (e.g., "100-120 MPa")
- [ ] Automatic test condition extraction
- [ ] Multi-language support enhancement
- [ ] Database backend integration
- [ ] Web UI version
- [ ] Real-time collaboration features

## Getting Started

### Quick Start (2 minutes)
1. Run `install.bat`
2. Double-click `run.bat`
3. Select PDFs and click "Extract"

### Learn More
- See **QUICKSTART.md** for basic usage
- See **INSTALLATION.md** for setup details
- See **README.md** for complete documentation
- Run `python demo.py` for examples

## Troubleshooting

**No metrics found?**
- Check PDF has metric names (Tensile Strength, Density, etc.)
- Verify PDF text is selectable
- Try different PDFs to test

**Wrong values?**
- Verify original PDF values
- Check unit conversion logic
- Review extraction log for clues

**Excel won't open?**
- Ensure output directory exists
- Check file path has no invalid characters
- Try different output location

## Support Resources

| Resource | Location |
|----------|----------|
| Quick Start | QUICKSTART.md |
| Installation | INSTALLATION.md |
| Full Docs | README.md |
| Examples | demo.py |
| Testing | test_extraction.py |
| Configuration | config.py |

## Version Information

- **Current Version**: 1.0
- **Release Date**: 2026-09-02
- **Python**: 3.8+
- **Status**: Stable

## License

Provided as-is for internal use and development.

## Contact & Support

For issues, questions, or feature requests:
1. Check the documentation files
2. Review the demo script
3. Test with sample PDFs
4. Check configuration options

---

**Thank you for using the Plastic Material Metrics Extractor!**

For detailed information, please refer to the documentation files included in the project.
