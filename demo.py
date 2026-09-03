"""
Demo script for testing the Plastic Material Metrics Extractor
Useful for understanding how the extraction works
"""

import os
import sys
from pathlib import Path
from advanced_extractor import AdvancedPDFExtractor, MetricWithConversion
from excel_writer import DataOrganizer
from unit_converter import UnitConverter


def demo_unit_conversion():
    """Demonstrate unit conversion capabilities"""
    print("=" * 60)
    print("UNIT CONVERSION DEMONSTRATIONS")
    print("=" * 60)
    
    converter = UnitConverter()
    
    print("\n1. STRESS/STRENGTH CONVERSIONS (to MPa)")
    print("-" * 60)
    
    test_cases = [
        (380, "kg/cm2"),
        (55000, "psi"),
        (550, "N/mm2"),
        (75, "kPa"),
    ]
    
    for value, unit in test_cases:
        converted, new_unit = converter.convert_stress(value, unit)
        print(f"  {value} {unit:15} → {converted:10.4f} {new_unit}")
    
    print("\n2. DENSITY CONVERSIONS (to g/cm³)")
    print("-" * 60)
    
    test_cases = [
        (1.035, "g/cm³"),
        (1050, "kg/m³"),
        (1.06, ""),  # Specific gravity (unitless)
    ]
    
    for value, unit in test_cases:
        converted, new_unit = converter.convert_density(value, unit)
        print(f"  {value} {unit:15} → {converted:10.4f} {new_unit}")
    
    print("\n3. ELONGATION CONVERSIONS (to strain)")
    print("-" * 60)
    
    test_cases = [
        (15, "%"),
        (0.15, ""),
        (1.5, "%"),
    ]
    
    for value, unit in test_cases:
        converted, new_unit = converter.convert_elongation(value, unit)
        print(f"  {value} {unit:15} → {converted:10.4f} {new_unit}")
    
    print("\n4. LENGTH CONVERSIONS (to mm)")
    print("-" * 60)
    
    test_cases = [
        (0.5, "cm"),
        (25.4, "inch"),
        (0.125, "inch"),
        (1, "m"),
    ]
    
    for value, unit in test_cases:
        converted, new_unit = converter.convert_length(value, unit)
        print(f"  {value} {unit:15} → {converted:10.4f} {new_unit}")


def demo_pdf_extraction(pdf_path):
    """Demonstrate PDF extraction from a sample file"""
    print("\n" + "=" * 60)
    print(f"PDF EXTRACTION DEMO: {Path(pdf_path).name}")
    print("=" * 60)
    
    try:
        extractor = AdvancedPDFExtractor(pdf_path)
        result = extractor.extract_all()
        
        print(f"\nFile: {result['file']}")
        print(f"Metrics found: {len(result['metrics'])}")
        
        converter = UnitConverter()
        
        print("\n" + "-" * 60)
        print("EXTRACTED METRICS")
        print("-" * 60)
        
        if result['metrics']:
            for metric_name, (value, unit) in result['metrics'].items():
                # Create metric with conversion
                metric = MetricWithConversion(metric_name, value, unit, converter)
                
                print(f"\n{metric_name.upper().replace('_', ' ')}")
                print(f"  Original:     {value:12.4f} {unit}")
                print(f"  Standardized: {metric.standard_value:12.4f} {metric.standard_unit}")
        else:
            print("\n⚠ No metrics found in this PDF")
        
        return result
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


def demo_excel_generation(pdf_paths, output_path):
    """Demonstrate Excel file generation"""
    print("\n" + "=" * 60)
    print("EXCEL GENERATION DEMO")
    print("=" * 60)
    
    organizer = DataOrganizer()
    converter = UnitConverter()
    
    print(f"\nProcessing {len(pdf_paths)} PDF(s)...")
    
    processed_count = 0
    for pdf_path in pdf_paths:
        try:
            extractor = AdvancedPDFExtractor(pdf_path)
            result = extractor.extract_all()
            
            if result.get('metrics'):
                organizer.add_extraction_result(result)
                processed_count += 1
                print(f"  ✓ {Path(pdf_path).name}")
            else:
                print(f"  ✗ {Path(pdf_path).name} - No metrics found")
        
        except Exception as e:
            print(f"  ✗ {Path(pdf_path).name} - Error: {e}")
    
    if processed_count > 0:
        print(f"\nGenerating Excel file: {output_path}")
        organizer.generate_excel(output_path, converter)
        print("✓ Excel file generated successfully!")
    else:
        print("\n⚠ No files were successfully processed")


def main():
    """Main demo function"""
    print("\n" + "=" * 60)
    print("PLASTIC MATERIAL METRICS EXTRACTOR - DEMO")
    print("=" * 60)
    
    # Demo 1: Unit conversions
    demo_unit_conversion()
    
    # Demo 2: PDF extraction (if sample files exist)
    sample_dir = Path(__file__).parent / "samples"
    
    if sample_dir.exists():
        pdf_files = list(sample_dir.glob("*.pdf"))
        
        if pdf_files:
            print("\n" + "=" * 60)
            print("FOUND SAMPLE PDFs")
            print("=" * 60)
            
            for pdf_file in pdf_files:
                demo_pdf_extraction(str(pdf_file))
            
            # Generate Excel from all samples
            output_path = Path(__file__).parent / "demo_output.xlsx"
            demo_excel_generation([str(f) for f in pdf_files], str(output_path))
    
    else:
        print("\n" + "=" * 60)
        print("NO SAMPLE PDFs FOUND")
        print("=" * 60)
        print(f"\nTo test with PDFs, place them in: {sample_dir}")
        print("\nUsage:")
        print("1. Create a 'samples' folder in the project directory")
        print("2. Add plastic material datasheets (PDFs)")
        print("3. Run this script again")
    
    print("\n" + "=" * 60)
    print("For interactive extraction, run: python main.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
