"""
Enhanced PDF Extraction with configuration support
"""
import pdfplumber
import re
from typing import Dict, List, Tuple, Optional
from unit_converter import UnitConverter

try:
    from config import METRIC_KEYWORDS, VALUE_RANGES, EXTRACTION_SETTINGS
except ImportError:
    # Fallback if config not available
    METRIC_KEYWORDS = {}
    VALUE_RANGES = {}
    EXTRACTION_SETTINGS = {}

# Matches test method / standard designators like "ASTM D638", "ASTM* D792",
# "ASTM D-638", "ISO 527", "UL** 94"
TEST_METHOD_PATTERN = re.compile(
    r'(ASTM\*{0,2}\s*D[\s\-]?\d+|ISO\s*\d+|UL\*{0,2}\s*\d+)',
    re.IGNORECASE
)

# Known unit tokens (checked longest-first so multi-word units match before
# shorter substrings, e.g. "g/10 min" before "min")
_UNIT_TOKENS = [
    'g/10 min', 'g/10min', 'kg-cm/cm', 'kg/cm2', 'kg/cm\u00b2', 'n/mm2',
    'tonnes/mm3', 'tonnes/mm\u00b3', 'kg/m3', 'kg/m\u00b3',
    'g/cm3', 'g/cm\u00b3', 'mpa', 'gpa', 'kpa', 'pa', 'j/m', '\u00b0c', '%',
]
_UNIT_TOKENS.sort(key=len, reverse=True)


