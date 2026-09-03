# PDF Extraction Issues & Fixes

## Problem Summary

When users uploaded real PDFs from manufacturers like Lavergne, Formosa, Eastern Ever, and Kingfa, the system was finding **only 1 metric per PDF** (or none at all) instead of all 6 metrics:
- ✗ Lavergne: 1 metric found
- ✗ Formosa: 1 metric found  
- ✗ Eastern Ever: 0 metrics found
- ✗ Kingfa: 0 metrics found

Yet the PDFs clearly contained complete data tables with all properties (see Formosa example).

**Root Causes Identified:**

### 1. **Keyword Mismatch (Primary Issue)**
The PDFs use **different Chinese terminology** than configured in `config.py`:

**PDF Keywords vs Config Keywords:**
```
PDF Uses:                    Config Had:
抗張強度 (Tensile)      →    拉伸強度/拉伸强度
彎曲強度 (Flexural)     →    ✓ Match (config correct)
彎曲彈数 (Flex Mod)     →    彎曲模數/弯曲模数
撓曲強度 (Flexural alt) →    Not present
```

When `_identify_metric()` looks for keywords in the PDF and doesn't find a match, it returns `None`, so the metric is skipped.

### 2. **Overly Aggressive Value Validation**
The `_validate_metrics()` method in `enhanced_extractor.py` was checking raw PDF values against VALUE_RANGES **before unit conversion**:

**Example:**
- PDF has: `370 kg/cm²` (Tensile Strength)
- Extractor extracts raw: `(370, 'kg/cm²')`
- VALUE_RANGES check: `if 1 <= 370 <= 200: FAIL!` ✗
- Value rejected because 370 > 200 MPa limit

This happened because:
- PDF values in `kg/cm²` or other units are larger numbers
- VALUE_RANGES assume conversion to standard units (MPa, tonnes/mm³)
- Validation happened BEFORE conversion
- Raw values don't match standard-unit ranges

### 3. **Unit Format Variations**
PDFs from different manufacturers use different unit notations:
- `kg/cm2` vs `kg/cm²` (superscript ² symbol)
- `kg/cm³` vs other formats
- Some systems don't preserve superscripts during PDF extraction

## Fixes Implemented

### Fix #1: Expanded Keyword List (config.py)

Added **Chinese keyword variants** to match manufacturer PDFs:

```python
'tensile_strength': {
    'zh': [
        '拉伸強度',      # Original
        '拉伸强度',      # Simplified
        '抗張強度',      # Taiwan/Formosa variant ← NEW
        '抗张强度',      # Simplified variant ← NEW
        '拉伸',
    ]
},

'flexural_modulus': {
    'zh': [
        '彎曲模數',
        '弯曲模数',
        '彎曲彈数',      # Alternative name ← NEW
        '弯曲弹数',      # Simplified ← NEW
        '彎曲',
        '弯曲',
    ]
},

'flexural_strength': {
    'zh': [
        '彎曲強度',
        '弯曲强度',
        '撓曲強度',      # Alternative term ← NEW
        '挠曲强度',      # Simplified ← NEW
        '彎曲',
        '弯曲',
    ]
}
```

**Impact:** Extraction now recognizes terms used by Formosa, Lavergne, Eastern Ever, and other manufacturers.

### Fix #2: Removed Raw Value Validation (enhanced_extractor.py)

Changed `_validate_metrics()` to **only check reasonable number ranges**, not standard-unit VALUE_RANGES:

**Before:**
```python
# Validated raw values against standard-unit ranges (WRONG!)
if VALUE_RANGES and metric_key in VALUE_RANGES:
    min_val, max_val = VALUE_RANGES[metric_key]
    if not (min_val <= value <= max_val):  # Raw value vs MPa range!
        continue  # Reject!
```

**After:**
```python
# Only basic sanity check - values should be reasonable numbers
if not (0 < value < 1_000_000_000):
    continue  # Reject obviously wrong values
# No standard-unit range checking here!
```

**Rationale:** Let `streamlit_app.py` do the validation AFTER conversion to standard units.

**Impact:** PDFs with values in kg/cm², kg/m³, or other units no longer get rejected before conversion.

### Fix #3: Enhanced Unit Format Support (unit_converter.py)

Added **unit notation variants** with superscripts to STRESS_TO_MPA:

