"""
PDF Text Extraction Module
Extracts text and metadata from PDF files
"""
import pdfplumber
import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Combined text from all pages
    """
    try:
        full_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    full_text.append(text)
                logger.info(f"Extracted text from page {page_num}")
        
        return "\n".join(full_text)
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise


def extract_text_with_confidence(pdf_path: str) -> Tuple[str, List[Dict]]:
    """
    Extract text from PDF with additional metadata.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Tuple of (combined text, list of page metadata)
    """
    try:
        full_text = []
        metadata = []
        
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    full_text.append(text)
                
                metadata.append({
                    "page": page_num,
                    "total_pages": num_pages,
                    "width": page.width,
                    "height": page.height,
                    "has_text": bool(text)
                })
                logger.info(f"Processed page {page_num}/{num_pages}")
        
        return "\n".join(full_text), metadata
    except Exception as e:
        logger.error(f"Error extracting text with metadata: {e}")
        raise


def extract_structured_content(pdf_path: str) -> Dict:
    """
    Extract structured content from photo report PDF.
    Attempts to identify sections and key information.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with structured content
    """
    try:
        text, metadata = extract_text_with_confidence(pdf_path)
        
        result = {
            "raw_text": text,
            "metadata": metadata,
            "num_pages": len(metadata),
            "extraction_successful": bool(text)
        }
        
        logger.info(f"Successfully extracted structured content from {pdf_path}")
        return result
    except Exception as e:
        logger.error(f"Error extracting structured content: {e}")
        raise
