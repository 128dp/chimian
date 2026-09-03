# Density Unit Standardization Update

## Overview
Updated the entire codebase to use **tonnes/mm³** as the standard density unit instead of **g/cm³**, aligning with the SI unit specification: "density is in tonnes/mm cube. every mass SI unit is tonnes, every length is in mm, time is s, and MPa, and Newton"

## Files Modified

### 1. **unit_converter.py**
**Change:** Updated `convert_density()` method to convert all density values to tonnes/mm³

**Old Logic:**
- g/cm³ → g/cm³ (1.0x)
- kg/m³ → g/cm³ (÷1000)

**New Logic:**
- g/cm³ → tonnes/mm³ (×1e-9)
- kg/m³ → tonnes/mm³ (×1e-12)
- tonnes/m³ → tonnes/mm³ (×1e-9)
- tonnes/cm³ → tonnes/mm³ (×1e-9)
- Unitless (specific gravity) → tonnes/mm³ (×1e-9)

**Scientific Basis:**
- 1 g/cm³ = 1,000,000 g per 1,000 mm³ = 1 tonne per 1,000,000,000 mm³ = 1e-9 tonnes/mm³
- 1 kg/m³ = 1 kg per 1e9 mm³ = 1e-3 tonne per 1e9 mm³ = 1e-12 tonnes/mm³

**Example Conversions:**
- ABS (1.05 g/cm³) → 1.05e-9 tonnes/mm³
- PP (0.90 g/cm³) → 9.0e-10 tonnes/mm³
- PE (0.95 g/cm³) → 9.5e-10 tonnes/mm³

### 2. **excel_writer.py**
**Change:** Updated column header in DEFAULT_COLUMNS

**Before:**
```python
{'name': 'Density (g/cm³)', 'width': 16, 'format': '0.0000'},
```

**After:**
```python
{'name': 'Density (tonnes/mm³)', 'width': 18, 'format': '0.0000e+00'},
```

**Note:** Updated format to scientific notation (0.0000e+00) to properly display very small numbers in tonnes/mm³

### 3. **config.py**
**Changes:**
1. Added comprehensive header documentation of all standard units
2. Updated DENSITY_UNITS conversion dictionary
3. Updated VALUE_RANGES for density validation

**Standard Units (documented at top):**
```
- Stress (Tensile/Flexural Strength, Moduli): MPa
- Density: tonnes/mm³ (metric tonnes per cubic millimeter)
- Elongation: strain (dimensionless, 0-1 where 1 = 100%)
- Length: mm (millimeters)
- Time: s (seconds)
- Force: Newton (N)
- Mass: tonnes (metric tonnes)
```

**DENSITY_UNITS Dictionary:**
```python
'g/cm³': 1e-9,      # g/cm³ to tonnes/mm³
'kg/m³': 1e-12,     # kg/m³ to tonnes/mm³
'tonnes/m³': 1e-9,  # tonnes/m³ to tonnes/mm³
```

**VALUE_RANGES for density:**
```python
'density': (0.8e-9, 2.0e-9),  # tonnes/mm³ (roughly 0.8-2.0 g/cm³)
```

### 4. **streamlit_app.py**
**Change:** Updated Unit Settings display in the sidebar

**Before:**
```
Stress: MPa
Density: g/cm³
Elongation: strain
Length: mm
Time: seconds
```

**After:**
```
Stress (Tensile/Flexural Strength, Moduli): MPa
Density: tonnes/mm³
Elongation: strain (dimensionless)
Length: mm
Time: seconds
Force: Newton
Mass: tonnes
```

### 5. **demo_material_extraction.py**
**Change:** Updated all 4 company data records to use tonnes/mm³

**Example (Kingfa):**
- Before: `'density_standard_value': 1.050, 'density_standard_unit': 'g/cm³'`
- After: `'density_standard_value': 1.050e-9, 'density_standard_unit': 'tonnes/mm³'`

**Updated Companies:**
- Kingfa: 1.05 g/cm³ → 1.05e-9 tonnes/mm³
- Lavergne: 1.055 g/cm³ → 1.055e-9 tonnes/mm³
- BASF: 1.052 g/cm³ → 1.052e-9 tonnes/mm³
- Dow: 1.048 g/cm³ → 1.048e-9 tonnes/mm³

## Verification

✅ **Demo File Test:** demo_material_extraction.py runs successfully and generates correct density values in tonnes/mm³

✅ **Unit Consistency:** All SI units now properly aligned:
- Stress/Modulus: MPa ✓
- Density: tonnes/mm³ ✓
- Elongation: strain ✓
- Length: mm ✓
- Time: seconds ✓
- Force: Newton ✓
- Mass: tonnes ✓

✅ **Streamlit UI:** Shows updated unit settings with tonnes/mm³ for density

✅ **Excel Output:** Column headers display "Density (tonnes/mm³)" with scientific notation format

## Backward Compatibility

- The `convert_density()` method still accepts g/cm³, kg/m³, and other common density units as input
- All PDFs can still contain density values in any common unit (will be converted to tonnes/mm³)
- The excel_writer.py add_record() method still accepts **kwargs flexibly

## No Breaking Changes

- All other metric conversions remain unchanged (MPa, mm, strain, etc.)
- All extraction logic remains unchanged
- All PDF parsing logic remains unchanged
- Only density conversion and display units were modified

## Migration Notes for Users

If you have previously generated Excel files with density in g/cm³:
- The new format uses scientific notation (e.g., 1.05e-09 instead of 1.05)
- This is mathematically equivalent but displayed differently for precision
- Use a calculator or spreadsheet formula to verify: `g/cm³ × 1e-9 = tonnes/mm³`
- Example: 1.05 g/cm³ × 1e-9 = 1.05e-9 tonnes/mm³

## Testing the Update

Run the demo script to verify:
```bash
python demo_material_extraction.py
```

Open the generated `demo_abs_extraction.xlsx` and check the Density column values are in scientific notation (e.g., 1.05e-09).

Launch Streamlit to see the updated unit information:
```bash
python -m streamlit run streamlit_app.py
```

Check the Settings panel to confirm the Unit Settings display "Density: tonnes/mm³"
