"""
Data Mapping Module
Maps extracted data to template placeholders with intelligent field matching
"""
import logging
from typing import Dict, List, Optional
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataMapper:
    """Maps extracted insurance data to template placeholders"""
    
    # Mapping rules: template placeholder -> extracted data field
    DEFAULT_MAPPING = {
        "DATE_LOSS": "date_of_loss",
        "INSURED_NAME": "insured_name",
        "MORTGAGE_CO": "mortgage_company",
        "INSURED_H_STREET": "address_street",
        "INSURED_H_CITY": "address_city",
        "INSURED_H_STATE": "address_state",
        "INSURED_H_ZIP": "address_zip",
        "DATE_INSPECTED": "date_inspected",
        "MORTGAGEE": "mortgage_company",
        "TOL_CODE": "type_of_loss",
        "DATE_RECEIVED": None,  # Not typically in photo report
        "POLICY_NUMBER": "policy_number",
    }
    
    def __init__(self, extracted_data: Dict, template_placeholders: set):
        """
        Initialize mapper with extracted data and template structure.
        
        Args:
            extracted_data: Data extracted from photo report by LLM
            template_placeholders: Set of placeholders in template
        """
        self.extracted_data = extracted_data
        self.template_placeholders = template_placeholders
        self.mapping_used = {}
        logger.info(f"DataMapper initialized. Extracted keys: {sorted(list(self.extracted_data.keys()))}")
    
    def map_data(self) -> Dict[str, str]:
        """
        Map extracted data to template placeholders.
        
        Returns:
            Dictionary ready for template replacement
        """
        replacements = {}
        
        for placeholder in self.template_placeholders:
            value = self._find_value_for_placeholder(placeholder)
            # Always include the placeholder in replacements; use empty string if not found
            replacements[placeholder] = str(value) if value is not None else ""
            if value is not None:
                self.mapping_used[placeholder] = value
                logger.info(f"Mapped [{placeholder}] -> {value}")
            else:
                logger.warning(f"No mapping found for [{placeholder}] - leaving blank")
        
        return replacements
    
    def _find_value_for_placeholder(self, placeholder: str) -> Optional[str]:
        """
        Find appropriate value for a placeholder.
        
        Args:
            placeholder: Template placeholder name
            
        Returns:
            Value to fill, or None if not found
        """
        # 1) Direct mapping from DEFAULT_MAPPING
        if placeholder in self.DEFAULT_MAPPING:
            mapped_field = self.DEFAULT_MAPPING[placeholder]
            if mapped_field and mapped_field in self.extracted_data:
                return self.extracted_data[mapped_field]

        # Normalization helpers
        def norm(s: str) -> str:
            return re.sub(r"[^a-z0-9]", "", s.lower()) if s else ""

        norm_placeholder = norm(placeholder)

        # 2) Exact key match (case-insensitive)
        for key, value in self.extracted_data.items():
            if value is None:
                continue
            if norm(key) == norm_placeholder:
                return value

        # 3) Substring matches both ways
        for key, value in self.extracted_data.items():
            if value is None:
                continue
            nk = norm(key)
            if nk and (nk in norm_placeholder or norm_placeholder in nk):
                return value

        # 4) Token overlap: split on common separators and match meaningful tokens
        def tokens(s: str):
            # split camel/pascal/underscore and numbers
            return re.findall(r"[a-z]+|\d+", s.lower()) if s else []

        ph_tokens = set(tokens(placeholder))
        best_key = None
        best_score = 0
        for key, value in self.extracted_data.items():
            if value is None:
                continue
            key_tokens = set(tokens(key))
            # score is number of overlapping tokens
            score = len(ph_tokens & key_tokens)
            if score > best_score:
                best_score = score
                best_key = key

        if best_key and best_score > 0:
            return self.extracted_data[best_key]

        # 5) Address parsing fallback: if placeholder expects parts and we have a full risk_address
        addr_fields = {
            'ins_h_street': 'INSURED_H_STREET',
        }

        # If the placeholder is an address component, attempt to parse risk_address
        lower_ph = placeholder.lower()
        if 'address' in self.extracted_data and isinstance(self.extracted_data.get('address'), str):
            full_addr = self.extracted_data.get('address')
        else:
            full_addr = self.extracted_data.get('risk_address') or self.extracted_data.get('address')

        if full_addr and any(x in lower_ph for x in ['street', 'ins', 'insured_h', 'ins_h']):
            # Try simple parsing: 'street, city, state zip' or 'street\ncity, state zip'
            addr = full_addr.replace('\n', ', ')
            parts = [p.strip() for p in addr.split(',') if p.strip()]
            # street is usually first part
            if parts:
                street = parts[0]
            else:
                street = None

            city = None
            state = None
            zipc = None
            if len(parts) >= 2:
                # attempt to parse last part for state and zip
                last = parts[-1]
                m = re.search(r"([A-Za-z]{2})\s*(\d{5}(?:-\d{4})?)$", last)
                if m:
                    state = m.group(1)
                    zipc = m.group(2)
                    # city is the middle part(s)
                    city = ', '.join(parts[1:-1]) if len(parts) > 2 else None
                else:
                    # maybe parts[-1] is city
                    city = parts[-1]

            # Map requested placeholder
            if any(k in lower_ph for k in ['ins_h_street', 'insured_h_street', 'insured_h_street'.lower()] ):
                return street
            if 'city' in lower_ph:
                return city
            if 'state' in lower_ph:
                return state
            if 'zip' in lower_ph or 'zip_code' in lower_ph:
                return zipc

        # 6) No match found
        return None
    
    def get_mapping_report(self) -> Dict:
        """
        Get a report of how data was mapped.
        
        Returns:
            Dictionary with mapping details
        """
        return {
            "total_placeholders": len(self.template_placeholders),
            "mapped_count": len(self.mapping_used),
            "unmapped": list(self.template_placeholders - set(self.mapping_used.keys())),
            "mapping_used": self.mapping_used
        }
