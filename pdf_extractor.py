"""
PDF extraction utilities for plastic material datasheets
"""
import pdfplumber
import re
from typing import Dict, List, Tuple, Optional
from unit_converter import UnitConverter

class PDFDataExtractor:
    """Extract metrics from plastic material datasheets"""
    
    # Keywords for each metric to search for
    METRIC_PATTERNS = {
        'tensile_strength': [
            'tensile strength', 'tensile strenth', 'pull strength',
            '拉伸強度', '拉伸强度', 'tensile'
        ],
        'flexural_strength': [
            'flexural strength', 'bend strength', 'bending strength',
            '彎曲強度', '弯曲强度', 'flexural'
        ],
        'density': [
            'density', 'specific gravity', 'specific gr',
            '比重', '密度', 'sg'
        ],
        'tensile_modulus': [
            'tensile modulus', 'tensile mod', 'young\'s modulus',
            '拉伸模數', '拉伸模数', 'modulus'
        ],
        'flexural_modulus': [
            'flexural modulus', 'flexural mod', 'bending modulus',
            '彎曲模數', '弯曲模数'
        ],
        'elongation': [
            'elongation', 'elongation at break', 'strain',
            '延伸率', '伸長率', 'extend'
        ]
    }
    
    def __init__(self, pdf_path: str):
        """Initialize with PDF file path"""
        self.pdf_path = pdf_path
        self.metrics = {}
        self.material_name = ""
        self.company_name = ""
    
    def extract(self) -> Dict:
        """Extract all metrics from the PDF"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                # Extract text and tables from all pages
                all_text = ""
                all_tables = []
                
                for page in pdf.pages:
                    all_text += page.extract_text() or ""
                    all_tables.extend(page.extract_tables() or [])
                
                # Try to extract material and company info
                self._extract_metadata(all_text)
                
                # Extract metrics from tables
                self._extract_from_tables(all_tables, all_text)
                
                # Extract metrics from text
                self._extract_from_text(all_text)
                
            return self._format_output()
        
        except Exception as e:
            print(f"Error extracting from {self.pdf_path}: {str(e)}")
            return {}
    
    def _extract_metadata(self, text: str):
        """Extract material and company information"""
        lines = text.split('\n')
        
        # Try to identify company and material name from first few lines
        for i, line in enumerate(lines[:20]):
            line_clean = line.strip()
            if len(line_clean) > 3 and len(line_clean) < 100:
                if i < 5 and not self.company_name:
                    self.company_name = line_clean
                if ('ABS' in line or 'PLA' in line or 'PETG' in line or 
                    'PP' in line or 'PE' in line) and not self.material_name:
                    self.material_name = line_clean
    
    def _extract_from_tables(self, tables: List[List[List]], text: str):
        """Extract metrics from PDF tables"""
        for table in tables:
            if not table or len(table) < 2:
                continue
            
            # Convert table to text format for easier searching
            for row in table:
                if len(row) < 2:
                    continue
                
                row_text = ' '.join(str(cell) for cell in row if cell)
                
                # Check each metric
                for metric, keywords in self.METRIC_PATTERNS.items():
                    if metric in self.metrics:
                        continue
                    
                    if self._matches_keywords(row_text, keywords):
                        # Try to extract value and unit from this row
                        result = self._extract_value_unit(row)
                        if result:
                            self.metrics[metric] = result
    
    def _extract_from_text(self, text: str):
        """Extract metrics from body text using regex patterns"""
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            for metric, keywords in self.METRIC_PATTERNS.items():
                if metric in self.metrics:
                    continue
                
                if self._matches_keywords(line_lower, keywords):
                    # Try to extract value from this line and next few lines
                    result = self._extract_value_from_line(line)
                    if result:
                        self.metrics[metric] = result
                    else:
                        # Try next line
                        if i + 1 < len(lines):
                            result = self._extract_value_from_line(lines[i + 1])
                            if result:
                                self.metrics[metric] = result
    
    def _matches_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def _extract_value_unit(self, row: List) -> Optional[Tuple[float, str]]:
        """Extract numeric value and unit from a table row"""
        for cell in row:
            if cell is None:
                continue
            
            cell_str = str(cell).strip()
            
            # Try to parse number with unit
            match = re.search(r'([\d.]+)\s*([a-zA-Z°/\-³²]*)', cell_str)
            if match:
                try:
                    value = float(match.group(1))
                    unit = match.group(2).strip() if match.group(2) else ""
                    if value > 0:
                        return (value, unit)
                except ValueError:
                    continue
        
        return None
    
    def _extract_value_from_line(self, line: str) -> Optional[Tuple[float, str]]:
        """Extract numeric value and unit from a line of text"""
        # Pattern: number followed by optional unit
        pattern = r'([\d.]+(?:[\s-][\d.]+)*)\s*([a-zA-Z°/\-³²]*)'
        
        matches = re.finditer(pattern, line)
        
        for match in matches:
            try:
                value_str = match.group(1).replace(' ', '').replace('-', '')
                value = float(value_str)
                unit = match.group(2).strip() if match.group(2) else ""
                
                if 0 < value < 1_000_000:  # Sanity check
                    return (value, unit)
            except ValueError:
                continue
        
        return None
    
    def _extract_value_unit_from_row(self, row: List) -> Optional[Tuple[float, str]]:
        """Extract value and unit from a table row - looks for patterns"""
        if not row or len(row) < 2:
            return None
        
        # Typically: [description, ...other cells..., value, unit]
        # or [description, test method, condition, value, unit]
        
        for i in range(len(row) - 1, 0, -1):
            cell = row[i]
            if cell is None:
                continue
            
            cell_str = str(cell).strip()
            
            # Try to parse as number
            try:
                value = float(cell_str)
                
                # Check if next cell is unit
                if i + 1 < len(row):
                    unit = str(row[i + 1]).strip() if row[i + 1] else ""
                    return (value, unit)
                
                # Or try to extract unit from current or previous cell
                if i > 0:
                    prev_cell = str(row[i - 1]).strip()
                    match = re.search(r'([a-zA-Z°/\-³²]+)', prev_cell)
                    if match:
                        return (value, match.group(1))
                
                # Default empty unit
                return (value, "")
            
            except ValueError:
                continue
        
        return None
    
    def _format_output(self) -> Dict:
        """Format extracted metrics for output"""
        return {
            'file': self.pdf_path,
            'company': self.company_name,
            'material': self.material_name,
            'metrics': self.metrics
        }


def extract_metric_value(metric_dict: Dict) -> Optional[Tuple[float, str]]:
    """
    Extract and validate metric value and unit from dictionary.
    Returns (value, unit) or None
    """
    if not metric_dict or 'metrics' not in metric_dict:
        return None
    
    metrics = metric_dict['metrics']
    
    # Find first available value
    for key in ['tensile_strength', 'flexural_strength', 'density', 
                'tensile_modulus', 'flexural_modulus', 'elongation']:
        if key in metrics:
            return metrics[key]
    
    return None
