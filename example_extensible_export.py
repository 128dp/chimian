"""
Example: Using the Extensible Excel Export System

This script demonstrates how to customize the Excel export with:
- Custom columns
- Custom data fields
- Custom formatters
- Different configurations
"""

from excel_writer import ExcelWriter
from enhanced_extractor import EnhancedPDFExtractor
from unit_converter import UnitConverter
from pathlib import Path


def example_1_basic_extraction():
    """Example 1: Basic extraction and export"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Extraction and Export")
    print("="*70)
    
    # Create Excel writer with default columns
    excel_writer = ExcelWriter("example_basic.xlsx")
    
    # Add a record
    excel_writer.add_record(
        company="Example Corp",
        material="ABS",
        metric_name="Tensile Strength",
        original_value=380,
        original_unit="kg/cm2",
        standard_value=37.3,
        standard_unit="MPa",
        test_method="ASTM D638"
    )
    
    # Create sheets and save
    excel_writer.create_sheets()
    excel_writer.save()
    
    print("✓ File saved: example_basic.xlsx")


def example_2_custom_columns():
    """Example 2: Using custom columns"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Custom Columns")
    print("="*70)
    
    # Define custom columns
    custom_columns = [
        {'name': 'Company', 'width': 20},
        {'name': 'Metric', 'width': 25},
        {'name': 'Value', 'width': 12, 'format': '0.0000'},
        {'name': 'Unit', 'width': 12},
        {'name': 'Specification', 'width': 30},  # New custom column
    ]
    
    # Create Excel writer with custom columns
    excel_writer = ExcelWriter("example_custom_columns.xlsx", columns=custom_columns)
    
    # Add records with custom fields
    excel_writer.add_record(
        company="Example Corp",
        material="ABS",
        metric_name="Tensile Strength",
        original_value=380,
        original_unit="MPa",
        standard_value=380,
        standard_unit="MPa",
        specification="ASTM D638, 50mm/min"  # Custom field
    )
    
    # Create sheets and save
    excel_writer.create_sheets()
    excel_writer.save()
    
    print("✓ File saved: example_custom_columns.xlsx")


def example_3_custom_formatters():
    """Example 3: Using custom formatters"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom Formatters")
    print("="*70)
    
    # Create Excel writer
    excel_writer = ExcelWriter("example_custom_formatters.xlsx")
    
    # Add custom formatters
    def format_unit_with_link(unit):
        """Custom formatter for units"""
        return f"{unit} (SI)"
    
    def format_value_percentage(value):
        """Format value as percentage"""
        return f"{value:.2%}" if isinstance(value, (int, float)) else value
    
    # Add formatters
    excel_writer.add_custom_formatter("Original Unit", format_unit_with_link)
    excel_writer.add_custom_formatter("Standardized Unit", format_unit_with_link)
    
    # Add records
    excel_writer.add_record(
        company="Example Corp",
        material="ABS",
        metric_name="Tensile Strength",
        original_value=380,
        original_unit="kg/cm²",
        standard_value=37.3,
        standard_unit="MPa"
    )
    
    # Create sheets and save
    excel_writer.create_sheets()
    excel_writer.save()
    
    print("✓ File saved: example_custom_formatters.xlsx")


def example_4_multiple_materials():
    """Example 4: Extracting multiple materials"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Multiple Materials")
    print("="*70)
    
    # Create Excel writer
    excel_writer = ExcelWriter("example_multiple_materials.xlsx")
    
    # ABS Data
    excel_writer.add_record(
        company="Kingfa",
        material="ABS",
        metric_name="Tensile Strength",
        original_value=40,
        original_unit="MPa",
        standard_value=40,
        standard_unit="MPa",
        test_method="ASTM D638"
    )
    
    excel_writer.add_record(
        company="Lavergne",
        material="ABS",
        metric_name="Tensile Strength",
        original_value=45,
        original_unit="MPa",
        standard_value=45,
        standard_unit="MPa",
        test_method="ASTM D638"
    )
    
    # PP Data
    excel_writer.add_record(
        company="Example Corp",
        material="PP",
        metric_name="Tensile Strength",
        original_value=32,
        original_unit="MPa",
        standard_value=32,
        standard_unit="MPa",
        test_method="ASTM D638"
    )
    
    # Create sheets and save
    excel_writer.create_sheets()
    excel_writer.save()
    
    print("✓ File saved: example_multiple_materials.xlsx")
    print("  (Separate tabs for ABS and PP)")


