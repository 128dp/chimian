"""
Configuration file for Plastic Material Metrics Extractor
Customize keywords, units, and extraction behavior

STANDARD UNITS (SI-based):
=========================
- Stress (Tensile/Flexural Strength, Tensile/Flexural Modulus): MPa
- Density: tonnes/mm³ (metric tonnes per cubic millimeter)
- Elongation: strain (dimensionless, 0-1 where 1 = 100%)
- Length: mm (millimeters)
- Time: s (seconds)
- Force: Newton (N)
- Mass: tonnes (metric tonnes)
"""

# Material names and their aliases
MATERIAL_TYPES = {
    'ABS': ['ABS', 'acrylonitrile butadiene styrene', 'acrylonitril-butadiene-styrene'],
    'PP': ['PP', 'polypropylene', 'polypropylen'],
    'PE': ['PE', 'polyethylene', 'polyethen'],
    'PETG': ['PETG', 'polyethylene terephthalate glycol'],
    'PLA': ['PLA', 'polylactic acid'],
    'PC': ['PC', 'polycarbonate'],
    'NYLON': ['NYLON', 'PA', 'polyamide'],
}

# Metric keywords for extraction (can be extended)
METRIC_KEYWORDS = {
    'tensile_strength': {
        'en': [
            'tensile strength',
            'tensile strenth',
            'tensile str',
            'pull strength',
            'tensile stress',
        ],
        'zh': [
            '拉伸強度',
            '拉伸强度',
            '抗張強度',    # Taiwan/alternative terminology
            '抗张强度',    # Simplified
            '拉伸',
        ]
    },
    'flexural_strength': {
        'en': [
            'flexural strength',
            'bend strength',
            'bending strength',
        ],
        'zh': [
            '彎曲強度',
            '弯曲强度',
            '彎曲',
            '弯曲',
            '撓曲強度',    # Alternative Chinese term
            '挠曲强度',    # Simplified
        ]
    },
    'density': {
        'en': [
            'density',
            'specific gravity',
            'specific gr',
            'sg',
            'density ()',
        ],
        'zh': [
            '比重',
            '密度',
        ]
    },
    'tensile_modulus': {
        'en': [
            'tensile modulus',
            'tensile mod',
            'young\'s modulus',
            'youngs modulus',
            'modulus of elasticity',
        ],
        'zh': [
            '拉伸模數',
            '拉伸模数',
            '拉伸模',
        ]
    },
    'flexural_modulus': {
        'en': [
            'flexural modulus',
            'flexural mod',
            'bending modulus',
        ],
        'zh': [
            '彎曲模數',
            '弯曲模数',            '彎曲彈数',    # Alternative name used in some datasheets
            '弯曲弹数',    # Simplified alternative            '彎曲模',
            '弯曲模',
        ]
    },
    'elongation': {
        'en': [
            'elongation',
            'elongation at break',
            'strain',
            'percent elongation',
            'extension',
        ],
        'zh': [
            '延伸率',
            '伸長率',
            '延伸',
            '伸长',
        ]
    }
}

# Unit conversion factors (can be extended)
STRESS_UNITS = {
    'mpa': 1.0,
    'MPa': 1.0,
    'pa': 1e-6,
    'Pa': 1e-6,
    'kpa': 1e-3,
    'kPa': 1e-3,
    'gpa': 1000,
    'GPa': 1000,
    'psi': 1/145.038,
    'kg/cm2': 0.0980665,
    'kg/cm³': 0.0980665,
    'kgf/cm2': 0.0980665,
    'n/mm2': 1.0,
    'N/mm2': 1.0,
}

DENSITY_UNITS = {
    'tonnes/mm³': 1.0,
    'tonnes/mm3': 1.0,
    'tonne/mm³': 1.0,
    'tonne/mm3': 1.0,
    'g/cm³': 1e-9,      # g/cm³ to tonnes/mm³
    'g/cm3': 1e-9,
    'kg/m³': 1e-12,     # kg/m³ to tonnes/mm³
    'kg/m3': 1e-12,
    'tonnes/m³': 1e-9,  # tonnes/m³ to tonnes/mm³
    'tonnes/m3': 1e-9,
    'tonne/m³': 1e-9,
    'tonne/m3': 1e-9,
}

# Test conditions to preserve (optional)
TEST_CONDITIONS = [
    '23°C',
    '23 °C',
    'room temperature',
    'unannealed',
    'annealed',
]

# Value range sanity checks
VALUE_RANGES = {
    'tensile_strength': (1, 200),          # MPa
    'flexural_strength': (10, 500),        # MPa
    'density': (0.8e-9, 2.0e-9),          # tonnes/mm³ (roughly 0.8-2.0 g/cm³)
    'tensile_modulus': (1000, 100000),    # MPa
    'flexural_modulus': (1000, 100000),   # MPa
    'elongation': (0, 1.0),               # strain (0-100%)
}

# PDF processing settings
PDF_SETTINGS = {
    'extract_tables': True,
    'extract_text': True,
    'table_min_rows': 2,
    'table_min_cols': 2,
}

# Extraction behavior
EXTRACTION_SETTINGS = {
    'merge_similar_metrics': True,
    'prefer_first_value': True,  # Use first value found instead of averaging
    'strict_unit_matching': False,  # Allow partial unit matches
    'debug_mode': False,  # Print debug info
}

# Excel output settings
EXCEL_SETTINGS = {
    'include_test_method': True,
    'include_test_condition': False,
    'freeze_header': True,
    'auto_adjust_columns': True,
    'number_format': '0.0000',
}

# Languages to support (can be extended)
SUPPORTED_LANGUAGES = ['en', 'zh']

# Default output filename pattern
OUTPUT_FILENAME_PATTERN = "material_extraction_{timestamp}.xlsx"

# Logging
LOGGING = {
    'verbose': True,
    'log_file': None,  # Set to filename to log to file
    'debug_output': False,
}