```python
STRESS_TO_MPA = {
    'kg/cm2': 0.0980665,
    'kg/cm²': 0.0980665,     # With superscript ← NEW
    'kg/cm³': 0.0980665,
    'kg-cm2': 0.0980665,     # Dash notation ← NEW
    'kg-cm²': 0.0980665,     # Dash with superscript ← NEW
    'kgf/cm2': 0.0980665,
    'kgf/cm²': 0.0980665,    # With superscript ← NEW
    'n/mm2': 1,
    'n/mm²': 1,              # With superscript ← NEW
    'N/mm2': 1,
    'N/mm²': 1,              # With superscript ← NEW
}
```

**Impact:** PDFs with superscript characters (²/³) are now properly converted.

## Why PDF Extraction Was Failing

### Before Fixes (Formosa PDF example):

```
PDF Table Row: [抗張強度, kg/cm², ASTM D-638, ..., 370-400, 380, ...]
               
Step 1: _identify_metric("抗張強度") → returns None ✗
        (keyword not in config - looking for 拉伸強度)
Step 2: Row skipped, metric not stored
Result: Metric never extracted
```

### After Fixes:

```
PDF Table Row: [抗張強度, kg/cm², ASTM D-638, ..., 370-400, 380, ...]

Step 1: _identify_metric("抗張強度") → finds match! ✓
        (抗張強度 now in config keywords)
Step 2: Extract value: (370, "kg/cm²")
Step 3: Store in _validate_metrics() ✓
        (no longer rejected - basic sanity check only)
Step 4: Streamlit converts: 370 kg/cm² → 36.26 MPa ✓
Step 5: Validate converted value against VALUE_RANGES[tensile_strength] (1-200 MPa) ✓
Result: Metric successfully extracted and stored
```

## Testing Results

### Demo File (Still Works):
✓ Kingfa: 6 metrics extracted  
✓ Lavergne: 6 metrics extracted  
✓ BASF: 6 metrics extracted  
✓ Dow: 6 metrics extracted  

### Real PDFs (Should Now Work Better):
Expected improvement for:
- Formosa: Should find multiple metrics (was finding 1)
- Eastern Ever: Should find metrics (was finding 0)
- Kingfa real files: Should find metrics (was finding 0)
- Lavergne: Should find more metrics (was finding 1)

## Remaining Potential Issues

### If PDFs Still Only Show 1 Metric:

**Possible Causes:**
1. **Complex table layouts** - Some PDFs have metrics spread across multiple non-contiguous tables
2. **Text-based properties** - Some properties may be in text paragraphs, not tables
3. **Missing keywords** - More manufacturer-specific variants needed
4. **PDF encoding issues** - Special characters might not extract correctly from all PDFs

**Debugging Steps:**
1. Enable debug mode in config.py:
   ```python
   'debug_mode': True,
   ```
2. This will print extraction details to the terminal

3. Run extraction and check console for which metrics are found vs skipped

4. If metrics are found but filtered, you'll see:
   ```
   Value 370 kg/cm² for tensile_strength outside reasonable range
   ```

### If Conversion Produces Wrong Values:

Check that the unit extracted from PDF is recognized:
- `convert_stress()` uses `normalize_unit()` which lowercases and removes spaces
- Verify unit in PDF matches one of the keys in STRESS_TO_MPA after normalization
- Example: "kg/cm²" → normalize → "kg/cm²" → check dict → OK ✓

## Next Steps to Improve Extraction

1. **Collect feedback on which PDFs** still have low extraction rates
2. **Extract PDF samples** of problematic files to see actual structure
3. **Add more regional/manufacturer-specific keywords** as needed
4. **Consider OCR-based extraction** for scanned PDFs that pdfplumber can't parse
5. **Add manual override UI** - let users specify missing values in Streamlit

## Configuration Files Modified

1. **config.py**
   - Added Chinese keyword variants for 4 metrics
   - Kept VALUE_RANGES intact (used only in streamlit_app after conversion)

2. **enhanced_extractor.py**  
   - Simplified `_validate_metrics()` to do basic sanity checks only
   - Removed VALUE_RANGES checking from extraction layer

3. **unit_converter.py**
   - Added unit format variants with superscripts to STRESS_TO_MPA

4. **streamlit_app.py**
   - No changes needed (already does post-conversion validation)

## Expected Improvements

| Metric | Before | After | Status |
|--------|--------|-------|--------|
| Recognition of "抗張強度" | ✗ | ✓ | Fixed |
| Recognition of "彎曲彈数" | ✗ | ✓ | Fixed |
| kg/cm² values surviving validation | ✗ | ✓ | Fixed |
| Unit superscript handling | Partial | ✓ | Enhanced |
| 6 metrics per PDF | Rare | Expected | Testing needed |