def example_5_extended_data():
    """Example 5: Extended data with additional columns"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Extended Data Fields")
    print("="*70)
    
    # Define extended columns
    extended_columns = [
        {'name': 'Supplier', 'width': 20},
        {'name': 'Property', 'width': 25},
        {'name': 'Original', 'width': 12, 'format': '0.0000'},
        {'name': 'Orig. Unit', 'width': 12},
        {'name': 'Standard', 'width': 12, 'format': '0.0000'},
        {'name': 'Std. Unit', 'width': 12},
        {'name': 'Test Condition', 'width': 20},
        {'name': 'Notes', 'width': 30},
    ]
    
    # Create Excel writer with extended columns
    excel_writer = ExcelWriter(
        "example_extended_data.xlsx",
        columns=extended_columns,
        include_test_method=False  # We're using Test Condition instead
    )
    
    # Rename some columns in our usage
    # (Actually we need to use the correct mapping - let me adjust)
    
    # Add records with extended fields
    excel_writer.add_record(
        company="Example Corp",
        material="ABS",
        metric_name="Tensile Strength",
        original_value=380,
        original_unit="kg/cm²",
        standard_value=37.3,
        standard_unit="MPa",
        test_condition="23°C, 50mm/min",  # Custom field
        notes="From technical datasheet v2.0"  # Custom field
    )
    
    # Create sheets and save
    excel_writer.create_sheets()
    excel_writer.save()
    
    print("✓ File saved: example_extended_data.xlsx")


def example_6_minimal_columns():
    """Example 6: Minimal column set"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Minimal Columns")
    print("="*70)
    
    # Define minimal columns
    minimal_columns = [
        {'name': 'Company', 'width': 15},
        {'name': 'Metric', 'width': 20},
        {'name': 'Value', 'width': 12, 'format': '0.0000'},
        {'name': 'Unit', 'width': 12},
    ]
    
    # Create Excel writer with minimal columns
    excel_writer = ExcelWriter(
        "example_minimal.xlsx",
        columns=minimal_columns
    )
    
    # Add record (note: we need to map the fields)
    excel_writer.add_record(
        company="Example Corp",
        material="ABS",
        metric_name="Tensile Strength",
        original_value=38.0,
        original_unit="MPa",
        standard_value=38.0,
        standard_unit="MPa"
    )
    
    # Create sheets and save
    excel_writer.create_sheets()
    excel_writer.save()
    
    print("✓ File saved: example_minimal.xlsx")


def main():
    """Run all examples"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "EXTENSIBLE EXCEL EXPORT EXAMPLES" + " "*21 + "║")
    print("╚" + "="*68 + "╝")
    
    examples = [
        ("Basic Extraction", example_1_basic_extraction),
        ("Custom Columns", example_2_custom_columns),
        ("Custom Formatters", example_3_custom_formatters),
        ("Multiple Materials", example_4_multiple_materials),
        ("Extended Data", example_5_extended_data),
        ("Minimal Columns", example_6_minimal_columns),
    ]
    
    for idx, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"✗ Error in example {idx} ({name}): {str(e)}")
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED")
    print("="*70)
    print("\nGenerated files:")
    for file in Path(".").glob("example_*.xlsx"):
        print(f"  - {file.name}")
    
    print("\n" + "="*70)
    print("CUSTOMIZATION GUIDE")
    print("="*70)
    print("""
1. CUSTOM COLUMNS:
   - Define column configuration with 'name', 'width', 'format'
   - Pass to ExcelWriter(columns=custom_columns)

2. CUSTOM DATA:
   - Add any field with add_record(**kwargs)
   - Use mapped field names in records

3. CUSTOM FORMATTERS:
   - Define formatter functions
   - Register with add_custom_formatter()

4. DYNAMIC CONFIGURATION:
   - Use remove_column() to remove defaults
   - Use add_custom_column() to add new columns
   - Use set_custom_columns() for complete replacement

5. MATERIAL ORGANIZATION:
   - Automatically creates separate sheets per material
   - Groups records by material type

6. STYLING:
   - Headers: Colored fill, bold text, centered
   - Data: Bordered cells, alternating formats
   - Numbers: Custom format strings (e.g., '0.0000')
""")


if __name__ == "__main__":
    main()
