## 🔧 EXTRACTION & FORMATTING FIXES - NOW LOCKED IN

### What Was Broken
1. **Naive left-to-right scanning** - grabbed first number in row (often test temperature like "23°C") instead of actual metric values
2. **Generic keyword matching** - single-word keywords like "flexural" caused misclassification across metrics
3. **Metric-only metrics with no test method** - couldn't detect ASTM standards, test conditions, units from structured tables
4. **Varying column layouts** - different manufacturers have Property/Unit/TestMethod/Value in different orders

### What's Fixed
✅ **Column-Role Detection Engine**
- Scans table headers to map column index → role (property, unit, test_method, typical_value, etc.)
- Caches column roles across split tables (pdfplumber breaks some tables on section dividers)
- Uses detected roles instead of naive left-to-right scanning
- Falls back cleanly when no header detected

✅ **Keyword Matching Rewrite**
- Single flattened (keyword, metric, is_chinese) index sorted by keyword LENGTH descending
- Longest/most-specific keyword ALWAYS wins, regardless of metric order
- Removed generic single-word keywords like "flexural" and "modulus" that cross-contaminate metrics
- Proper Chinese variant support

✅ **Test Method Extraction**
- Regex pattern matches ASTM D-xxx, ISO xxx, UL xx formats (with or without spaces/hyphens)
- Looks in dedicated test_method columns when detected, falls back to full-text search
- Cleanly separated from value extraction

✅ **Excel Output Format (FINAL)**
```
COMPANY A
┌──────────────────┬──────────┬──────────────┬──────────────┐
│ PROPERTY         │ UNIT     │ TEST METHOD  │ VALUE        │
├──────────────────┼──────────┼──────────────┼──────────────┤
│ Tensile Strength │ MPa      │ ASTM D638    │ 40           │
│ Flexural Strength│ MPa      │ ASTM D790    │ 65           │
│ Density          │ g/cm3    │ ASTM D792    │ 1.06         │
│ Tensile Modulus  │ -        │ -            │ -            │
│ Flexural Modulus │ MPa      │ ASTM D790    │ 2300         │
│ Elongation       │ %        │ ASTM D638    │ 15           │
└──────────────────┴──────────┴──────────────┴──────────────┘

COMPANY B
...
```

### Tested on Real PDFs
✅ Kingfa GAR-011(H85)TDS - 5 metrics extracted correctly
✅ Lavergne VYTEEN ABS - 4 metrics extracted correctly  
✅ Eastern Ever AR130(85) - 4 metrics extracted correctly
✅ Formosa AF358R - 5 metrics extracted correctly

All values now match source PDFs exactly, with proper units and ASTM standards captured.

### What You See in Streamlit UI Now
1. Select material type (ABS, PP, PE, etc.)
2. Upload PDF files
3. Click "Extract & Generate Excel"
4. Download Excel with clean, accurate data in PROPERTY | UNIT | TEST METHOD | VALUE layout

**App is live at: http://localhost:8501**
