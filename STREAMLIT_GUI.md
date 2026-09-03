# Streamlit GUI - Modern Web-Based Interface

The Plastic Material Metrics Extractor now includes a modern Streamlit-based GUI with enhanced features.

## Features

### 🎨 Modern Web Interface
- Clean, responsive design
- Real-time progress tracking
- Interactive file upload
- Live extraction feedback

### 📋 Clipboard Functionality
- **Copy Excel Path** - One-click copy of output file path to clipboard
- **Download Button** - Direct download from the browser
- **Open Folder** - Quick access to output directory

### 🔧 Extensible Excel Export

The Excel writer has been redesigned to support:

#### Custom Columns
Define your own column structure:
```python
custom_columns = [
    {'name': 'Company', 'width': 15},
    {'name': 'Metric', 'width': 20},
    {'name': 'Value', 'width': 12, 'format': '0.0000'},
    {'name': 'Custom Field', 'width': 20},
]
excel_writer = ExcelWriter("output.xlsx", columns=custom_columns)
```

#### Custom Data Fields
Add any field to records:
```python
excel_writer.add_record(
    company="Supplier",
    material="ABS",
    metric_name="Tensile Strength",
    original_value=380,
    original_unit="kg/cm²",
    standard_value=37.3,
    standard_unit="MPa",
    custom_field="Your data here"  # Custom field
)
```

#### Custom Formatters
Apply custom formatting to columns:
```python
def format_unit(unit):
    return f"{unit} (SI)"

excel_writer.add_custom_formatter("Unit", format_unit)
```

## Installation

### Step 1: Install Streamlit
```bash
pip install streamlit pyperclip
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Launch the GUI
```bash
# Windows
run_streamlit.bat

# Linux/macOS
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage Workflow

### 1. Upload PDF Files
- Click "Browse files" to select one or more plastic datasheets
- Files are displayed with their sizes
- Use "Clear Files" to reset selection

### 2. Configure Output
- Enter desired filename (e.g., `material_report.xlsx`)
- Choose output directory (defaults to Downloads)
- Path is validated and shown

### 3. Extract & Generate
- Click "🚀 Extract & Generate Excel"
- Watch real-time progress in the interface
- Results show extraction summary

### 4. Get Your File
- **Copy Path** - Click to copy file path to clipboard
- **Open Folder** - Quick access to output directory
- **Download** - Download directly from browser
- Full path displayed for reference

## Advanced Configuration

### Extensible Metrics

Add support for new metrics by editing `config.py`:

```python
METRIC_KEYWORDS = {
    'new_metric': {
        'en': ['keyword1', 'keyword2'],
        'zh': ['中文关键字']
    }
}
```

### Custom Excel Schema

Modify column structure in your extraction code:

```python
from excel_writer import ExcelWriter

# Remove columns
excel_writer.remove_column("Test Method")

# Add custom columns
excel_writer.add_custom_column({
    'name': 'Temperature', 
    'width': 15
})

# Replace entire schema
excel_writer.set_custom_columns(my_columns)
```

### Format Numbers

Configure number formatting for columns:

```python
columns = [
    {'name': 'Value', 'format': '0.0000'},     # 4 decimals
    {'name': 'Percentage', 'format': '0.00%'},  # Percentage
    {'name': 'Integer', 'format': '0'},         # No decimals
]
```

## Examples

See `example_extensible_export.py` for complete examples:

```bash
python example_extensible_export.py
```

This demonstrates:
1. Basic extraction and export
2. Custom columns
3. Custom formatters
4. Multiple materials
5. Extended data fields
6. Minimal column set

## File Structure

```
c:\chimian\
├── streamlit_app.py          # Streamlit GUI (NEW)
├── run_streamlit.bat         # Streamlit launcher
├── example_extensible_export.py  # Extensibility examples
├── excel_writer.py           # Enhanced with extensibility
├── enhanced_extractor.py     # PDF extraction
├── unit_converter.py         # Unit conversions
└── ... (other files)
```

## Comparison: Tkinter vs Streamlit

| Feature | Tkinter | Streamlit |
|---------|---------|-----------|
| Interface | Desktop GUI | Web-based |
| Launch | Fast | Slightly slower |
| File Upload | Dialog | Drag-drop |
| Clipboard | Limited | Built-in copy button |
| Mobile | No | Responsive |
| Customization | Limited | Extensive |
| Modern Look | Basic | Modern |

## Troubleshooting

### Port Already in Use
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Clipboard Not Working
- Windows: Should work automatically
- Linux: Install `xclip` or `xsel`
- macOS: Should work automatically

### File Upload Issues
- Max file size may be limited by browser settings
- Use "Set file upload limits" in Streamlit config

### Memory Issues
- For large batches, extract files in groups
- Clear cache with `streamlit cache clear`

## Performance Tips

1. **Batch Processing**: Process similar materials together
2. **File Size**: Smaller PDFs process faster
3. **Memory**: Streamlit caches results automatically
4. **CPU**: Extraction is CPU-bound, not I/O-bound

## Keyboard Shortcuts

- **R**: Rerun app
- **C**: Clear cache
- **K**: Run in development mode (if applicable)

## Configuration

Edit `config.py` to customize:
- Keywords for metric detection
- Unit conversion factors
- Value validation ranges
- PDF extraction settings

## API Usage

Use the extraction engine programmatically:

```python
from streamlit_app import extract_pdfs, generate_excel_report

# Extract from files
results = extract_pdfs(uploaded_files)

# Generate report
success = generate_excel_report(results, output_path)
```

## Roadmap

- [ ] Material database backend
- [ ] Batch processing queue
- [ ] Real-time collaboration
- [ ] Advanced filtering
- [ ] Data visualization
- [ ] Export to PDF/CSV
- [ ] REST API
- [ ] Multi-language UI

## Support

For issues or questions:
1. Check README.md for general info
2. See example_extensible_export.py for examples
3. Review streamlit_app.py source code
4. Check Streamlit documentation

## License

Provided as-is for internal use.

---

**Enjoy the modern Streamlit interface!** 🚀

For detailed information, see README.md or QUICKSTART.md
