"""
Advanced PDF extraction with improved table handling
"""
import pdfplumber
import re
from typing import Dict, List, Tuple, Optional
from unit_converter import UnitConverter


class AdvancedPDFExtractor:
    """Advanced extraction with intelligent table parsing"""
    
    METRIC_KEYWORDS = {
        'tensile_strength': {
            'en': ['tensile strength', 'tensile strenth', 'tensile str', 'pull strength'],
            'zh': ['拉伸強度', '拉伸强度', '拉伸']
        },
        'flexural_strength': {
            'en': ['flexural strength', 'bend strength', 'bending strength'],
            'zh': ['彎曲強度', '弯曲强度', '彎曲', '弯曲']
        },
        'density': {
            'en': ['density', 'specific gravity', 'specific gr', 'sg'],
            'zh': ['比重', '密度']
        },
        'tensile_modulus': {
            'en': ['tensile modulus', 'tensile mod', 'young\'s modulus', 'youngs modulus'],
            'zh': ['拉伸模數', '拉伸模数', '拉伸模']
        },
        'flexural_modulus': {
            'en': ['flexural modulus', 'flexural mod', 'bending modulus'],
            'zh': ['彎曲模數', '弯曲模数', '彎曲模', '弯曲模']
        },
        'elongation': {
            'en': ['elongation', 'elongation at break', 'strain', 'percent elongation'],
            'zh': ['延伸率', '伸長率', '延伸', '伸长']
        }
    }
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.converter = UnitConverter()
        self.data = {}
    
    def extract_all(self) -> Dict:
        """Extract all metrics from PDF"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                # Extract from all pages
                for page_num, page in enumerate(pdf.pages):
                    self._process_page(page, page_num)
            
            return {
                'file': self.pdf_path,
                'metrics': self.data
            }
        
        except Exception as e:
            print(f"Error processing {self.pdf_path}: {e}")
            return {'file': self.pdf_path, 'metrics': {}}
    
    def _process_page(self, page, page_num: int):
        """Process a single page"""
        # Extract tables from page
        tables = page.extract_tables()
        if tables:
            for table in tables:
                self._process_table(table)
        
        # Also extract text
        text = page.extract_text()
        if text:
            self._process_text(text)
    
    def _process_table(self, table: List[List]):
        """Process a table extracted from PDF"""
        if not table or len(table) < 2:
            return
        
        # Try to identify rows containing our metrics
        for i, row in enumerate(table):
            row_text = ' '.join(str(cell or '') for cell in row)
            
            # Check which metric this row might contain
            metric_type = self._identify_metric(row_text)
            
            if metric_type and metric_type not in self.data:
                # Try to extract value from this row
                value, unit = self._extract_from_row(row)
                
                if value is not None:
                    self.data[metric_type] = (value, unit)
    
    def _identify_metric(self, text: str) -> Optional[str]:
        """Identify which metric a line of text refers to"""
        text_lower = text.lower()
        
        for metric, keywords in self.METRIC_KEYWORDS.items():
            # Check English keywords
            for keyword in keywords.get('en', []):
                if keyword.lower() in text_lower:
                    return metric
            
            # Check Chinese keywords
            for keyword in keywords.get('zh', []):
                if keyword in text:
                    return metric
        
        return None
    
    def _extract_from_row(self, row: List) -> Tuple[Optional[float], Optional[str]]:
        """Extract numeric value and unit from a table row"""
        values_found = []
        
        for cell in row:
            if cell is None or cell == '':
                continue
            
            cell_str = str(cell).strip()
            
            # Try to extract number and unit
            match = re.search(r'([\d.]+(?:[\s-]?[\d.]*)?)\s*([a-zA-Z°/\-³²%]*)', cell_str)
            
            if match:
                try:
                    value_str = match.group(1).replace(' ', '').replace('-', '.')
                    value = float(value_str)
                    unit = match.group(2).strip() if match.group(2) else ""
                    
                    # Sanity check on value range
                    if 0 < value < 1_000_000:
                        values_found.append((value, unit))
                
                except (ValueError, IndexError):
                    continue
        
        # Return the most reasonable value (usually the last one or the one with highest precision)
        if values_found:
            # Prefer the value with the longest unit string (usually more complete)
            return max(values_found, key=lambda x: len(str(x[1])))
        
        return None, None
    
    def _process_text(self, text: str):
        """Process extracted text"""
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            metric_type = self._identify_metric(line)
            
            if metric_type and metric_type not in self.data:
                # Try to find value in this line or next few lines
                for j in range(i, min(i + 3, len(lines))):
                    value, unit = self._extract_value_unit(lines[j])
                    if value is not None:
                        self.data[metric_type] = (value, unit)
                        break
            
            i += 1
    
    def _extract_value_unit(self, text: str) -> Tuple[Optional[float], Optional[str]]:
        """Extract value and unit from text"""
        # Pattern for number followed by unit
        matches = re.finditer(r'([\d.]+(?:[\s-]?[\d.]*)?)\s*([a-zA-Z°/\-³²%]*)', text)
        
        for match in matches:
            try:
                value_str = match.group(1).replace(' ', '').replace('-', '.')
                value = float(value_str)
                unit = match.group(2).strip() if match.group(2) else ""
                
                if 0 < value < 1_000_000:
                    return value, unit
            
            except ValueError:
                continue
        
        return None, None


class MetricWithConversion:
    """Metric with original and converted values"""
    
    def __init__(self, metric_name: str, original_value: float, 
                 original_unit: str, converter: UnitConverter):
        self.metric_name = metric_name
        self.original_value = original_value
        self.original_unit = original_unit
        self.converter = converter
        
        # Calculate standardized values
        self.standard_value, self.standard_unit = self._convert()
    
    def _convert(self) -> Tuple[float, str]:
        """Convert to standard unit based on metric type"""
        if self.metric_name == 'tensile_strength' or self.metric_name == 'flexural_strength':
            return self.converter.convert_stress(self.original_value, self.original_unit)
        
        elif self.metric_name == 'density':
            return self.converter.convert_density(self.original_value, self.original_unit)
        
        elif self.metric_name == 'tensile_modulus' or self.metric_name == 'flexural_modulus':
            return self.converter.convert_stress(self.original_value, self.original_unit)
        
        elif self.metric_name == 'elongation':
            return self.converter.convert_elongation(self.original_value, self.original_unit)
        
        return self.original_value, self.original_unit
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for Excel export"""
        return {
            'metric': self.metric_name,
            'original_value': self.original_value,
            'original_unit': self.original_unit,
            'standard_value': self.standard_value,
            'standard_unit': self.standard_unit
        }
