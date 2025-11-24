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
        logger.info("DataMapper initialized")
    
    def map_data(self) -> Dict[str, str]:
        """
        Map extracted data to template placeholders.
        
        Returns:
            Dictionary ready for template replacement
        """
        replacements = {}
        
        for placeholder in self.template_placeholders:
            value = self._find_value_for_placeholder(placeholder)
            if value is not None:
                replacements[placeholder] = str(value)
                self.mapping_used[placeholder] = value
                logger.info(f"Mapped [{placeholder}] -> {value}")
            else:
                logger.warning(f"No mapping found for [{placeholder}]")
        
        return replacements
    
    def _find_value_for_placeholder(self, placeholder: str) -> Optional[str]:
        """
        Find appropriate value for a placeholder.
        
        Args:
            placeholder: Template placeholder name
            
        Returns:
            Value to fill, or None if not found
        """
        # Check direct mapping
        if placeholder in self.DEFAULT_MAPPING:
            mapped_field = self.DEFAULT_MAPPING[placeholder]
            if mapped_field and mapped_field in self.extracted_data:
                return self.extracted_data[mapped_field]
        
        # Try fuzzy matching
        lower_placeholder = placeholder.lower()
        for key, value in self.extracted_data.items():
            if value is not None and key.lower() in lower_placeholder:
                return value
        
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
