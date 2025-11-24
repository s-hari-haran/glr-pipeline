"""
LLM Integration Module
Handles communication with Google Gemini API for data extraction and analysis
"""
import google.generativeai as genai
import logging
import json
import re
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiLLMHandler:
    """Handles all interactions with Google Gemini LLM"""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini API handler.
        
        Args:
            api_key: Google Generative AI API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("Gemini LLM initialized")
    
    def extract_insurance_data(self, photo_report_text: str) -> Dict:
        """
        Extract key insurance data from photo report text.
        
        Args:
            photo_report_text: Extracted text from photo report PDF
            
        Returns:
            Dictionary with extracted key-value pairs
        """
        prompt = """
        You are an insurance claims adjuster AI. Extract all relevant information from this photo report.
        Return ONLY a valid JSON object with the following fields (use null for missing values):
        {
            "insured_name": "name of insured/property owner",
            "policy_number": "policy number",
            "claim_number": "claim number",
            "mortgage_company": "mortgage company name if mentioned",
            "date_of_loss": "date when damage occurred",
            "date_inspected": "date of inspection",
            "risk_address": "full property address",
            "address_street": "street address",
            "address_city": "city",
            "address_state": "state",
            "address_zip": "zip code",
            "dwelling_type": "type of dwelling (1 story, 2 story, etc)",
            "roof_material": "roof shingles/material type",
            "roof_age": "approximate roof age in years",
            "roof_pitch": "roof pitch (e.g., 5/12)",
            "roof_condition": "description of roof condition",
            "front_elevation_damage": "damage description for front",
            "right_elevation_damage": "damage description for right side",
            "rear_elevation_damage": "damage description for rear",
            "left_elevation_damage": "damage description for left side",
            "interior_damage": "description of interior damage if any",
            "type_of_loss": "type of loss (wind, hail, etc)",
            "damage_summary": "brief summary of all damages",
            "additional_notes": "any other relevant information"
        }
        
        Here is the photo report text:
        
        {text}
        
        Return ONLY the JSON object, no other text.
        """.format(text=photo_report_text)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up response if it has markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            extracted_data = json.loads(response_text)
            logger.info("Successfully extracted insurance data from photo report")
            return extracted_data
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Response text: {response_text}")
            return self._parse_response_fallback(response_text)
        except Exception as e:
            logger.error(f"Error extracting insurance data: {e}")
            raise
    
    def _parse_response_fallback(self, response_text: str) -> Dict:
        """Fallback parsing if JSON extraction fails"""
        logger.warning("Using fallback parsing for LLM response")
        result = {
            "insured_name": None,
            "policy_number": None,
            "claim_number": None,
            "mortgage_company": None,
            "date_of_loss": None,
            "date_inspected": None,
            "risk_address": None,
            "address_street": None,
            "address_city": None,
            "address_state": None,
            "address_zip": None,
            "dwelling_type": None,
            "roof_material": None,
            "roof_age": None,
            "roof_pitch": None,
            "roof_condition": None,
            "front_elevation_damage": None,
            "right_elevation_damage": None,
            "rear_elevation_damage": None,
            "left_elevation_damage": None,
            "interior_damage": None,
            "type_of_loss": None,
            "damage_summary": None,
            "additional_notes": response_text
        }
        return result
    
    def generate_narrative(self, extracted_data: Dict, template_context: str = "") -> Dict:
        """
        Generate narrative descriptions for template sections.
        
        Args:
            extracted_data: Extracted key-value pairs from photo report
            template_context: Optional context about the template structure
            
        Returns:
            Dictionary with generated narratives
        """
        prompt = """
        You are an insurance claims adjuster writing a professional GLR (General Loss Report).
        Based on the following extracted information, generate professional narrative text for each section.
        
        Extracted Data:
        {data}
        
        Template Context (if provided):
        {context}
        
        Generate ONLY a valid JSON object with these narrative sections (max 2-3 sentences each):
        {{
            "dwelling_description": "professional description of the dwelling and its condition",
            "property_condition": "assessment of general property condition and any concerns",
            "roof_details": "detailed description of roof materials, age, pitch, and condition",
            "front_elevation": "description of front elevation and any damages",
            "right_elevation": "description of right elevation and any damages",
            "rear_elevation": "description of rear elevation and any damages",
            "left_elevation": "description of left elevation and any damages",
            "interior": "description of interior and any damages",
            "damage_summary": "professional summary of all damages found"
        }}
        
        Return ONLY the JSON object, no other text.
        """.format(data=json.dumps(extracted_data, indent=2), context=template_context)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up response if it has markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            narratives = json.loads(response_text)
            logger.info("Successfully generated narrative descriptions")
            return narratives
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in narrative generation: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error generating narrative: {e}")
            raise
