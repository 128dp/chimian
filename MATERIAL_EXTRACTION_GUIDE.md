# Material-Based Extraction with All 6 Metrics - User Guide

## 🎯 What's New

The Plastic Material Metrics Extractor has been enhanced with two major improvements:

### 1. **Material Type Selection**
- Choose material type before uploading PDFs (ABS, PP, PE, PET, etc.)
- All files for the same material are automatically organized in one Excel tab
- Supports custom material names for flexibility

### 2. **All 6 Metrics Display**
- Every company now shows all 6 metrics in one row (when extracted)
- Metrics displayed as columns for easy comparison
- Standardized units across all materials:
  - **Tensile Strength**: MPa
  - **Flexural Strength**: MPa
  - **Density**: g/cm³
  - **Tensile Modulus**: MPa
  - **Flexural Modulus**: MPa
  - **Elongation**: strain

## 📊 Excel Organization

### Before (Old Format)
```
| Company  | Metric           | Original Value | Original Unit | Standard Value | Standard Unit |
|----------|------------------|----------------|---------------|----------------|---------------|
| Kingfa   | Tensile Strength | 40             | MPa           | 40             | MPa           |
| Kingfa   | Density          | 1.05           | g/cm³         | 1.05           | g/cm³         |
| Lavergne | Tensile Strength | 45             | MPa           | 45             | MPa           |
```

### After (New Format) ✨
```
| Company  | Tensile Strength | Flexural Strength | Density | Tensile Modulus | Flexural Modulus | Elongation |
|----------|------------------|-------------------|---------|-----------------|------------------|------------|
| Kingfa   | 40.0             | 65.0              | 1.050   | 2300.0          | 2400.0           | 0.25       |
| Lavergne | 45.0             | 70.0              | 1.055   | 2400.0          | 2500.0           | 0.20       |
| BASF     | 42.0             | 68.0              | 1.052   | 2350.0          | 2450.0           | 0.23       |
| Dow      | 38.0             | 62.0              | 1.048   | 2250.0          | 2350.0           | 0.22       |
```

**Benefits:**
- ✓ All metrics visible at a glance
- ✓ Easy horizontal comparison between companies
- ✓ One row per company (cleaner layout)
- ✓ Professional formatting with alternating row colors
- ✓ Frozen header row for easy scrolling

## 🚀 Step-by-Step Usage

### Step 1: Select Material & Upload PDFs

1. **Choose Material Type** from dropdown
   - Options: ABS, PP, PE, PET, PC, PVC, PMMA, or Other
   - Selected material: "📌 Material: ABS - All files will be saved under this material tab"

2. **Upload PDF Files**
   - Click "Choose File" or drag-drop PDFs
   - Select multiple files at once (all 4 ABS files in your case)
   - Files display with their names and sizes

3. **Organize by Material**
   - All files from this upload will go to the same sheet
   - Sheet name = Material type (e.g., "ABS")
   - To process multiple materials:
     - Upload ABS files first → generates Excel
     - Change material to PP
     - Upload PP files → same Excel, new tab for PP
     - (Or start fresh for separate files)

### Step 2: Configure Output

1. **Output Filename**: `material_extraction.xlsx`
   - Choose any name you want
   - File will be saved as Excel format

2. **Output Directory**: `C:\Users\YourName\Downloads`
   - Default: Downloads folder
   - Change to save elsewhere
   - Creates directory if it doesn't exist

### Step 3: Extract & Generate

1. **Click "🚀 Extract & Generate Excel"**
   - Shows progress bar
   - Extracts all 6 metrics from PDFs
   - Converts units to standard format
   - Generates formatted Excel file

2. **Download or Copy Path**
   - ✓ "📋 Copy Path" - One-click clipboard copy
   - ✓ "📥 Download" - Direct browser download
   - ✓ Full file path shown for reference

## 📋 Example Workflow

**Scenario: Processing 4 ABS manufacturer datasheets**

```
Step 1: Select Material & Upload
  ├─ Material: ABS
  ├─ Upload: kingfa_abs.pdf
  ├─ Upload: lavergne_abs.pdf
  ├─ Upload: basf_abs.pdf
  └─ Upload: dow_abs.pdf

Step 2: Configure Output
  ├─ Filename: abs_properties.xlsx
  └─ Directory: C:\Users\YourName\Downloads

Step 3: Extract & Generate
  ├─ Extract metrics from 4 PDFs
  ├─ Convert all units to standard
  ├─ Create "ABS" sheet
  ├─ Add 4 rows (one per company)
  ├─ Format headers and borders
  └─ Save file: abs_properties.xlsx

Result:
  ✓ One Excel file with ABS tab
  ✓ 4 companies shown
  ✓ All 6 metrics in columns
  ✓ Professional formatting
  ✓ Ready for analysis
```

