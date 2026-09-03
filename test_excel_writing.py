"""
Quick test to verify extraction and Excel writing works
"""
from enhanced_extractor import EnhancedPDFExtractor
from excel_writer import ExcelWriter
from unit_converter import UnitConverter
import os

# Create dummy extraction result to test Excel writing
test_results = {
    "Lavergne": [
        {
            "metrics": {
                "tensile_strength": (370, "kg/cm²"),
                "flexural_strength": (620, "kg/cm²"),
                "density": (1.04, "g/cm³"),
                "tensile_modulus": (2300, "MPa"),
                "flexural_modulus": (1900, "MPa"),
                "elongation": (5.0, "%"),
            }
        }
    ],
    "Formosa": [
        {
            "metrics": {
                "tensile_strength": (19000, "kg/cm²"),  # Range parsed, first value
                "flexural_strength": (15, "kN/cm²"),  # Needs unit conversion
                "density": (1.05, "g/cm³"),
                "tensile_modulus": (2200, "MPa"),
                "flexural_modulus": (1800, "MPa"),
                "elongation": (4.8, "%"),
            }
        }
    ],
}

# Setup
output_file = "test_extraction_results.xlsx"
material_type = "ABS"
converter = UnitConverter()

# Create Excel writer
excel_writer = ExcelWriter(output_file)

# Process extraction results
ALL_METRICS = [
    'tensile_strength',
    'flexural_strength', 
    'density',
    'tensile_modulus',
    'flexural_modulus',
    'elongation'
]

# Organize by company
company_data = {}
for company_name, results_list in test_results.items():
    company_data[company_name] = {}
    
    for result_item in results_list:
        metrics = result_item['metrics']
        
        # Process each metric found
        for metric_key, (original_value, original_unit) in metrics.items():
            if metric_key not in company_data[company_name]:
                company_data[company_name][metric_key] = {
                    'original_value': original_value,
                    'original_unit': original_unit
                }
                
                # Convert to standard units
                if metric_key in ['tensile_strength', 'flexural_strength', 
                                 'tensile_modulus', 'flexural_modulus']:
                    std_value, std_unit = converter.convert_stress(original_value, original_unit)
                elif metric_key == 'density':
                    std_value, std_unit = converter.convert_density(original_value, original_unit)
                elif metric_key == 'elongation':
                    std_value, std_unit = converter.convert_elongation(original_value, original_unit)
                else:
                    std_value, std_unit = original_value, original_unit
                
                company_data[company_name][metric_key]['standard_value'] = std_value
                company_data[company_name][metric_key]['standard_unit'] = std_unit

# Add records
print("Adding records to Excel...")
for company_name, metrics_dict in company_data.items():
    record = {
        'company': company_name,
        'material': material_type
    }
    
    # Add all 6 metrics (use extracted value or empty)
    for metric_key in ALL_METRICS:
        if metric_key in metrics_dict:
            metric_data = metrics_dict[metric_key]
            record[f'{metric_key}_original_value'] = metric_data['original_value']
            record[f'{metric_key}_original_unit'] = metric_data['original_unit']
            record[f'{metric_key}_standard_value'] = metric_data['standard_value']
            record[f'{metric_key}_standard_unit'] = metric_data['standard_unit']
        else:
            record[f'{metric_key}_original_value'] = "-"
            record[f'{metric_key}_original_unit'] = "-"
            record[f'{metric_key}_standard_value'] = "-"
            record[f'{metric_key}_standard_unit'] = "-"
    
    print(f"  Adding: {company_name}")
    excel_writer.add_record(**record)

# Create and save
print("\nCreating sheets and saving...")
excel_writer.create_sheets()
excel_writer.save()

if os.path.exists(output_file):
    print(f"✓ SUCCESS: {output_file} created")
else:
    print(f"✗ FAILED: {output_file} not created")
