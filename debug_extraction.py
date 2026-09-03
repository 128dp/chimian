"""
Debug script to test PDF extraction on real files
"""
import os
from pathlib import Path
from enhanced_extractor import EnhancedPDFExtractor

# Test PDFs
test_files = [
    "Lavergne VYTEEN ABS Dark Color.pdf",
    "Formosa 20221020-RCP_ABS AF358R_TDS-R4.pdf",
    "Eastern Ever - TDS - AR130(85) All Dark Colors - Rev. 2 (1).pdf",
    "Kingfa GAR-011(H85)TDS V6.7-ASTM-2023 for HP.pdf",
]

print("=" * 80)
print("PDF EXTRACTION DEBUG REPORT")
print("=" * 80)

for pdf_file in test_files:
    pdf_path = Path(pdf_file)
    
    if not pdf_path.exists():
        print(f"\n❌ File not found: {pdf_file}")
        continue
    
    print(f"\n{'=' * 80}")
    print(f"📄 File: {pdf_file}")
    print(f"{'=' * 80}")
    
    try:
        extractor = EnhancedPDFExtractor(str(pdf_path))
        extractor.debug = True  # Enable debug output
        
        # Extract
        result = extractor.extract_all()
        
        metrics_found = result.get('metrics', {})
        
        print(f"\n✓ Extraction completed")
        print(f"  Metrics found: {len(metrics_found)}")
        
        if metrics_found:
            print(f"\n  Metrics:")
            for metric_key, (value, unit) in metrics_found.items():
                print(f"    - {metric_key}: {value} {unit}")
        else:
            print(f"\n  ⚠️  NO METRICS FOUND!")
            
            # Debug info
            print(f"\n  Debug info - raw extracted data:")
            print(f"    {extractor.data}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

print(f"\n{'=' * 80}")
print("END OF REPORT")
print("=" * 80)