class EnhancedPDFExtractor:
    """Enhanced PDF extraction with configuration support"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.converter = UnitConverter()
        self.data: Dict[str, List[Dict]] = {}
        self.debug = EXTRACTION_SETTINGS.get('debug_mode', False)
        
        # Column-role cache: manufacturer tables are often split across
        # multiple pdfplumber "tables" (section dividers break detection),
        # so once we detect a header row we reuse its column roles for
        # subsequent same-shaped tables that lack their own header.
        self.last_known_roles: Dict[int, str] = {}
        self.last_known_col_count: Optional[int] = None
        
        # Use config keywords or fallback
        if METRIC_KEYWORDS:
            self.metric_keywords = METRIC_KEYWORDS
        else:
            self._default_keywords()
        
        # Flatten keywords into a single (keyword, metric) list sorted by
        # keyword length descending, so the most specific/longest keyword
        # match always wins regardless of which metric it belongs to.
        # This avoids bugs like a generic "flexural" keyword under
        # flexural_strength shadowing "flexural modulus".
        self._keyword_index: List[Tuple[str, str, bool]] = []
        for metric, keywords in self.metric_keywords.items():
            for keyword in keywords.get('en', []):
                self._keyword_index.append((keyword.lower(), metric, False))
            for keyword in keywords.get('zh', []):
                self._keyword_index.append((keyword, metric, True))
        self._keyword_index.sort(key=lambda item: len(item[0]), reverse=True)
    
    def _default_keywords(self):
        """Set default keywords if config not loaded"""
        self.metric_keywords = {
            'tensile_strength': {
                'en': ['tensile strength', 'tensile str', 'pull strength'],
                'zh': ['拉伸強度', '拉伸强度']
            },
            'flexural_strength': {
                'en': ['flexural strength', 'bend strength', 'bending strength'],
                'zh': ['彎曲強度', '弯曲强度']
            },
            'density': {
                'en': ['density', 'specific gravity', 'sg'],
                'zh': ['比重', '密度']
            },
            'tensile_modulus': {
                'en': ['tensile modulus', 'young\'s modulus'],
                'zh': ['拉伸模數', '拉伸模数']
            },
            'flexural_modulus': {
                'en': ['flexural modulus', 'bending modulus'],
                'zh': ['彎曲模數', '弯曲模数']
            },
            'elongation': {
                'en': ['elongation', 'elongation at break', 'strain'],
                'zh': ['延伸率', '伸長率']
            }
        }
    
    def extract_all(self) -> Dict:
        """Extract all metrics from PDF"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    self._process_page(page, page_num)
            
            return {
                'file': self.pdf_path,
                'metrics': self._validate_metrics()
            }
        
        except Exception as e:
            if self.debug:
                print(f"Error processing {self.pdf_path}: {e}")
            return {'file': self.pdf_path, 'metrics': {}}
    
    def _process_page(self, page, page_num: int):
        """Process a single page"""
        # Extract tables
        tables = page.extract_tables()
        table_data_extracted = False
        if tables:
            for table in tables:
                if self._process_table(table):
                    table_data_extracted = True
        
        # Extract text - only used as a fallback when no table on this page
        # yielded usable column-based rows. Running text extraction on a page
        # whose table already parsed cleanly re-reads the same row as loose
        # text, which can misidentify a "TEST CONDITION" cell (e.g.
        # "50mm/min,3.2mm") as a bogus value+unit and create a garbled
        # duplicate entry alongside the correct table-derived one.
        if not table_data_extracted:
            text = page.extract_text()
            if text:
                self._process_text(text)
    
    def _process_table(self, table: List[List]) -> bool:
        """Process a table using column-role detection.
        
        Manufacturer tables have different column layouts (property/unit/
        test method/value in varying order). We detect header rows to map
        column index -> role (property, test_method, unit, typical_value,
        control_value, range_value, tolerance_value), then read each data
        row using those roles instead of naively scanning left-to-right.
        
        Returns True if this table yielded usable structured (column-based)
        data, so the caller can skip the loose-text fallback for this page.
        """
        if not table or len(table) < 1:
            return False
        
        num_cols = max((len(row) for row in table if row), default=0)
        
        header_rows, data_start = self._split_header_and_data(table)
        roles = self._detect_column_roles(header_rows) if header_rows else {}
        
        has_value_role = any(
            role in ('typical_value', 'control_value', 'range_value', 'tolerance_value')
            for role in roles.values()
        )
        
        if has_value_role:
            # Cache these roles in case a later split table (section divider
            # broke pdfplumber's detection) reuses the same column layout.
            self.last_known_roles = roles
            self.last_known_col_count = num_cols
        elif self.last_known_roles and num_cols == self.last_known_col_count:
            roles = self.last_known_roles
            has_value_role = True
        
        if has_value_role:
            # Return whether any entry was actually extracted, not just
            # whether a value column was detected - a table can have a
            # recognizable header (e.g. an unrelated small table whose
            # header text happens to match "unit"/"value") but contain no
            # rows matching a known metric, in which case the page's real
            # data may still be sitting in the loose text and the text
            # fallback must still run.
            return self._extract_rows_with_roles(table[data_start:], roles)
        else:
            # Fallback: no reliable column layout detected, scan cells directly
            row_extracted = False
            for row in table:
                if self._process_row(row):
                    row_extracted = True
            return row_extracted
    
    def _split_header_and_data(self, table: List[List]) -> Tuple[List[List], int]:
        """Split a table into header rows and the index where data rows start.
        
        A row is considered the first data row once its first cell matches
        a known metric keyword.
        """
        for idx, row in enumerate(table):
            if not row:
                continue
            first_cell = str(row[0] or '')
            if self._identify_metric(first_cell):
                return table[:idx], idx
        
        # No recognizable data row found; treat everything as header
        return table, len(table)
    
    def _detect_column_roles(self, header_rows: List[List]) -> Dict[int, str]:
        """Detect which column index holds which role based on header text.
        
        Some manufacturers split header info across multiple rows (e.g. a
        merged "TAIRILAC AF358R" cell with "TOLERANCE"/"TYPICAL VALUES"
        sub-headers below it), so header rows are combined column-wise.
        """
        if not header_rows:
            return {}
        
        role_patterns = [
            ('test_method', ['test method', 'test standard', 'standard', 'method']),
            ('test_condition', ['test condition', 'condition']),
            ('unit', ['unit']),
            ('typical_value', ['typical value', 'typical values']),
            ('control_value', ['control value']),
            ('tolerance_value', ['tolerance']),
            ('range_value', ['range']),
            ('property', ['propert']),
        ]
        
        max_cols = max((len(row) for row in header_rows if row), default=0)
        roles: Dict[int, str] = {}
        
        for col_idx in range(max_cols):
            texts = []
            for row in header_rows:
                if row and col_idx < len(row) and row[col_idx]:
                    texts.append(str(row[col_idx]))
            combined = ' '.join(texts).lower().replace('\n', ' ')
            combined = re.sub(r'\s+', ' ', combined).strip()
            if not combined:
                continue
            
            for role, patterns in role_patterns:
                if role in roles.values():
                    continue
                if any(pattern in combined for pattern in patterns):
                    roles[col_idx] = role
                    break
        
        return roles
    
    def _extract_rows_with_roles(self, rows: List[List], roles: Dict[int, str]) -> bool:
        """Extract metrics from data rows using detected column roles.
        
        Some manufacturers list the same property multiple times under
        different test conditions (e.g. Flexural Modulus tested at two
        different span/speed settings), sometimes as a full repeated row
        and sometimes as a continuation row where only the test condition
        and value are filled in (property/test method/unit cells are
        blank and should be carried forward from the previous row).
        
        Returns True if at least one entry was actually extracted, so the
        caller can tell detected-but-empty column layouts (e.g. an
        unrelated small table whose header text happens to match a role
        pattern) apart from genuinely useful tables.
        """
        property_col = next((c for c, r in roles.items() if r == 'property'), 0)
        test_method_col = next((c for c, r in roles.items() if r == 'test_method'), None)
        test_condition_col = next((c for c, r in roles.items() if r == 'test_condition'), None)
        unit_col = next((c for c, r in roles.items() if r == 'unit'), None)
        
        value_col = None
        for role in ('typical_value', 'control_value', 'range_value', 'tolerance_value'):
            col = next((c for c, r in roles.items() if r == role), None)
            if col is not None:
                value_col = col
                break
        
        def cell_at(row, col_idx):
            if col_idx is None or col_idx >= len(row):
                return None
            val = row[col_idx]
            return str(val).strip() if val else None
        
        last_metric = None
        last_test_method = None
        last_unit = None
        added_any = False
        
        for row in rows:
            if not row:
                continue
            
            property_text = cell_at(row, property_col)
            metric_type = self._identify_metric(property_text) if property_text else None
            
            if metric_type:
                last_metric = metric_type
            elif last_metric and not property_text:
                # Continuation row: same property, different test condition
                metric_type = last_metric
            else:
                # Unrelated property (or section divider) - reset context
                last_metric = None
                continue
            
            raw_value_cell = cell_at(row, value_col)
            if not raw_value_cell:
                continue
            
            value, extracted_unit = self._extract_value_unit(raw_value_cell)
            if value is None:
                continue
            
            unit_cell = cell_at(row, unit_col)
            if unit_cell:
                last_unit = unit_cell
            unit = unit_cell or last_unit or extracted_unit
            
            test_method_cell = cell_at(row, test_method_col)
            if test_method_cell:
                cleaned_method = re.sub(r'\s+', ' ', test_method_cell.replace('\n', ' ')).strip()
                method_match = TEST_METHOD_PATTERN.search(cleaned_method)
                last_test_method = method_match.group(1) if method_match else cleaned_method
            test_method = last_test_method
            
            test_condition_cell = cell_at(row, test_condition_col)
            test_condition = (
                re.sub(r'\s+', ' ', test_condition_cell.replace('\n', ' ')).strip()
                if test_condition_cell else None
            )
            
            if self._add_entry(metric_type, {
                'value': value,
                'unit': unit,
                'test_method': test_method,
                'test_condition': test_condition,
                'raw_value': raw_value_cell
            }):
                added_any = True
        
        return added_any
    
    def _add_entry(self, metric_type: str, entry: Dict) -> bool:
        """Append an extracted entry for a metric, skipping exact duplicates
        (same unit/test_condition/raw_value) that may arise when both table
        and text extraction pick up the same row.
        
        Returns True if a new entry was appended, False if it was a
        duplicate that was skipped.
        """
        entries = self.data.setdefault(metric_type, [])
        dedup_key = (entry.get('unit'), entry.get('test_condition'), entry.get('raw_value'))
        for existing in entries:
            if (existing.get('unit'), existing.get('test_condition'), existing.get('raw_value')) == dedup_key:
                return False
        entries.append(entry)
        return True
    
    def _process_row(self, row: List) -> bool:
        """Fallback: process a table row by scanning cells left-to-right
        (used when no reliable column layout could be detected).
        
        Returns True if an entry was extracted from this row.
        """
        if not row:
            return False
        
        row_text = ' '.join(str(cell or '') for cell in row)
        metric_type = self._identify_metric(row_text)
        
        if metric_type:
            value, unit, test_method, raw_value = self._extract_full_row_data(row)
            if value is not None:
                self._add_entry(metric_type, {
                    'value': value,
                    'unit': unit,
                    'test_method': test_method,
                    'test_condition': None,
                    'raw_value': raw_value
                })
                return True
        
        return False
    
    def _extract_full_row_data(self, row: List) -> Tuple[Optional[float], Optional[str], Optional[str], Optional[str]]:
        """Extract value, unit, test method, and raw value from row"""
        test_method = None
        raw_value = None
        value = None
        unit = None
        
        # Look for a test method standard in the row
        for cell in row:
            cell_str = str(cell or '').replace('\n', ' ')
            method_match = TEST_METHOD_PATTERN.search(cell_str)
            if method_match:
                test_method = re.sub(r'\s+', ' ', method_match.group(1)).strip()
                break
        
        # Look for numeric values
        for cell in row:
            if cell is None or cell == '':
                continue
            
            cell_str = str(cell).strip()
            value_extracted, unit_extracted = self._extract_value_unit(cell)
            if value_extracted is not None:
                value = value_extracted
                unit = unit_extracted
                raw_value = cell_str  # Keep the original cell content
                break
        
        return value, unit, test_method, raw_value
    
    def _extract_value_unit(self, cell) -> Tuple[Optional[float], Optional[str]]:
        """Extract value and unit from a cell"""
        if cell is None:
            return None, None
        
        cell_str = str(cell).strip()
        if not cell_str:
            return None, None
        
        # First, remove thousands separators (commas that are between digits)
        # e.g., "19,000~22,000" → "19000~22000", "2,300 MPa" → "2300 MPa"
        cleaned = re.sub(r'(\d),(\d)', r'\1\2', cell_str)
        # Collapse spaced-out digit groups like "3 7 0 - 400" → "370 - 400"
        cleaned = re.sub(r'(?<=\d) (?=\d)', '', cleaned)
        
        # Extract a number (potentially multiple digits with decimal point)
        # This will match the FIRST number in the string
        # Handles: 380, 1.042, 19000, 370, 620, etc.
        match = re.match(r'([\d.]+)', cleaned)
        
        if match:
            try:
                value = float(match.group(1))
                
                # Extract unit - everything after the first number (and any range/range separator)
                # Remove range indicators (~, -, spaces after the first number)
                remaining = cleaned[len(match.group(1)):].lstrip('~-\u2013\u2014 \t')
                # Find the unit part (letters/special chars)
                unit_match = re.match(r'([a-zA-Z°/\-³²%]+)', remaining)
                unit = unit_match.group(1) if unit_match else ""
                
                # Sanity check
                if 0 < value < 1_000_000:
                    return value, unit
            
            except ValueError:
                pass
        
        return None, None
    
    def _identify_metric(self, text: str) -> Optional[str]:
        """Identify which metric a text refers to.
        
        Checks the single longest matching keyword across ALL metrics (not
        grouped by metric), so a specific term like "flexural modulus"
        always wins over a shorter generic term like "flexural" even if
        that generic term happens to belong to a different metric.
        """
        if not text:
            return None
        
        text_lower = text.lower()
        
        for keyword, metric, is_zh in self._keyword_index:
            haystack = text if is_zh else text_lower
            if keyword in haystack:
                return metric
        
        return None
    
    def _process_text(self, text: str):
        """Process body text, preferring structured PROPERTY ... TEST_METHOD UNIT VALUE
        line parsing (used by manufacturers whose tables don't parse into clean
        columns), falling back to simple line scanning."""
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if self._process_text_line(line):
                continue
            
            # Fallback: old simple line-based extraction
            metric_type = self._identify_metric(line)
            if metric_type:
                value, unit = self._extract_value_unit(line)
                if value is not None:
                    self._add_entry(metric_type, {
                        'value': value,
                        'unit': unit,
                        'test_method': None,
                        'test_condition': None,
                        'raw_value': line
                    })
    
    def _process_text_line(self, line: str) -> bool:
        """Try to parse a line shaped like "PROPERTY[, condition] TEST_METHOD UNIT VALUE".
        Returns True if a metric was successfully extracted."""
        method_match = TEST_METHOD_PATTERN.search(line)
        if not method_match:
            return False
        
        property_full = line[:method_match.start()].strip(' ,.')
        metric_type = self._identify_metric(property_full)
        if not metric_type:
            return False
        
        # Split "Property Name, condition" or "Property Name @ condition"
        # e.g. "Density, 23°C" -> condition "23°C"; "Tensile Strength @ Yield, 50 mm/min"
        parts = re.split(r',| @ ', property_full, maxsplit=1)
        test_condition = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
        
        test_method = re.sub(r'\s+', ' ', method_match.group(1)).strip()
        remainder = line[method_match.end():].strip()
        
        unit = None
        value_text = remainder
        remainder_lower = remainder.lower()
        for token in _UNIT_TOKENS:
            if remainder_lower.startswith(token):
                unit = remainder[:len(token)]
                value_text = remainder[len(token):].strip()
                break
        
        if not value_text:
            return False
        
        value, extracted_unit = self._extract_value_unit(value_text)
        if value is None:
            return False
        
        self._add_entry(metric_type, {
            'value': value,
            'unit': unit or extracted_unit,
            'test_method': test_method,
            'test_condition': test_condition,
            'raw_value': value_text
        })
        return True
    
    def _validate_metrics(self) -> Dict[str, List[Dict]]:
        """Return extracted metrics as lists of entries (a property may have
        multiple entries when tested under different conditions). No range
        validation on converted units here - the caller converts and
        validates after standardization."""
        validated: Dict[str, List[Dict]] = {}
        
        for metric_key, entries in self.data.items():
            valid_entries = []
            for entry in entries:
                value = entry.get('value')
                if value is None:
                    continue
                
                try:
                    if not (0 < value < 1_000_000_000):
                        if self.debug:
                            print(f"Value {value} for {metric_key} outside reasonable range")
                        continue
                except (TypeError, ValueError):
                    continue
                
                valid_entries.append({
                    'value': value,
                    'unit': entry.get('unit'),
                    'test_method': entry.get('test_method'),
                    'test_condition': entry.get('test_condition'),
                    'raw_value': entry.get('raw_value'),
                })
            
            if valid_entries:
                validated[metric_key] = valid_entries
        
        return validated


# For backward compatibility
AdvancedPDFExtractor = EnhancedPDFExtractor

