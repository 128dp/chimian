"""Quick test of value extraction fix"""
from enhanced_extractor import EnhancedPDFExtractor

extractor = EnhancedPDFExtractor("dummy.pdf")

test_values = [
    ("19,000~22,000", 19000.0, "Should extract 19000 from comma-separated range"),
    ("2,300 MPa", 2300.0, "Should extract 2300 from comma-separated with unit"),
    ("370-400", 370.0, "Should extract 370 from hyphen range"),
    ("620~720", 620.0, "Should extract 620 from tilde range"),
    ("1,042", 1042.0, "Should extract 1042 from single comma-separated number"),
]

print("VALUE EXTRACTION TESTS (AFTER FIX)\n" + "="*60)

all_pass = True
for test_str, expected_val, description in test_values:
    value, unit = extractor._extract_value_unit(test_str)
    status = "✓ PASS" if value == expected_val else "✗ FAIL"
    if value != expected_val:
        all_pass = False
    print(f"{status}: '{test_str}'")
    print(f"       Expected {expected_val}, got {value}")
    print(f"       {description}\n")

print("="*60)
print(f"Overall: {'ALL TESTS PASSED ✓' if all_pass else 'SOME TESTS FAILED ✗'}")
