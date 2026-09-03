# Plastic Material Metrics Extractor

A Python application to extract key metrics from plastic material datasheets (PDFs) from different manufacturers and consolidate them into a single Excel file with standardized units.

## Features

- **Automated PDF Extraction**: Extracts 6 key metrics from plastic datasheets:
  - Tensile Strength
  - Flexural Strength
  - Density (with specific gravity conversion)
  - Tensile Modulus
  - Flexural Modulus
  - Elongation

- **Unit Standardization**: Automatically converts the extracted metrics to standard units:
  - Tensile Strength, Flexural Strength, Tensile Modulus, Flexural Modulus → **MPa**
  - Density → **tonnes/mm³** (converted from g/cm³, kg/m³, specific gravity, etc.)
  - Elongation → **strain** (dimensionless, converted from %)
  
  A few additional general-purpose converters exist (Length → mm, Mass → tonnes,
  Time → seconds, Force → Newton) for future use but aren't applied to the 6
  tracked metrics above.

- **Organized Output**: 
  - Creates separate Excel tabs for each material type
  - Groups data by manufacturer
  - Preserves original values and units
  - Shows both original and standardized measurements

- **Simple GUI**: User-friendly interface for selecting files and generating reports

## Installation

1. **Clone or download this project**

2. **Install Python 3.8 or higher**

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Via GUI (Recommended)

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **In the GUI window**:
   - Click "Select PDF Files" and choose one or more plastic material datasheets
   - Click "Choose Output Path" and select where to save the Excel file
   - Click "Extract & Generate Excel"

3. **View Results**:
   - The Excel file will open with tabs for each material type
   - Each tab contains data from all manufacturers for that material
   - Compare metrics across different suppliers

### Via Command Line

```python
from advanced_extractor import AdvancedPDFExtractor, MetricWithConversion
from excel_writer import DataOrganizer
from unit_converter import UnitConverter

# Extract data
extractor = AdvancedPDFExtractor("your_file.pdf")
result = extractor.extract_all()

# Generate Excel
organizer = DataOrganizer()
organizer.add_extraction_result(result)
organizer.generate_excel("output.xlsx", UnitConverter())
```

## Supported PDF Formats

The extractor is designed to work with:
- Datasheet tables with property names and values
- Technical specification PDFs
- Material datasheets from various manufacturers

Currently tested with:
- Eastern Ever International ABS (AR130)
- Kingfa ECOEX® ABS (GAR-011)
- Lavergne VYTEEN™ ABS
- FCFC Plastics Formosa ABS

## Output Format

Each material gets its own Excel sheet, grouped by manufacturer/company. Every
metric row contains both the as-listed datasheet value and the standardized
(converted) value side by side:

| Column | Description |
|--------|-------------|
| PROPERTY | Metric name (Tensile Strength, Density, etc.) |
| TEST METHOD | Testing standard (ASTM D638, ISO 527, etc.) |
| TEST CONDITION | Test condition as listed (speed, span, temperature, etc.) |
| UNIT (FILE) | Unit exactly as listed in the datasheet |
| VALUE (FILE) | Value exactly as listed in the datasheet |
| UNIT (CONVERTED) | Standardized unit (see Unit Conversion Reference below) |
| VALUE (CONVERTED) | Value converted to the standardized unit |

## Project Structure

```
c:\chimian\
├── main.py                  # Entry point
├── gui.py                   # GUI application
├── pdf_extractor.py         # Basic PDF extraction
├── advanced_extractor.py    # Advanced PDF parsing
├── unit_converter.py        # Unit conversion utilities
├── excel_writer.py          # Excel file generation
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## How It Works

1. **PDF Extraction**: Uses pdfplumber to extract text and tables from PDFs
2. **Metric Identification**: Searches for keywords (English and Chinese) to identify metrics
3. **Value Parsing**: Extracts numeric values and their associated units
4. **Unit Conversion**: Standardizes all measurements to consistent units
5. **Excel Generation**: Organizes data by material type and exports to Excel

## Unit Conversion Reference

The standardized unit is always shown in the UNIT (CONVERTED) column; the
original datasheet unit/value are preserved unchanged in UNIT (FILE) / VALUE (FILE).

### Tensile/Flexural Strength & Tensile/Flexural Modulus → MPa
- MPa (already standard, passed through)
- PSI → MPa
- kPa, GPa, Pa → MPa
- kg/cm², kgf/cm², kg·cm⁻² → MPa
- N/mm² (equivalent to MPa)

### Density → tonnes/mm³
- g/cm³ → tonnes/mm³ (× 1e-9)
- kg/m³ → tonnes/mm³ (× 1e-12)
- tonnes/m³, tonnes/cm³ → tonnes/mm³
- Specific gravity (unitless) → tonnes/mm³ (assumes water = 1 g/cm³)

Note: the converted density values are intentionally expressed in
tonnes/mm³ (not the more common g/cm³) - this is very small in magnitude
(e.g. 1.06 g/cm³ → ~1.06e-9 tonnes/mm³), which is expected.

### Elongation → strain (dimensionless)
- Percentage (%) → strain (divide by 100)
- Already unitless/strain values are passed through

### General-purpose converters (not currently applied to the 6 tracked metrics)
- Length: mm, cm, m, inch, µm → mm
- Time: s, min, hr, day → seconds
- Mass: kg, g, mg, lb, oz → tonnes
- Force: N, kN, kgf, lbf → Newton

## Limitations

- Requires PDFs to contain tables or structured text
- Accuracy depends on PDF structure consistency
- May require manual verification for unusual formats
- Chinese text support for common material terms

## Troubleshooting

**Issue**: "No metrics found" for a PDF
- **Solution**: Ensure the PDF contains clear tables or structured data with metric names

**Issue**: Incorrect unit conversions
- **Solution**: Check if the original unit is spelled consistently; you may need to add custom patterns

**Issue**: Permission denied when saving Excel
- **Solution**: Ensure the output directory is writable and not protected

## Future Enhancements

- Support for more material types (PP, PE, PETG, etc.)
- Better handling of range values (e.g., "100-120 MPa")
- Extraction of test conditions (temperature, pressure, etc.)
- Support for more languages
- Batch processing improvements

## Contributing

To add support for new materials or PDF formats:

1. Test the PDF with the current extractor
2. Add new keywords to `METRIC_KEYWORDS` if needed
3. Improve the `_extract_from_row()` method if needed
4. Test with sample PDFs

## License

This project is provided as-is for internal use.

## Support

For issues or questions, please check:
1. That the PDF contains standard property tables
2. That you have all required dependencies installed
3. The PDF is not password-protected
4. Your system has sufficient disk space for the output

---

**Last Updated**: 2026-09-02
**Version**: 1.0