## 🎨 Excel Features

### Formatting
- **Header Row**
  - Dark blue background (#1F4E78)
  - White bold text
  - Centered alignment
  - Frozen (stays visible when scrolling)

- **Data Rows**
  - Alternating light blue/white for readability
  - Centered text alignment
  - Thin borders for definition
  - Number format: 4 decimal places

- **Column Widths**
  - Auto-sized for content
  - Company: 18 characters
  - Metrics: 16-20 characters
  - All values clearly visible

### Units Displayed
All metrics show standardized units in column headers:
- Tensile Strength (MPa)
- Flexural Strength (MPa)
- Density (g/cm³)
- Tensile Modulus (MPa)
- Flexural Modulus (MPa)
- Elongation (strain)

## 🔧 Configuration Options

### Add More Materials
To add custom material types, edit the UI in `streamlit_app.py`:

```python
material_options = [
    "ABS",
    "PP (Polypropylene)",
    "PE (Polyethylene)",
    "Custom Material",
]
```

### Adjust Column Order
To change metric column order, edit `excel_writer.py`:

```python
DEFAULT_COLUMNS = [
    {'name': 'Company', 'width': 18},
    {'name': 'Density (g/cm³)', 'width': 16},  # Move density first
    {'name': 'Tensile Strength (MPa)', 'width': 18},
    # ... other metrics
]
```

### Customize Formatting
To change colors, borders, or styling:

```python
# In _create_material_sheet method
header_fill = PatternFill(start_color="1F4E78", ...)  # Change color code
header_font = Font(bold=True, color="FFFFFF", ...)  # Change font
```

## 📚 Files Modified

1. **streamlit_app.py**
   - Added material_type to session state
   - Added material selector UI (Step 1)
   - Updated extract_pdfs() to accept material_type
   - Updated generate_excel_report() for all 6 metrics

2. **excel_writer.py**
   - Changed DEFAULT_COLUMNS to show all 6 metrics
   - Updated _create_material_sheet() mapping
   - Added alternating row colors
   - Improved formatting and styling

3. **demo_material_extraction.py** (NEW)
   - Demonstrates new functionality
   - Shows sample data for 4 ABS companies
   - Generates demo_abs_extraction.xlsx

## 🧪 Testing

### Run Demo
```bash
cd c:\chimian
python demo_material_extraction.py
```

This generates `demo_abs_extraction.xlsx` with sample data showing:
- Material: ABS
- Companies: Kingfa, Lavergne, BASF, Dow
- All 6 metrics per company
- Standardized units

### Try with Real PDFs
1. Open http://localhost:8501
2. Select Material: ABS
3. Upload your 4 ABS datasheets
4. Configure output filename
5. Click "Extract & Generate Excel"
6. Download and review

## 🐛 Troubleshooting

### Issue: Only 1 metric showing
- **Solution**: Ensure PDFs contain data for multiple metrics
- Check extraction log to see which metrics were found

### Issue: Material not showing as tab name
- **Solution**: Check character limit (Excel max 31 chars)
- Material name is truncated if longer

### Issue: Values show as "-" for some metrics
- **Solution**: Metric not found in that PDF
- Different manufacturers include different properties
- "-" indicates metric was not extracted

### Issue: Units not converting correctly
- **Solution**: Check original unit is recognized
- Update config.py if using non-standard units

## ✨ Benefits Summary

✅ **User Experience**
- Intuitive material selection
- All 6 metrics in one view
- Professional Excel formatting
- One-click path copying

✅ **Data Organization**
- Material-based tabs
- Company-per-row layout
- Standardized units
- Easy comparison

✅ **Efficiency**
- Process multiple files at once
- Batch by material type
- Automatic unit conversion
- Ready-to-use Excel output

## 📞 Next Steps

1. **Test with Your PDFs**
   - Upload 4 ABS files
   - Verify all metrics extract
   - Check Excel formatting

2. **Process Other Materials**
   - Change material to PP
   - Upload PP datasheets
   - Compare with ABS data

3. **Customize for Your Needs**
   - Add more material types
   - Adjust formatting
   - Modify column order

---

**Happy extracting!** 📊✨

For detailed setup and installation, see README.md or QUICKSTART.md
