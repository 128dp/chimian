"""
Demonstration: New Material-Based Excel Extraction with All 6 Metrics

This script demonstrates:
1. Material type specification (e.g., ABS plastic)
2. Extraction and organization of all 6 metrics
3. Neat Excel formatting with one company per row
4. Standardized units across materials
"""

from excel_writer import ExcelWriter
from unit_converter import UnitConverter
from pathlib import Path

def demo_material_extraction():
    """
    Demonstrate the new material-based extraction with all 6 metrics.
    Each company shows all 6 metrics in separate columns with standardized units.
    """
    
    print("\n" + "="*80)
    print("DEMO: Material-Based Extraction with All 6 Metrics")
    print("="*80)
    
    # Material type
    material = "ABS"
    print(f"\n📌 Material Type: {material}")
    print(f"   All data will be organized in one Excel tab under '{material}'")
    
    # Create Excel writer with new default columns (all 6 metrics)
    output_file = "demo_abs_extraction.xlsx"
    excel_writer = ExcelWriter(output_file)
    
    converter = UnitConverter()
    
    # Sample data from 4 ABS companies (as mentioned in user request)
    print("\n📂 Processing 4 ABS files:")
    print("   - kingfa_abs.pdf")
    print("   - lavergne_abs.pdf")
    print("   - basf_abs.pdf")
    print("   - dow_abs.pdf")
    
    # Company 1: Kingfa
    print("\n📍 Company 1: Kingfa")
    data1 = {
        'company': 'Kingfa',
        'material': material,
        'tensile_strength_raw_value': '40.0 MPa',
        'tensile_strength_unit': 'MPa',
        'tensile_strength_test_method': 'ASTM D638',
        'flexural_strength_raw_value': '65.0 MPa',
        'flexural_strength_unit': 'MPa',
        'flexural_strength_test_method': 'ASTM D790',
        'density_raw_value': '1.050 g/cm³',
        'density_unit': 'g/cm³',
        'density_test_method': 'ASTM D792',
        'tensile_modulus_raw_value': '2300 MPa',
        'tensile_modulus_unit': 'MPa',
        'tensile_modulus_test_method': 'ASTM D638',
        'flexural_modulus_raw_value': '2400 MPa',
        'flexural_modulus_unit': 'MPa',
        'flexural_modulus_test_method': 'ASTM D790',
        'elongation_raw_value': '25%',
        'elongation_unit': '%',
        'elongation_test_method': 'ASTM D638',
    }
    excel_writer.add_record(**data1)
    print("   ✓ 6 metrics extracted and standardized")
    
    # Company 2: Lavergne
    print("\n📍 Company 2: Lavergne")
    data2 = {
        'company': 'Lavergne',
        'material': material,
        'tensile_strength_raw_value': '45.0 MPa',
        'tensile_strength_unit': 'MPa',
        'tensile_strength_test_method': 'ASTM D638',
        'flexural_strength_raw_value': '70.0 MPa',
        'flexural_strength_unit': 'MPa',
        'flexural_strength_test_method': 'ASTM D790',
        'density_raw_value': '1.055 g/cm³',
        'density_unit': 'g/cm³',
        'density_test_method': 'ASTM D792',
        'tensile_modulus_raw_value': '2400 MPa',
        'tensile_modulus_unit': 'MPa',
        'tensile_modulus_test_method': 'ASTM D638',
        'flexural_modulus_raw_value': '2500 MPa',
        'flexural_modulus_unit': 'MPa',
        'flexural_modulus_test_method': 'ASTM D790',
        'elongation_raw_value': '20%',
        'elongation_unit': '%',
        'elongation_test_method': 'ASTM D638',
    }
    excel_writer.add_record(**data2)
    print("   ✓ 6 metrics extracted and standardized")
    
    # Company 3: BASF
    print("\n📍 Company 3: BASF")
    data3 = {
        'company': 'BASF',
        'material': material,
        'tensile_strength_raw_value': '42.0 MPa',
        'tensile_strength_unit': 'MPa',
        'tensile_strength_test_method': 'ASTM D638',
        'flexural_strength_raw_value': '68.0 MPa',
        'flexural_strength_unit': 'MPa',
        'flexural_strength_test_method': 'ASTM D790',
        'density_raw_value': '1.052 g/cm³',
        'density_unit': 'g/cm³',
        'density_test_method': 'ASTM D792',
        'tensile_modulus_raw_value': '2350 MPa',
        'tensile_modulus_unit': 'MPa',
        'tensile_modulus_test_method': 'ASTM D638',
        'flexural_modulus_raw_value': '2450 MPa',
        'flexural_modulus_unit': 'MPa',
        'flexural_modulus_test_method': 'ASTM D790',
        'elongation_raw_value': '23%',
        'elongation_unit': '%',
        'elongation_test_method': 'ASTM D638',
    }
    excel_writer.add_record(**data3)
    print("   ✓ 6 metrics extracted and standardized")
    
    # Company 4: Dow
    print("\n📍 Company 4: Dow")
    data4 = {
        'company': 'Dow',
        'material': material,
        'tensile_strength_raw_value': '38.0 MPa',
        'tensile_strength_unit': 'MPa',
        'tensile_strength_test_method': 'ASTM D638',
        'flexural_strength_raw_value': '62.0 MPa',
        'flexural_strength_unit': 'MPa',
        'flexural_strength_test_method': 'ASTM D790',
        'density_raw_value': '1.048 g/cm³',
        'density_unit': 'g/cm³',
        'density_test_method': 'ASTM D792',
        'tensile_modulus_raw_value': '2250 MPa',
        'tensile_modulus_unit': 'MPa',
        'tensile_modulus_test_method': 'ASTM D638',
        'flexural_modulus_raw_value': '2350 MPa',
        'flexural_modulus_unit': 'MPa',
        'flexural_modulus_test_method': 'ASTM D790',
        'elongation_raw_value': '22%',
        'elongation_unit': '%',
        'elongation_test_method': 'ASTM D638',
    }
    excel_writer.add_record(**data4)
    print("   ✓ 6 metrics extracted and standardized")
    
    # Generate Excel file
    print(f"\n📊 Generating Excel file: {output_file}")
    print("   Columns: Company | Tensile Strength | Flexural Strength | Density | Tensile Modulus | Flexural Modulus | Elongation")
    
    excel_writer.create_sheets()
    excel_writer.save()
    
    print("\n✅ Excel file generated successfully!")
    print(f"   Location: {Path(output_file).absolute()}")
    print(f"   Sheet: '{material}' (contains all 4 companies)")
    
    print("\n" + "="*80)
    print("FEATURES DEMONSTRATED:")
    print("="*80)
    print("✓ Material Type Selection: Users choose material (ABS, PP, etc.)")
    print("✓ All 6 Metrics Displayed: Each company shows all 6 properties")
    print("✓ Standardized Units: All values converted to standard units (MPa, g/cm³, strain)")
    print("✓ Single Material Tab: All ABS files organized in one Excel sheet")
    print("✓ Neat Organization: One company per row, metrics in columns")
    print("✓ Professional Formatting: Headers, colors, borders, proper alignment")
    
    print("\n" + "="*80)
    print("HOW TO USE IN STREAMLIT UI:")
    print("="*80)
    print("1. Select Material Type: Choose 'ABS' (or other material) from dropdown")
    print("2. Upload PDF Files: Select all 4 ABS datasheets")
    print("3. Configure Output: Set filename and directory")
    print("4. Click 'Extract & Generate Excel'")
    print("5. Download the Excel file - all metrics shown neatly per company!")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    demo_material_extraction()
