"""
Unit conversion utilities for plastic material metrics
"""

class UnitConverter:
    """Convert various units to standard units"""
    
    # Mass conversions to tonnes
    MASS_TO_TONNES = {
        'kg': 1/1000,
        'g': 1/1_000_000,
        'mg': 1/1_000_000_000,
        'tonne': 1,
        't': 1,
        'ton': 1,
        'lb': 1/2204.62,
        'lbs': 1/2204.62,
        'oz': 1/35_274,
    }
    
    # Time conversions to seconds
    TIME_TO_SECONDS = {
        's': 1,
        'sec': 1,
        'second': 1,
        'seconds': 1,
        'min': 60,
        'minute': 60,
        'minutes': 60,
        'hr': 3600,
        'hrs': 3600,
        'hour': 3600,
        'hours': 3600,
        'h': 3600,
        'day': 86400,
        'days': 86400,
    }
    
    # Length conversions to mm
    LENGTH_TO_MM = {
        'mm': 1,
        'cm': 10,
        'm': 1000,
        'inch': 25.4,
        'in': 25.4,
        '"': 25.4,
        'um': 0.001,
        'μm': 0.001,
    }
    
    # Stress conversions to MPa
    STRESS_TO_MPA = {
        'mpa': 1,
        'MPa': 1,
        'pa': 1/1_000_000,
        'Pa': 1/1_000_000,
        'kpa': 1/1000,
        'kPa': 1/1000,
        'gpa': 1000,
        'GPa': 1000,
        'psi': 1/145.038,
        'kg/cm2': 0.0980665,
        'kg/cm²': 0.0980665,     # With superscript
        'kg/cm³': 0.0980665,
        'kg/cm³': 0.0980665,     # With superscript (same as above)
        'kg-cm2': 0.0980665,
        'kg-cm²': 0.0980665,
        'kgf/cm2': 0.0980665,
        'kgf/cm²': 0.0980665,    # With superscript
        'kg·cm-2': 0.0980665,    # Dot notation
        'kg·cm²': 0.0980665,     # Dot with superscript
        'n/mm2': 1,  # same as MPa
        'n/mm²': 1,  # With superscript
        'N/mm2': 1,
        'N/mm²': 1,              # With superscript
    }
    
    # Force conversions to Newton
    FORCE_TO_NEWTON = {
        'n': 1,
        'N': 1,
        'kn': 1000,
        'kN': 1000,
        'kgf': 9.80665,
        'kg-f': 9.80665,
        'kg': 9.80665,
        'lbf': 4.44822,
        'lb-f': 4.44822,
        'lbs': 4.44822,
        'oz': 0.278014,
    }
    
    @staticmethod
    def normalize_unit(unit_str):
        """Normalize unit string for comparison"""
        if not unit_str:
            return ""
        return unit_str.lower().strip().replace('°', '').replace('±', '').replace(' ', '')
    
    @staticmethod
    def convert_stress(value, from_unit):
        """Convert stress values to MPa"""
        if value is None or from_unit is None:
            return None, None
        
        normalized = UnitConverter.normalize_unit(from_unit)
        
        # Direct match
        if normalized in UnitConverter.STRESS_TO_MPA:
            factor = UnitConverter.STRESS_TO_MPA[normalized]
            return round(value * factor, 4), 'MPa'
        
        # Try partial matches
        for key, factor in UnitConverter.STRESS_TO_MPA.items():
            if key in normalized or normalized in key:
                return round(value * factor, 4), 'MPa'
        
        return value, from_unit
    
    @staticmethod
    def convert_density(value, from_unit):
        """Convert density to standard density (tonnes/mm³)
        
        Conversions:
        - g/cm³ to tonnes/mm³: multiply by 1e-9
        - kg/m³ to tonnes/mm³: multiply by 1e-12
        - tonnes/m³ to tonnes/mm³: multiply by 1e-9
        - tonnes/cm³ to tonnes/mm³: multiply by 1e-9
        - Specific gravity (unitless) to tonnes/mm³: multiply by 1e-9 (assuming density of water = 1 g/cm³)
        """
        if value is None or from_unit is None:
            return None, None
        
        normalized = UnitConverter.normalize_unit(from_unit)
        
        # Already in tonnes/mm³
        if 'tonnes/mm' in normalized or 'tonne/mm' in normalized or 't/mm' in normalized:
            return round(value, 12), 'tonnes/mm³'
        
        # g/cm³ to tonnes/mm³ (multiply by 1e-9)
        if 'g/cm' in normalized:
            return round(value * 1e-9, 12), 'tonnes/mm³'
        
        # kg/m³ to tonnes/mm³ (multiply by 1e-12)
        if 'kg/m' in normalized:
            return round(value * 1e-12, 12), 'tonnes/mm³'
        
        # tonnes/m³ to tonnes/mm³ (multiply by 1e-9)
        if 'tonnes/m' in normalized or 'tonne/m' in normalized:
            return round(value * 1e-9, 12), 'tonnes/mm³'
        
        # tonnes/cm³ to tonnes/mm³ (multiply by 1e-9)
        if 'tonnes/cm' in normalized or 'tonne/cm' in normalized:
            return round(value * 1e-9, 12), 'tonnes/mm³'
        
        # If no unit specified, assume it's specific gravity (unitless, 1 g/cm³)
        if normalized == '':
            return round(value * 1e-9, 12), 'tonnes/mm³'
        
        return value, from_unit
    
    @staticmethod
    def convert_length(value, from_unit):
        """Convert length values to mm"""
        if value is None or from_unit is None:
            return None, None
        
        normalized = UnitConverter.normalize_unit(from_unit)
        
        if normalized in UnitConverter.LENGTH_TO_MM:
            factor = UnitConverter.LENGTH_TO_MM[normalized]
            return round(value * factor, 4), 'mm'
        
        # Try partial matches
        for key, factor in UnitConverter.LENGTH_TO_MM.items():
            if key in normalized:
                return round(value * factor, 4), 'mm'
        
        return value, from_unit
    
    @staticmethod
    def convert_time(value, from_unit):
        """Convert time values to seconds"""
        if value is None or from_unit is None:
            return None, None
        
        normalized = UnitConverter.normalize_unit(from_unit)
        
        if normalized in UnitConverter.TIME_TO_SECONDS:
            factor = UnitConverter.TIME_TO_SECONDS[normalized]
            return round(value * factor, 4), 's'
        
        # Try partial matches
        for key, factor in UnitConverter.TIME_TO_SECONDS.items():
            if key in normalized:
                return round(value * factor, 4), 's'
        
        return value, from_unit
    
    @staticmethod
    def convert_mass(value, from_unit):
        """Convert mass values to tonnes"""
        if value is None or from_unit is None:
            return None, None
        
        normalized = UnitConverter.normalize_unit(from_unit)
        
        if normalized in UnitConverter.MASS_TO_TONNES:
            factor = UnitConverter.MASS_TO_TONNES[normalized]
            return round(value * factor, 9), 'tonne'
        
        # Try partial matches
        for key, factor in UnitConverter.MASS_TO_TONNES.items():
            if key in normalized:
                return round(value * factor, 9), 'tonne'
        
        return value, from_unit
    
    @staticmethod
    def convert_elongation(value, from_unit):
        """Convert elongation to strain (dimensionless)"""
        if value is None or from_unit is None:
            return None, None
        
        normalized = UnitConverter.normalize_unit(from_unit)
        
        # Already a percentage or strain
        if '%' in normalized or 'percent' in normalized:
            # Convert percentage to strain (divide by 100)
            return round(value / 100, 4), 'strain'
        
        if 'strain' in normalized:
            return round(value, 4), 'strain'
        
        # If unitless, might be already in decimal form
        if normalized == '':
            return round(value, 4), 'strain'
        
        return value, from_unit
