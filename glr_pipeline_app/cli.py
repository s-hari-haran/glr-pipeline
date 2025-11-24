#!/usr/bin/env python3
"""
GLR Pipeline CLI - Command Line Interface
Processes insurance templates and PDFs without Streamlit
Better for work laptop environments with network restrictions
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from pdf_extractor import extract_text_from_pdf
from llm_handler import GeminiLLMHandler
from template_handler import DocxTemplateHandler
from data_mapper import DataMapper


def main():
    """Main CLI application"""
    parser = argparse.ArgumentParser(
        description="GLR Pipeline - Insurance Template Filler CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py -t template.docx -p report.pdf -o output.docx
  python cli.py --template template.docx --pdf report.pdf --output filled.docx
        """
    )
    
    parser.add_argument(
        "-t", "--template",
        required=True,
        help="Path to Word template file (.docx)"
    )
    parser.add_argument(
        "-p", "--pdf",
        required=True,
        help="Path to PDF file (photo report, inspection notes)"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output path for filled document (.docx)"
    )
    
    args = parser.parse_args()
    
    # Validate files exist
    template_path = Path(args.template)
    pdf_path = Path(args.pdf)
    
    if not template_path.exists():
        print(f"❌ Template file not found: {template_path}")
        sys.exit(1)
    
    if not pdf_path.exists():
        print(f"❌ PDF file not found: {pdf_path}")
        sys.exit(1)
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set in .env file")
        sys.exit(1)
    
    try:
        print("\n🔄 GLR Pipeline - Processing Started")
        print(f"Template: {template_path}")
        print(f"PDF: {pdf_path}")
        
        # Step 1: Extract text from PDF
        print("\n📄 Step 1: Extracting text from PDF...")
        pdf_text = extract_text_from_pdf(str(pdf_path))
        print(f"✓ Extracted {len(pdf_text)} characters from PDF")
        
        # Step 2: Extract structured data using LLM
        print("\n🤖 Step 2: Extracting structured data with AI...")
        llm = GeminiLLMHandler(api_key)
        extracted_data = llm.extract_insurance_data(pdf_text)
        print("✓ Data extraction complete")
        print("\nExtracted Data:")
        for key, value in extracted_data.items():
            if value:
                print(f"  {key}: {value}")
        
        # Step 3: Load template and get placeholders
        print("\n📋 Step 3: Processing template...")
        template_handler = DocxTemplateHandler(str(template_path))
        placeholders = template_handler.get_placeholders()
        print(f"✓ Found {len(placeholders)} placeholders in template")
        print(f"  Placeholders: {', '.join(list(placeholders)[:5])}{'...' if len(placeholders) > 5 else ''}")
        
        # Step 4: Map extracted data to template placeholders
        print("\n🔗 Step 4: Mapping data to template...")
        mapper = DataMapper()
        replacements = mapper.map_data(extracted_data, placeholders)
        print(f"✓ Mapped {len(replacements)} fields")
        
        # Step 5: Fill template and save
        print("\n💾 Step 5: Filling template and saving...")
        output_path = Path(args.output)
        template_handler.fill_and_save(replacements, str(output_path))
        print(f"✓ Document saved to: {output_path}")
        
        print("\n✅ Processing Complete!")
        print(f"Output file: {output_path.absolute()}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
