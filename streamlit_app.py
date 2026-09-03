"""
Streamlit-based GUI for Plastic Material Metrics Extractor
Modern web-based interface with clipboard copy functionality
"""

import streamlit as st
import os
from pathlib import Path
import tempfile
import pyperclip
from enhanced_extractor import EnhancedPDFExtractor
from excel_writer import ExcelWriter, DataOrganizer
from unit_converter import UnitConverter
from collections import defaultdict

# Page configuration
st.set_page_config(
    page_title="Plastic Material Metrics Extractor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
# NOTE: these boxes set an explicit text `color` (not just background) so
# they stay readable in BOTH Streamlit's light and dark themes. Relying on
# the theme's default text color on top of a hardcoded light background was
# causing near-invisible text for dark-theme users.
st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f2f6;
        color: #1a1a2e;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    .success-box h3, .success-box p { color: #155724; margin: 0 0 4px 0; }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 10px 0;
    }
    .error-box h3, .error-box p { color: #721c24; margin: 0 0 4px 0; }
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'material_name' not in st.session_state:
        st.session_state.material_name = "ABS"
    if 'output_path' not in st.session_state:
        st.session_state.output_path = None
    if 'extraction_results' not in st.session_state:
        st.session_state.extraction_results = {}  # {company: [result_items]}
    if 'excel_generated' not in st.session_state:
        st.session_state.excel_generated = False
    if 'last_excel_path' not in st.session_state:
        st.session_state.last_excel_path = None


def copy_to_clipboard(text):
    """Copy text to clipboard"""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        st.error(f"Failed to copy to clipboard: {str(e)}")
        return False


def format_bytes(bytes_size):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"


def extract_pdfs(pdf_files, material_type):
    """Extract metrics from PDF files"""
    results = defaultdict(list)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    converter = UnitConverter()
    
    for idx, pdf_file in enumerate(pdf_files):
        try:
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(pdf_file.read())
                tmp_path = tmp.name
            
            status_text.text(f"Processing: {pdf_file.name}...")
            
            # Extract metrics
            extractor = EnhancedPDFExtractor(tmp_path)
            result = extractor.extract_all()
            
            if result.get('metrics'):
                # Get company name from filename
                company_name = Path(pdf_file.name).stem
                
                results[company_name].append({
                    'file': pdf_file.name,
                    'company': company_name,
                    'material': material_type,
                    'metrics': result['metrics'],
                    'converter': converter
                })
                st.success(f"✓ {pdf_file.name} - Found {len(result['metrics'])} metric(s)")
            else:
                st.warning(f"⚠ {pdf_file.name} - No metrics found")
            
            # Cleanup
            os.unlink(tmp_path)
        
        except Exception as e:
            st.error(f"✗ {pdf_file.name} - Error: {str(e)}")
        
        # Update progress
        progress_bar.progress((idx + 1) / len(pdf_files))
    
    progress_bar.empty()
    status_text.empty()
    
    return results


def _organize_company_metrics(extraction_results):
    """Organize one material's extraction results by company, converting each
    entry to standardized SI units. Each metric can have MULTIPLE entries
    when the datasheet lists it under different test conditions."""
    converter = UnitConverter()

    def convert_entry(metric_key, value, unit):
        """Convert an extracted value/unit to standardized SI units."""
        if metric_key in ('tensile_strength', 'flexural_strength',
                          'tensile_modulus', 'flexural_modulus'):
            return converter.convert_stress(value, unit)
        elif metric_key == 'density':
            return converter.convert_density(value, unit)
        elif metric_key == 'elongation':
            return converter.convert_elongation(value, unit)
        return value, unit

    company_data = {}
    for company_name, results_list in extraction_results.items():
        company_metrics = {}

        for result_item in results_list:
            metrics = result_item['metrics']

            for metric_key, entries in metrics.items():
                bucket = company_metrics.setdefault(metric_key, [])
                for entry in entries:
                    if not isinstance(entry, dict):
                        # Defensive: skip malformed entries instead of
                        # crashing on entry.get(...) below.
                        continue

                    original_value = entry.get('value')
                    original_unit = entry.get('unit')
                    raw_value = entry.get('raw_value')

                    std_value, std_unit = convert_entry(metric_key, original_value, original_unit)

                    bucket.append({
                        'test_method': entry.get('test_method'),
                        'test_condition': entry.get('test_condition'),
                        'unit_file': original_unit,
                        'value_file': raw_value if raw_value not in (None, '') else original_value,
                        'unit_si': std_unit,
                        'value_si': std_value,
                    })

        company_data[company_name] = company_metrics

    return company_data


def generate_combined_excel_report(all_results, output_path, existing_workbook_bytes=None):
    """Generate an Excel report covering one or more materials in a single
    workbook. If `existing_workbook_bytes` is provided, new material sheets
    are added alongside the existing ones, and materials that already have
    a sheet get their new companies appended below the existing content
    instead of being overwritten.

    Args:
        all_results: {material_name: {company_name: [result_items]}}
        output_path: where to save the resulting workbook
        existing_workbook_bytes: optional bytes of an uploaded .xlsx file to merge into
    """
    try:
        excel_writer = ExcelWriter(output_path, existing_workbook_bytes=existing_workbook_bytes)

        for material_name, extraction_results in all_results.items():
            company_data = _organize_company_metrics(extraction_results)

            for company_name, metrics_dict in company_data.items():
                excel_writer.add_record(
                    company=company_name,
                    material=material_name,
                    metrics=metrics_dict
                )

        excel_writer.create_sheets()
        excel_writer.save()

        return True, None

    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, str(e)


def get_metric_name(metric_key):
    """Convert metric key to display name"""
    names = {
        'tensile_strength': 'Tensile Strength',
        'flexural_strength': 'Flexural Strength',
        'density': 'Density',
        'tensile_modulus': 'Tensile Modulus',
        'flexural_modulus': 'Flexural Modulus',
        'elongation': 'Elongation'
    }
    return names.get(metric_key, metric_key.replace('_', ' ').title())


def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.title("📊 Plastic Material Metrics Extractor")
    st.markdown("Extract and standardize material properties from PDF datasheets.")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Add custom metrics option
        st.subheader("Extensible Metrics")
        add_custom_metrics = st.checkbox("Add custom metrics?", value=False)
        
        if add_custom_metrics:
            st.info("Custom metrics can be configured in the config.py file")
            with st.expander("View supported metrics"):
                metrics = [
                    "✓ Tensile Strength (MPa)",
                    "✓ Flexural Strength (MPa)",
                    "✓ Density (tonnes/mm³)",
                    "✓ Tensile Modulus (MPa)",
                    "✓ Flexural Modulus (MPa)",
                    "✓ Elongation (strain)"
                ]
                for metric in metrics:
                    st.write(metric)
        
        # Unit settings
        st.subheader("Unit Settings")
        st.write("Standard units configured:")
        st.code("""
Stress (Tensile/Flexural Strength, Moduli): MPa
Density: tonnes/mm³
Elongation: strain (dimensionless)
Length: mm
Time: seconds
Force: Newton
Mass: tonnes
        """)
    
    # ------------------------------------------------------------------
    # Step 1: Material name + PDF upload, together in one step.
    # ------------------------------------------------------------------
    st.header("🔄 Step 1: Material & Upload PDFs")
    
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        material_name = st.text_input(
            "Material name",
            value=st.session_state.material_name,
            placeholder="e.g. ABS, PP, PC, PET...",
            help="Name of the plastic material for this batch of files"
        )
        st.session_state.material_name = material_name
    with col2:
        uploaded_files = st.file_uploader(
            "Select PDF datasheets",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more datasheets for this material"
        )
    
    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} file(s) selected")
        with st.expander("📋 View selected files"):
            for file in uploaded_files:
                st.write(f"📄 {file.name} ({format_bytes(file.size)})")
    
    # ------------------------------------------------------------------
    # Step 2: Create a new workbook, or merge into an existing one.
    # ------------------------------------------------------------------
    st.header("💾 Step 2: Create New or Merge Into Existing Excel")
    
    output_mode = st.radio(
        "Excel output mode",
        options=["Create new Excel file", "Merge into existing Excel file"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    existing_workbook_file = None
    if output_mode == "Merge into existing Excel file":
        existing_workbook_file = st.file_uploader(
            "Upload the existing Excel workbook to merge into",
            type=['xlsx'],
            key="existing_workbook_uploader",
            help="Sheets already in this workbook are preserved. If this "
                 "material already has a sheet, new companies are appended "
                 "below the existing rows; otherwise a new sheet is added."
        )
    
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        output_filename = st.text_input(
            "Output filename",
            value="material_extraction.xlsx",
            help="Name of the generated Excel file"
        )
    
    with col2:
        output_dir = st.text_input(
            "Output directory",
            # CHIMIAN_OUTPUT_DIR lets a Docker deployment point this at a
            # mounted volume (e.g. /data) by default; falls back to the
            # user's Downloads folder for local/desktop use.
            value=os.environ.get('CHIMIAN_OUTPUT_DIR', str(Path.home() / "Downloads")),
            help="Where to save the Excel file"
        )
    
    if output_filename and output_dir:
        output_path = str(Path(output_dir) / output_filename)
        st.session_state.output_path = output_path
        
        # Check if path is valid
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            st.caption(f"📁 Output: {output_path}")
        except Exception as e:
            st.error(f"Invalid output directory: {str(e)}")
            st.session_state.output_path = None
    
    # ------------------------------------------------------------------
    # Step 3: Extract & generate
    # ------------------------------------------------------------------
    st.header("⚡ Step 3: Generate")
    
    col1, col2 = st.columns(2)
    
    with col1:
        extract_button = st.button(
            "🚀 Extract & Generate Excel",
            use_container_width=True,
            type="primary",
            disabled=not (uploaded_files and material_name and st.session_state.output_path)
        )
    
    with col2:
        reset_button = st.button(
            "🔄 Reset All",
            use_container_width=True
        )
    
    if reset_button:
        st.session_state.material_name = "ABS"
        st.session_state.output_path = None
        st.session_state.extraction_results = {}
        st.session_state.excel_generated = False
        st.session_state.last_excel_path = None
        st.rerun()
    
    if extract_button and uploaded_files and material_name and st.session_state.output_path:
        st.header("📈 Processing")
        
        # Extract metrics
        with st.spinner(f"🔍 Extracting metrics for {material_name}..."):
            results = extract_pdfs(uploaded_files, material_name)
            st.session_state.extraction_results = results
        
        if results:
            existing_bytes = existing_workbook_file.getvalue() if existing_workbook_file is not None else None
            
            # Generate Excel
            with st.spinner("📊 Generating Excel report..."):
                success, error = generate_combined_excel_report(
                    {material_name: results},
                    st.session_state.output_path,
                    existing_bytes
                )
            
            if success:
                st.session_state.excel_generated = True
                st.session_state.last_excel_path = st.session_state.output_path
                
                # Success message
                st.markdown("""
                <div class="success-box">
                <h3>✅ Success!</h3>
                <p>Excel file has been generated successfully.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # File info and copy button
                col1, col2, col3 = st.columns([0.4, 0.3, 0.3])
                
                with col1:
                    file_size = Path(st.session_state.output_path).stat().st_size
                    st.info(f"📊 File size: {format_bytes(file_size)}")
                
                with col2:
                    if st.button("📋 Copy Path", use_container_width=True):
                        if copy_to_clipboard(st.session_state.output_path):
                            st.success("✓ Path copied to clipboard!")
                        else:
                            st.error("✗ Failed to copy path")
                
                with col3:
                    if st.button("📂 Open Folder", use_container_width=True):
                        if hasattr(os, 'startfile'):
                            os.startfile(str(Path(st.session_state.output_path).parent))
                        else:
                            # os.startfile is Windows-only (e.g. not available
                            # when running in a Linux Docker container) - the
                            # download button above is the reliable way to
                            # retrieve the file in that case.
                            st.info("Opening a folder isn't supported on this "
                                    "server - use the Download button instead.")
                
                # Show path
                st.code(st.session_state.output_path, language="text")
                
                # Download button
                with open(st.session_state.output_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Excel File",
                        data=f.read(),
                        file_name=Path(st.session_state.output_path).name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                # Extraction summary
                st.subheader("📋 Extraction Summary")
                
                total_companies = len(results)
                total_metrics = sum(
                    sum(len(r['metrics']) for r in results_list)
                    for results_list in results.values()
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Companies Processed", total_companies)
                with col2:
                    st.metric("Metrics Extracted", total_metrics)
                
                # Detailed results
                with st.expander("View detailed extraction results"):
                    for filename, results_list in results.items():
                        st.write(f"**{filename}**")
                        for result_item in results_list:
                            metrics = result_item['metrics']
                            for metric_key, entries in metrics.items():
                                for entry in entries:
                                    condition_suffix = (
                                        f" [{entry.get('test_condition')}]"
                                        if entry.get('test_condition') else ""
                                    )
                                    st.write(
                                        f"  - {get_metric_name(metric_key)}: "
                                        f"{entry.get('value')} {entry.get('unit')}{condition_suffix}"
                                    )
            
            else:
                st.markdown(f"""
                <div class="error-box">
                <h3>❌ Error!</h3>
                <p>{error}</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.warning("⚠️ No metrics could be extracted from any files")
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("📚 **Documentation**")
        st.markdown("- [README](./README.md)")
        st.markdown("- [Quick Start](./QUICKSTART.md)")
    
    with col2:
        st.write("🔧 **Support**")
        st.markdown("- Run tests: `python test_extraction.py`")
        st.markdown("- View logs in terminal")
    
    with col3:
        st.write("⚙️ **Settings**")
        st.markdown("- Edit `config.py` for customization")
        st.markdown("- Update `unit_converter.py` for units")


if __name__ == "__main__":
    main()
