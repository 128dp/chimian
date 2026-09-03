"""
Test extraction logic with simulated PDF content from real datasheets
"""
from enhanced_extractor import EnhancedPDFExtractor
from config import METRIC_KEYWORDS
import re

# Simulated text extracted from Formosa PDF (what pdfplumber should return)
formosa_text = """
FORMOSA ABS( 85%PCR) TAIRILAC AF358R TDS
項 目
抗 張 強 度
Tensile Strength
彎曲強度
Flexural Strength
彎曲強度
Flexural Strength
彎曲模數
Flexural Modulus
彎曲模數
Flexural Modulus
耐 衝 擊 強 度
Izod Impact Strength
熱 變 形 溫 度
Heat Deflection Temperature
延伸率
Elongation
比 重
Specific Gravity

單 位
kg/cm²
kg/cm²
kg/cm2
kg/cm²
kg/cm²
kg-cm/cm
℃
℃
%
g/cm³

試驗方法
ASTM D-638
ASTM D-790
ASTM D-790
ASTM D-790
ASTM D-790
ASTM D-256
ASTM D-648
ASTM D-648
ASTM D-638
ASTM D-792

試 驗 條 件
50mm/min 3.2mm thickness
15mm/min 3.2mm thickness Span 50mm
15mm/min 3.2mm thickness Span 50mm
15mm/min 3.2mm thickness Span 50mm
1.3mm/min Span 50mm
1/8"Thickness
Unannealed 1/4"Thickness Load 18.6 kg/cm2
Annealed 3.2mm thickness Load 18.6 kg/cm2
50mm/min 1/8" (3.2mm) thickness
23℃/23℃

TOLERANCE
370 - 400
620~720
560~660
19,000~22,000
19,000~23,000
14~24
80 - 90
85~95
---
1.04 - 1.05

TYPICAL VALUES
380
670
610
20,500
21,000
18
84
90
15
1.042
"""

# Simulated Kingfa text (English, MPa)
kingfa_text = """
Properties Test Standard Test Condition S.I. Unit Control Value S.I. Typical Value
Mechanical
Tensile Strength ASTM D638 50mm/min,3.2mm MPa 38-48 40
Percent Elongation at Break ASTM D638 50mm/min,3.2mm % 10-30 15
Flexural Strength ASTM D790 3.2mm, 1.32mm/min span 50mm MPa 60-75 65
Flexural Modulus ASTM D790 MPa 2000-2800 2300
Izod Notched Impact Strength ASTM D256 23℃, 3.2mm J/m 140-250 180
Density ASTM D792 23℃ g/cm3 1.04-1.08 1.06
"""

# Simulated Lavergne text (English, MPa)
lavergne_text = """
PROPERTIES
Density, 23°C ASTM D792 g/cm3 1.04 – 1.08
Melt Flow Rate 230°C /3.8 Kg ASTM D1238 g/10 min 7 – 9
Izod-Notched, 23°C ASTM D256 J/m 120 – 150
Tensile Strength @ Yield, 50 mm/min ASTM D638 MPa 32 – 37
Flexural Strength, 1.3 mm/min ASTM D790 MPa 60 – 70
Flexural Modulus, 1.3 mm/min ASTM D790 MPa 2,002 – 2,448
Heat Deflection Temperature, 0.45 MPa ASTM D648 °C 81 – 99
"""

print("=" * 80)
print("TESTING KEYWORD MATCHING")
print("=" * 80)

# Test if keywords match
test_cases = [
    ("抗張強度", "Tensile Strength (Chinese variant)"),
    ("拉伸強度", "Tensile Strength (original Chinese)"),
    ("彎曲強度", "Flexural Strength (Chinese)"),
    ("彎曲模數", "Flexural Modulus (Chinese)"),
    ("彎曲彈数", "Flexural Modulus (alternative Chinese)"),
    ("Tensile Strength", "Tensile Strength (English)"),
    ("Flexural Strength", "Flexural Strength (English)"),
    ("Flexural Modulus", "Flexural Modulus (English)"),
    ("Density", "Density (English)"),
    ("Elongation", "Elongation (English)"),
]

for text, description in test_cases:
    print(f"\nTesting: '{text}' ({description})")
    
    for metric, keywords in METRIC_KEYWORDS.items():
        for lang in ['en', 'zh']:
            for kw in keywords.get(lang, []):
                if kw.lower() in text.lower() or text.lower() in kw.lower():
                    print(f"  ✓ MATCH: {metric} (keyword: '{kw}')")
                    break

print("\n" + "=" * 80)
print("TESTING VALUE EXTRACTION")
print("=" * 80)

# Test value extraction patterns
extractor = EnhancedPDFExtractor("dummy.pdf")

test_values = [
    "370 kg/cm²",
    "380",
    "620~720",
    "19,000~22,000",
    "670",
    "15",
    "1.04 - 1.05",
    "1.042",
    "40 MPa",
    "65 MPa",
    "2,300 MPa",
]

print("\nValue extraction tests:")
for test_val in test_values:
    value, unit = extractor._extract_value_unit(test_val)
    print(f"  '{test_val}' → value={value}, unit='{unit}'")

print("\n" + "=" * 80)
print("TESTING METRIC IDENTIFICATION FROM TEXT LINES")
print("=" * 80)

# Test on actual lines from PDFs
test_lines = [
    "抗 張 強 度 Tensile Strength kg/cm² ASTM D-638 50mm/min 3.2mm thickness 370 - 400 380",
    "Tensile Strength ASTM D638 50mm/min,3.2mm MPa 38-48 40",
    "彎曲模數 Flexural Modulus kg/cm² ASTM D-790 15mm/min 3.2mm thickness Span 50mm 19,000~22,000 20,500",
    "Flexural Strength, 1.3 mm/min ASTM D790 MPa 60 – 70",
]

print("\nLine identification tests:")
for line in test_lines:
    metric_type = extractor._identify_metric(line)
    print(f"  '{line[:50]}...' → metric={metric_type}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
