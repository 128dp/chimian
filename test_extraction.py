"""
Test script to validate extraction on sample PDFs
Place your PDF files in a 'test_files' directory and run this script
"""

import sys
from pathlib import Path
from advanced_extractor import AdvancedPDFExtractor, MetricWithConversion
from unit_converter import UnitConverter
import json


def test_extraction(pdf_path):
    """Test extraction on a single PDF"""
    print(f"\n{'='*70}")
    print(f"Testing: {Path(pdf_path).name}")
    print('='*70)
    
    try:
        extractor = AdvancedPDFExtractor(pdf_path)
        result = extractor.extract_all()
        
        metrics = result.get('metrics', {})
        
        if not metrics:
            print("⚠ No metrics extracted from this PDF")
            return None
        
        print(f"\n✓ Successfully extracted {len(metrics)} metric(s)\n")
        
        converter = UnitConverter()
        
        # Display results
        for metric_name, (original_value, original_unit) in metrics.items():
            print(f"{metric_name.upper().replace('_', ' ')}")
            print(f"  Original:     {original_value} {original_unit}")
            
            # Convert to standard
            metric = MetricWithConversion(metric_name, original_value, original_unit, converter)
            print(f"  Standardized: {metric.standard_value} {metric.standard_unit}")
            print()
        
        return result
    
    except Exception as e:
        print(f"✗ Error during extraction: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main test function"""
    print("\n" + "="*70)
    print("PLASTIC MATERIAL METRICS EXTRACTOR - TEST SUITE")
    print("="*70)
    
    # Look for test files
    test_dir = Path(__file__).parent / "test_files"
    
    if not test_dir.exists():
        print(f"\n⚠ Test directory not found: {test_dir}")
        print("\nTo run tests:")
        print("1. Create a 'test_files' folder in this directory")
        print("2. Add PDF datasheets to test")
        print("3. Run this script again")
        print("\nExample:")
        print("  c:\\chimian\\test_files\\material1.pdf")
        print("  c:\\chimian\\test_files\\material2.pdf")
        return
    
    pdf_files = list(test_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n⚠ No PDF files found in {test_dir}")
        print("Please add PDF datasheets to the test_files folder")
        return
    
    print(f"\n📁 Found {len(pdf_files)} PDF file(s) to test\n")
    
    # Test each file
    results = []
    successful = 0
    
    for pdf_path in pdf_files:
        result = test_extraction(str(pdf_path))
        if result:
            results.append(result)
            successful += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"\nTotal files tested: {len(pdf_files)}")
    print(f"Successful extractions: {successful}")
    print(f"Failed: {len(pdf_files) - successful}")
    
    if results:
        total_metrics = sum(len(r.get('metrics', {})) for r in results)
        print(f"Total metrics extracted: {total_metrics}")
    
    print("\n" + "="*70)
    print("NOTES")
    print("="*70)
    print("""
If extraction is not working as expected:

1. Check PDF Quality
   - Ensure text is selectable (not an image)
   - Try opening in a PDF reader to verify

2. Verify Metric Names
   - The tool looks for specific keywords
   - Check if metric names match our patterns
   - Supported: Tensile Strength, Flexural Strength, Density, etc.

3. Unit Verification
   - Ensure units are clearly separated from values
   - Supported units are listed in unit_converter.py

4. Table Structure
   - PDFs with clear tables work best
   - Unstructured text may not extract properly

5. Debug Output
   - Check the Python console for error messages
   - Run demo.py to see how extraction works
    """)


if __name__ == "__main__":
    main()
