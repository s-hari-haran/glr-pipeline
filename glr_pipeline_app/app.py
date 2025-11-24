"""
GLR Pipeline Streamlit Application
Main interface for automating insurance template filling with LLM
"""
import streamlit as st
import os
from pathlib import Path
import logging
from typing import Optional, Dict
import tempfile
import json

# Import custom modules
from pdf_extractor import extract_text_from_pdf, extract_structured_content
from llm_handler import GeminiLLMHandler
from template_handler import DocxTemplateHandler
from data_mapper import DataMapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="GLR Pipeline - Insurance Template Filler",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = False
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = None
    if "template_handler" not in st.session_state:
        st.session_state.template_handler = None
    if "replacements" not in st.session_state:
        st.session_state.replacements = None
    if "processing_complete" not in st.session_state:
        st.session_state.processing_complete = False


def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    return len(api_key.strip()) > 0


def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">📋 GLR Pipeline - Insurance Template Filler</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automate insurance template filling using AI and photo reports</div>', 
                unsafe_allow_html=True)
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("---")
        
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            help="Get your API key from https://ai.google.dev/",
            placeholder="Enter your Google Gemini API key"
        )
        
        if api_key and validate_api_key(api_key):
            st.session_state.api_key_set = True
            st.success("✓ API key set")
        else:
            st.session_state.api_key_set = False
            st.warning("⚠️ API key required to proceed")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This application automates the process of filling insurance templates 
        (Word documents) using information extracted from photo reports (PDFs).
        
        **Process:**
        1. Upload insurance template (.docx)
        2. Upload photo report(s) (.pdf)
        3. System extracts text and analyzes with AI
        4. Maps data to template fields
        5. Download completed form
        """)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Step 1: Upload Insurance Template")
        st.markdown("Upload your insurance template in .docx format")
        
        template_file = st.file_uploader(
            "Choose template file",
            type=["docx"],
            key="template_upload",
            help="Upload the insurance claim template in Word format"
        )
        
        if template_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_template:
                tmp_template.write(template_file.read())
                tmp_template_path = tmp_template.name
            
            try:
                st.session_state.template_handler = DocxTemplateHandler(tmp_template_path)
                st.success(f"✓ Template loaded successfully")
                
                with st.expander("View Template Placeholders"):
                    placeholders = sorted(st.session_state.template_handler.get_placeholders())
                    st.write(f"**Found {len(placeholders)} placeholder(s):**")
                    st.code("\n".join([f"[{p}]" for p in placeholders]))
            except Exception as e:
                st.error(f"Error loading template: {str(e)}")
                st.session_state.template_handler = None
    
    with col2:
        st.markdown("### 📸 Step 2: Upload Photo Report(s)")
        st.markdown("Upload one or more photo reports in .pdf format")
        
        photo_files = st.file_uploader(
            "Choose photo report(s)",
            type=["pdf"],
            key="photo_upload",
            accept_multiple_files=True,
            help="Upload PDF photo reports. Multiple PDFs will be combined."
        )
        
        if photo_files:
            st.info(f"✓ {len(photo_files)} photo report(s) uploaded")
    
    st.markdown("---")
    
    # Processing section
    if template_file and photo_files and st.session_state.template_handler:
        st.markdown("### ⚡ Step 3: Process and Fill Template")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Process & Extract Data", key="process_btn"):
                if not st.session_state.api_key_set:
                    st.error("❌ Please configure your API key in the sidebar first")
                else:
                    with st.spinner("Processing photo reports..."):
                        try:
                            # Extract text from all PDFs
                            all_text = []
                            for pdf_file in photo_files:
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                                    tmp_pdf.write(pdf_file.read())
                                    tmp_pdf_path = tmp_pdf.name
                                
                                pdf_text = extract_text_from_pdf(tmp_pdf_path)
                                all_text.append(pdf_text)
                                os.unlink(tmp_pdf_path)
                            
                            combined_text = "\n---NEXT_DOCUMENT---\n".join(all_text)
                            
                            # Use LLM to extract data
                            with st.spinner("Analyzing with AI..."):
                                llm = GeminiLLMHandler(api_key)
                                st.session_state.extracted_data = llm.extract_insurance_data(combined_text)
                                
                                # Generate narratives
                                with st.spinner("Generating narrative text..."):
                                    narratives = llm.generate_narrative(st.session_state.extracted_data)
                                    st.session_state.extracted_data.update(narratives)
                            
                            st.success("✓ Data extraction complete!")
                            st.session_state.processing_complete = True
                            
                        except Exception as e:
                            st.error(f"Error during processing: {str(e)}")
                            logger.error(f"Processing error: {e}")
        
        # Show extracted data
        if st.session_state.extracted_data:
            st.markdown("### 📊 Step 4: Review Extracted Data")
            
            tabs = st.tabs(["Structured Data", "Raw Text Analysis"])
            
            with tabs[0]:
                st.write("**Extracted insurance information:**")
                
                # Display in organized columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Personal Information:**")
                    display_data = {
                        "Insured Name": st.session_state.extracted_data.get("insured_name"),
                        "Policy #": st.session_state.extracted_data.get("policy_number"),
                        "Claim #": st.session_state.extracted_data.get("claim_number"),
                        "Date of Loss": st.session_state.extracted_data.get("date_of_loss"),
                        "Date Inspected": st.session_state.extracted_data.get("date_inspected"),
                    }
                    for key, value in display_data.items():
                        st.write(f"• **{key}:** {value if value else '(not found)'}")
                
                with col2:
                    st.write("**Property Information:**")
                    property_data = {
                        "Address": f"{st.session_state.extracted_data.get('address_street', '')}, {st.session_state.extracted_data.get('address_city', '')}, {st.session_state.extracted_data.get('address_state', '')}",
                        "Dwelling Type": st.session_state.extracted_data.get("dwelling_type"),
                        "Roof Material": st.session_state.extracted_data.get("roof_material"),
                        "Roof Age": st.session_state.extracted_data.get("roof_age"),
                        "Type of Loss": st.session_state.extracted_data.get("type_of_loss"),
                    }
                    for key, value in property_data.items():
                        st.write(f"• **{key}:** {value if value else '(not found)'}")
            
            with tabs[1]:
                st.write("**Damage Summary:**")
                st.info(st.session_state.extracted_data.get("damage_summary", "No summary available"))
            
            # Generate final document
            st.markdown("### 📝 Step 5: Generate Final Document")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Generate Filled Document", key="generate_btn"):
                    with st.spinner("Filling template..."):
                        try:
                            # Map data to template
                            mapper = DataMapper(
                                st.session_state.extracted_data,
                                st.session_state.template_handler.get_placeholders()
                            )
                            st.session_state.replacements = mapper.map_data()
                            
                            # Generate document
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_output:
                                output_path = tmp_output.name
                            
                            st.session_state.template_handler.fill_and_save(
                                st.session_state.replacements,
                                output_path
                            )
                            
                            # Read file for download
                            with open(output_path, "rb") as f:
                                file_data = f.read()
                            
                            st.success("✓ Document generated successfully!")
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Filled Document",
                                data=file_data,
                                file_name="Completed_GLR_Report.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                            
                            os.unlink(output_path)
                            
                        except Exception as e:
                            st.error(f"Error generating document: {str(e)}")
                            logger.error(f"Generation error: {e}")
            
            with col2:
                if st.button("🔍 View Mapping Report", key="report_btn"):
                    if st.session_state.replacements:
                        st.json(st.session_state.replacements)
    
    else:
        st.info("⏳ Please upload both template and photo report(s) to proceed")


if __name__ == "__main__":
    main()
