"""
LLM Integration Module
Handles communication with Google Gemini API for data extraction and analysis
"""
import google.generativeai as genai
import logging
import json
import re
import os
from typing import Dict, List, Optional
from string import Template

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
        # Allow overriding model via env var `GLR_LLM_MODEL`, fallback to a supported model
        default_model = os.environ.get("GLR_LLM_MODEL", "gemini-2.5-pro")
        self.model_name = default_model
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Gemini LLM initialized using model: {self.model_name}")
    
    def extract_insurance_data(self, photo_report_text: str) -> Dict:
        """
        Extract key insurance data from photo report text.
        
        Args:
            photo_report_text: Extracted text from photo report PDF
            
        Returns:
            Dictionary with extracted key-value pairs
        """
        # Use string.Template to avoid interpreting braces in the prompt template
        safe_text = photo_report_text
        prompt_t = Template("""
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
        
        $text
        
        Return ONLY the JSON object, no other text.
        """)
        prompt = prompt_t.substitute(text=safe_text)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text or ""
            response_text = response_text.strip()

            # Clean up response if it has markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            # Try direct JSON parse first
            try:
                extracted_data = json.loads(response_text)
                logger.info("Successfully extracted insurance data from photo report")
                try:
                    logger.info(f"Extracted data keys: {sorted(list(extracted_data.keys()))}")
                    logger.info(json.dumps(extracted_data, indent=2))
                except Exception:
                    logger.debug("Could not serialize extracted_data for logging")
                return extracted_data
            except json.JSONDecodeError:
                # Attempt to locate JSON substring within the response
                candidate = self._extract_json_from_text(response_text)
                if candidate:
                    # Clean common issues: trailing commas
                    candidate = re.sub(r",\s*}\s*$", "}", candidate)
                    candidate = re.sub(r",\s*]", "]", candidate)
                    try:
                        extracted_data = json.loads(candidate)
                        logger.info("Extracted JSON by locating substring in LLM response")
                        return extracted_data
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON parsing error after substring extraction: {e}")
                        logger.error(f"Candidate JSON: {candidate}")
                # As a last resort, try to coerce single quotes to double quotes
                coerced = response_text.replace("'", '"')
                try:
                    extracted_data = json.loads(coerced)
                    logger.info("Parsed JSON after coercing quotes")
                    return extracted_data
                except json.JSONDecodeError as e:
                    logger.error(f"Final JSON parsing attempts failed: {e}")
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

    def _extract_json_from_text(self, text: str) -> Optional[str]:
        """Try to find a JSON object within arbitrary text.

        Returns the JSON substring if found, else None.
        """
        if not text:
            return None

        # Remove common markdown fences
        text = text.replace("```json", "").replace("```", "")

        # Find the first { and the last } and return that slice
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end < start:
            return None

        candidate = text[start:end+1].strip()
        return candidate
    
    def generate_narrative(self, extracted_data: Dict, template_context: str = "") -> Dict:
        """
        Generate narrative descriptions for template sections.
        
        Args:
            extracted_data: Extracted key-value pairs from photo report
            template_context: Optional context about the template structure
            
        Returns:
            Dictionary with generated narratives
        """
        # Use string.Template to safely inject the extracted data and context
        data_str = json.dumps(extracted_data, indent=2)
        context_str = template_context if template_context else ""
        prompt_t = Template("""
        You are an insurance claims adjuster writing a professional GLR (General Loss Report).
        Based on the following extracted information, generate professional narrative text for each section.
        
        Extracted Data:
        $data
        
        Template Context (if provided):
        $context
        
        Generate ONLY a valid JSON object with these narrative sections (max 2-3 sentences each):
        {
            "dwelling_description": "professional description of the dwelling and its condition",
            "property_condition": "assessment of general property condition and any concerns",
            "roof_details": "detailed description of roof materials, age, pitch, and condition",
            "front_elevation": "description of front elevation and any damages",
            "right_elevation": "description of right elevation and any damages",
            "rear_elevation": "description of rear elevation and any damages",
            "left_elevation": "description of left elevation and any damages",
            "interior": "description of interior and any damages",
            "damage_summary": "professional summary of all damages found"
        }
        
        Return ONLY the JSON object, no other text.
        """)
        prompt = prompt_t.substitute(data=data_str, context=context_str)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text or ""
            response_text = response_text.strip()

            # Clean up response if it has markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            try:
                narratives = json.loads(response_text)
                logger.info("Successfully generated narrative descriptions")
                return narratives
            except json.JSONDecodeError:
                candidate = self._extract_json_from_text(response_text)
                if candidate:
                    try:
                        narratives = json.loads(candidate)
                        logger.info("Parsed narratives from JSON substring")
                        return narratives
                    except json.JSONDecodeError as e:
                        logger.error(f"Narrative JSON parsing error after substring extraction: {e}")
                logger.error(f"Narrative JSON parsing failed. Response: {response_text}")
                return {}
        except Exception as e:
            logger.error(f"Error generating narrative: {e}")
            raise

    def generate_filled_template(self, template_text: str, extracted_data: Dict) -> str:
        """
        Ask the LLM to take the provided `template_text` (plain text with placeholders like [INSURED_NAME])
        and the `extracted_data` dict and return the template text with placeholders replaced by the
        extracted values. Returns a filled text string.
        """
        # Prepare a compact JSON for the prompt
        data_json = json.dumps(extracted_data, indent=2)

        prompt_template = Template(
            """
            You are an assistant that fills a template. Replace placeholders in the template
            with the corresponding values from the provided JSON. Placeholders are of the form
            [PLACEHOLDER]. If a value is null or missing, replace the placeholder with an empty string.

            Template:
            $template_text

            Extracted Data (JSON):
            $data

            Return ONLY the filled template text with placeholders replaced. Do not add any
            explanatory text or markdown fences.
            """
        )

        # Use Template to avoid issues with braces
        prompt = prompt_template.substitute(template_text=template_text, data=data_json)

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text or ""
            # Strip code fences if any
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            return response_text
        except Exception as e:
            logger.error(f"Error generating filled template via LLM: {e}")
            raise

    def generate_placeholder_mapping(self, placeholders: List[str], extracted_data: Dict) -> Dict[str, str]:
        """
        Ask the LLM to produce a strict JSON mapping from placeholder names (without brackets)
        to values, using the provided `extracted_data` as the source. The LLM must return
        ONLY a JSON object where keys exactly match the provided placeholders.

        If a value is missing or null, return an empty string for that key.
        """
        # Prepare prompt
        data_json = json.dumps(extracted_data, indent=2)
        placeholders_json = json.dumps(placeholders)

        prompt_t = Template(
            """
            You are an assistant that maps extracted insurance data to template placeholders.
            Given a list of placeholder names and a JSON object of extracted data, return
            a single valid JSON object where each key is exactly one of the placeholders
            (strings, no brackets) and the value is the best textual value to place there.

            - If the information is missing or null, use an empty string for that key.
            - Do not include any keys beyond the provided placeholders.
            - Return ONLY the JSON object, no commentary, no fences.

            Placeholders list:
            $placeholders

            Extracted Data:
            $data

            """
        )

        prompt = prompt_t.substitute(placeholders=placeholders_json, data=data_json)

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text or ""
            response_text = response_text.strip()

            # Remove fences
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            # Try parse
            try:
                mapping = json.loads(response_text)
                # Coerce missing keys
                result = {}
                for p in placeholders:
                    v = mapping.get(p)
                    if v is None:
                        result[p] = ""
                    else:
                        result[p] = str(v)
                logger.info("LLM provided placeholder mapping")
                return result
            except json.JSONDecodeError:
                # Try to extract JSON substring
                candidate = self._extract_json_from_text(response_text)
                if candidate:
                    try:
                        mapping = json.loads(candidate)
                        result = {p: str(mapping.get(p) or "") for p in placeholders}
                        logger.info("Parsed placeholder mapping from JSON substring")
                        return result
                    except Exception:
                        logger.error("Failed to parse mapping candidate from LLM response")

            # As a last resort, attempt a very loose coercion
            coerced = response_text.replace("'", '"')
            try:
                mapping = json.loads(coerced)
                result = {p: str(mapping.get(p) or "") for p in placeholders}
                logger.info("Parsed placeholder mapping after quote coercion")
                return result
            except Exception:
                logger.error("Could not parse placeholder mapping from LLM response")
                return {p: "" for p in placeholders}

        except Exception as e:
            logger.error(f"Error generating placeholder mapping via LLM: {e}")
            return {p: "" for p in placeholders}
