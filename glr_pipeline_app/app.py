"""
GLR Pipeline Streamlit Application
Main interface for automating insurance template filling with LLM
"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
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
    if "awaiting_overrides" not in st.session_state:
        st.session_state.awaiting_overrides = False
    if "pending_replacements" not in st.session_state:
        st.session_state.pending_replacements = None
    if "last_placeholders" not in st.session_state:
        st.session_state.last_placeholders = None
    if "heuristics_only" not in st.session_state:
        st.session_state.heuristics_only = False


def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    return len(api_key.strip()) > 0


def main():
    """Main Streamlit application"""
    initialize_session_state()
    # Load environment variables from .env if present
    load_dotenv()
    env_api_key = os.environ.get("GOOGLE_API_KEY", "")
    
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
            placeholder="Enter your Google Gemini API key",
            value=env_api_key if env_api_key else ""
        )
        
        if api_key and validate_api_key(api_key):
            st.session_state.api_key_set = True
            st.success("✓ API key set")
        else:
            st.session_state.api_key_set = False
            st.warning("⚠️ API key required to proceed")
        st.markdown("---")
        # Allow users to run the app in heuristic-only mode when no API key is available
        heuristics_only = st.checkbox("Heuristics-only mode (no API key required)", value=False)
        st.session_state.heuristics_only = heuristics_only
        
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
                
                # Attempt to extract placeholders via LLM (if API key provided); otherwise fallback to local regex
                placeholders = sorted(st.session_state.template_handler.get_placeholders())
                # If API key is provided, call the LLM to extract placeholders from the template text
                if st.session_state.api_key_set:
                    try:
                        llm = GeminiLLMHandler(api_key)
                        template_text = st.session_state.template_handler.get_template_text()
                        llm_placeholders = llm.extract_template_placeholders(template_text)
                        # Normalize
                        llm_placeholders = sorted({p.upper().strip() for p in llm_placeholders if p})
                        if llm_placeholders:
                            placeholders = llm_placeholders
                            st.info("Placeholders extracted via LLM")
                        else:
                            st.info("LLM did not extract placeholders; using template detection as fallback")
                    except Exception as e:
                        logger.error(f"Error invoking LLM placeholder extraction: {e}")
                        st.info("LLM placeholder extraction failed; using template detection as fallback")

                with st.expander("View Template Placeholders"):
                    st.write(f"**Found {len(placeholders)} placeholder(s):**")
                    st.code("\n".join([f"[{p}]" for p in placeholders]))
                    # update the in-memory placeholders set so downstream code uses the LLM-based placeholders
                    try:
                        st.session_state.template_handler.placeholders = set(placeholders)
                    except Exception:
                        pass
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
                if not st.session_state.api_key_set and not st.session_state.heuristics_only:
                    st.error("❌ Please configure your API key or enable heuristics-only mode in the sidebar first")
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
                                # Create LLM handler - if heuristics-only mode, instantiate without an API key
                                llm = GeminiLLMHandler(api_key if st.session_state.api_key_set else None)
                                # Prefer to pass the placeholders list to the LLM so it extracts only needed keys
                                placeholders_for_extraction = None
                                try:
                                    placeholders_for_extraction = sorted(list(st.session_state.template_handler.get_placeholders()))
                                except Exception:
                                    placeholders_for_extraction = None
                                try:
                                    try:
                                        st.session_state.extracted_data = llm.extract_insurance_data(combined_text, placeholders_for_extraction)
                                    except Exception as e:
                                        # If LLM disabled or fails, try local heuristics fallback
                                        logger.info(f"LLM extraction failed or disabled ({e}). Using heuristics fallback.")
                                        try:
                                            st.session_state.extracted_data = llm._simple_text_extract(combined_text, placeholders_for_extraction)
                                        except Exception:
                                            st.session_state.extracted_data = {}
                                    # If extraction used LLM fallback heuristics, note it in the UI
                                    if isinstance(st.session_state.extracted_data, dict) and st.session_state.extracted_data.get('_llm_fallback'):
                                        st.session_state.llm_fallback = True
                                        # cleanup this helper key
                                        st.session_state.extracted_data.pop('_llm_fallback', None)
                                except Exception as e:
                                    logger.warning(f"LLM extraction with placeholders failed ({e}), retrying without placeholders")
                                    # Fallback: call extraction without placeholders
                                    try:
                                        st.session_state.extracted_data = llm.extract_insurance_data(combined_text, None)
                                    except Exception as e2:
                                        logger.error(f"LLM extraction failed: {e2}")
                                        raise
                                
                                # Generate narratives
                                with st.spinner("Generating narrative text..."):
                                    try:
                                        narratives = llm.generate_narrative(st.session_state.extracted_data)
                                    except Exception:
                                        narratives = {}
                                    st.session_state.extracted_data.update(narratives)
                            
                            st.success("✓ Data extraction complete!")
                            if st.session_state.llm_fallback:
                                st.warning("⚠️ LLM unavailable or rate-limited; using local heuristics as fallback. Some fields may be missing or approximated.")
                            st.session_state.processing_complete = True
                            
                        except Exception as e:
                            st.error("Error during processing. See logs for details.")
                            logger.exception("Processing error")
        
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
                            # Create a temp output, fill it, then copy to workspace for persistent download
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_output:
                                tmp_tmp_path = tmp_output.name

                            # Preferred flow: ask the LLM to produce a strict placeholder->value mapping
                            # then use the original .docx template and `fill_and_save` to preserve formatting.
                            placeholders = sorted(list(st.session_state.template_handler.get_placeholders()))
                            try:
                                llm_for_fill = GeminiLLMHandler(api_key if st.session_state.api_key_set else None)
                                llm_mapping = llm_for_fill.generate_placeholder_mapping(placeholders, st.session_state.extracted_data)

                                # Only use LLM mapping values for placeholders that are non-empty; otherwise fall back to our mapper
                                final_replacements = {}
                                for ph in placeholders:
                                    val = llm_mapping.get(ph, "")
                                    if val is None or val == "":
                                        val = st.session_state.replacements.get(ph, "")
                                    final_replacements[ph] = val

                                # If there are empty placeholders, prompt the user to provide overrides before finalizing
                                empty_placeholders = [p for p, v in final_replacements.items() if not v]
                                if empty_placeholders:
                                    st.session_state.pending_replacements = final_replacements
                                    st.session_state.last_placeholders = placeholders
                                    st.session_state.awaiting_overrides = True
                                    st.info("Some placeholders are missing values. Please provide overrides in the 'Provide Missing Values' panel below and click 'Apply overrides and generate final document'.")
                                    # write mapping report for visibility
                                    try:
                                        mapping_report = mapper.get_mapping_report()
                                        mapping_path = os.path.join(os.getcwd(), "mapping_report.json")
                                        with open(mapping_path, "w", encoding="utf-8") as mr:
                                            json.dump(mapping_report, mr, indent=2)
                                    except Exception:
                                        pass
                                else:
                                    # Fill using the original docx to preserve layout and formatting
                                    st.session_state.template_handler.fill_and_save(final_replacements, tmp_tmp_path)
                            except Exception as e:
                                logger.error(f"LLM placeholder-mapping failed: {e}. Falling back to local replacements.")
                                st.session_state.template_handler.fill_and_save(
                                    st.session_state.replacements,
                                    tmp_tmp_path
                                )

                            # Save mapping report for inspection
                            try:
                                mapping_report = mapper.get_mapping_report()
                                mapping_path = os.path.join(os.getcwd(), "mapping_report.json")
                                with open(mapping_path, "w", encoding="utf-8") as mr:
                                    json.dump(mapping_report, mr, indent=2)
                                logger.info(f"Mapping report saved to {mapping_path}")
                            except Exception as e:
                                logger.error(f"Failed to write mapping report: {e}")

                            # Copy the temp filled doc to a persistent location in the workspace
                            workspace_output = os.path.join(os.getcwd(), "Completed_GLR_Report.docx")
                            try:
                                import shutil
                                shutil.copyfile(tmp_tmp_path, workspace_output)
                            except Exception as e:
                                logger.error(f"Failed to copy filled document to workspace: {e}")

                            # Read the workspace file for download
                            with open(workspace_output, "rb") as f:
                                file_data = f.read()

                            st.success("✓ Document generated successfully! Saved to workspace")

                            # Download button (serves the workspace copy)
                            st.download_button(
                                label="📥 Download Filled Document",
                                data=file_data,
                                file_name="Completed_GLR_Report.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )

                            # Offer mapping report download
                            try:
                                with open(mapping_path, "rb") as mr:
                                    mapping_bytes = mr.read()
                                st.download_button(
                                    label="📄 Download Mapping Report (JSON)",
                                    data=mapping_bytes,
                                    file_name="mapping_report.json",
                                    mime="application/json"
                                )
                            except Exception:
                                pass

                            # Clean up temp file
                            try:
                                os.unlink(tmp_tmp_path)
                            except Exception:
                                pass
                            
                        except Exception as e:
                            st.error(f"Error generating document: {str(e)}")
                            logger.error(f"Generation error: {e}")
            
            with col2:
                if st.button("🔍 View Mapping Report", key="report_btn"):
                    if st.session_state.replacements:
                        st.json(st.session_state.replacements)

            # Render manual override form if the mapping left placeholders empty
            if st.session_state.awaiting_overrides and st.session_state.pending_replacements:
                st.markdown("### ✍️ Provide Missing Values")
                with st.form("overrides_form"):
                    override_inputs = {}
                    for ph, val in sorted(st.session_state.pending_replacements.items()):
                        # show input for placeholders that are empty (but allow editing any)
                        display_val = val if val is not None else ""
                        if not display_val:
                            override_inputs[ph] = st.text_input(f"{ph}", value="", key=f"override_{ph}")
                        else:
                            # still allow user to correct values if desired
                            override_inputs[ph] = st.text_input(f"{ph}", value=display_val, key=f"override_{ph}")

                    submitted = st.form_submit_button("Apply overrides and generate final document")

                if submitted:
                    # Merge overrides into pending_replacements
                    for ph in override_inputs:
                        st.session_state.pending_replacements[ph] = override_inputs[ph]

                    # Perform final fill and save
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_output2:
                            tmp_out_path = tmp_output2.name

                        st.session_state.template_handler.fill_and_save(st.session_state.pending_replacements, tmp_out_path)

                        # Save mapping report
                        try:
                            mapping_report = mapper.get_mapping_report()
                            mapping_path = os.path.join(os.getcwd(), "mapping_report.json")
                            with open(mapping_path, "w", encoding="utf-8") as mr:
                                json.dump(mapping_report, mr, indent=2)
                        except Exception:
                            pass

                        # Copy to workspace
                        workspace_output = os.path.join(os.getcwd(), "Completed_GLR_Report.docx")
                        import shutil
                        shutil.copyfile(tmp_out_path, workspace_output)

                        # Offer download
                        with open(workspace_output, "rb") as f:
                            file_data = f.read()

                        st.success("✓ Document generated with overrides and saved to workspace")
                        st.download_button(
                            label="📥 Download Filled Document",
                            data=file_data,
                            file_name="Completed_GLR_Report.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

                        # Clear override state
                        st.session_state.awaiting_overrides = False
                        st.session_state.pending_replacements = None
                        st.session_state.last_placeholders = None

                        # cleanup
                        try:
                            os.unlink(tmp_out_path)
                        except Exception:
                            pass
                    except Exception as e:
                        st.error(f"Error applying overrides and generating document: {e}")
    
    else:
        st.info("⏳ Please upload both template and photo report(s) to proceed")


if __name__ == "__main__":
    main()
