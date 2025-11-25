# GLR Pipeline - Development & Architecture Document

## Project Overview

The **GLR (General Loss Report) Pipeline** is an intelligent automation system that fills insurance claim templates using data extracted from photo reports via LLM analysis.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                      │
│                         (app.py)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Upload     │  │   Upload     │  │  API Config  │           │
│  │  Template    │  │ Photo Report │  │    Setup     │           │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘           │
│         │                 │                                      │
└─────────┼─────────────────┼──────────────────────────────────────┘
          │                 │
          ▼                 ▼
    ┌──────────────┐  ┌──────────────────┐
    │ Template     │  │ PDF Extractor    │
    │ Handler      │  │ (pdf_extractor)  │
    │ (template_   │  │                  │
    │  handler)    │  │ Extracts text    │
    └──────────────┘  │ from PDF files   │
          │           └─────────┬────────┘
          │                     │
          │    Combined Text    ▼
          │                ┌────────────────────┐
          │                │  LLM Handler       │
          │                │  (llm_handler)     │
          │                │                    │
          │                │ Google Gemini API  │
          │                └────────┬───────────┘
          │                         │
          │      Extracted Data     ▼
          │              ┌─────────────────────┐
          │              │  Data Mapper        │
          │              │  (data_mapper)      │
          │              │                     │
          │              │ Maps to fields      │
          │              └──────┬──────────────┘
          │                     │
          └─────────────────────┼───────┐
                                ▼       ▼
                    Template  Replacements
                    Handler   Data
                         │       │
                         └───┬───┘
                             ▼
                    ┌─────────────────────┐
                    │  Fill Template      │
                    │  & Generate .docx   │
                    └──────┬──────────────┘
                           │
                           ▼
                    ┌─────────────────────┐
                    │  Download Ready     │
                    │  Document           │
                    └─────────────────────┘
```

## Module Documentation

### 1. **app.py** - Main Streamlit Application

**Purpose:** Web interface for the GLR Pipeline

**Key Responsibilities:**
- Manage user input (file uploads, API key)
- Orchestrate workflow (extract → analyze → fill → download)
- Display progress and results
- Handle file I/O and session state

**Main Components:**
```python
initialize_session_state()      # Setup session variables
validate_api_key()              # Verify API key format
main()                          # Main UI logic
```

**Workflow:**
1. Sidebar: API key configuration
2. Column 1: Template upload & placeholder detection
3. Column 2: Photo report upload
4. Processing section: Data extraction & document generation

**Key Features:**
- Real-time progress updates
- Data preview tabs (structured/raw)
- Mapping report visualization
- One-click download

---

### 2. **pdf_extractor.py** - PDF Text Extraction

**Purpose:** Extract and process text from PDF files

**Key Functions:**

```python
extract_text_from_pdf(pdf_path: str) -> str
    Extract all text from PDF
    - Iterates through all pages
    - Handles text encoding
    - Returns combined text

extract_text_with_confidence(pdf_path: str) -> Tuple[str, List[Dict]]
    Extract text with metadata
    - Page count, dimensions, success status
    - Useful for validation

extract_structured_content(pdf_path: str) -> Dict
    Extract with full metadata
    - Raw text + page info
    - Extraction success flag
```

**Error Handling:**
- Handles corrupted PDFs gracefully
- Logs page-by-page extraction
- Returns empty string for non-text PDFs

---

### 3. **llm_handler.py** - LLM Integration

**Purpose:** Manage Google Gemini API interactions

**Key Class: GeminiLLMHandler**

```python
__init__(api_key: str)
    Initialize with Google Gemini API key
    Configure model: 'gemini-2.5-flash'

extract_insurance_data(photo_report_text: str) -> Dict
    Extract structured data from photo report text
    Returns dictionary with fields:
    - insured_name, policy_number, claim_number
    - address components (street, city, state, zip)
    - dwelling details (type, roof, age)
    - damage descriptions by elevation
    - type of loss, summary, notes

generate_narrative(extracted_data: Dict) -> Dict
    Generate professional text for template sections
    Returns descriptions for:
    - Dwelling, property condition, roof
    - Each elevation, interior, damage summary
```

**Prompting Strategy:**
- Provides structured JSON schema for responses
- Includes fallback parsing for malformed responses
- Adds markdown cleanup for API responses

**Error Handling:**
- JSON parsing with fallback mechanism
- Detailed error logging
- Validates response structure

---

### 4. **template_handler.py** - Document Manipulation

**Purpose:** Parse and fill .docx templates

**Key Class: DocxTemplateHandler**

```python
__init__(docx_path: str)
    Load template and extract placeholders
    Auto-discovers all [PLACEHOLDER] fields

get_placeholders() -> Set[str]
    Return all placeholder names found
    
fill_template(replacements: Dict) -> Document
    Fill template with data
    Returns new Document object
    
fill_and_save(replacements: Dict, output_path: str) -> bool
    Generate filled document and save
    
get_placeholder_mapping_template() -> Dict
    Get template dict for reference
```

**Placeholder Pattern:**
```regex
\[([A-Z_0-9]+)\]   # Matches [PLACEHOLDER_NAME]
```

**Features:**
- Searches paragraphs AND tables
- Preserves document formatting
- Deep copy to avoid modifying original
- Supports multiple replacements

---

### 5. **data_mapper.py** - Field Mapping

**Purpose:** Intelligently map extracted data to template fields

**Key Class: DataMapper**

```python
__init__(extracted_data: Dict, template_placeholders: set)
    Initialize with data and template structure

map_data() -> Dict[str, str]
    Map extracted fields to template placeholders
    - Direct mapping (DEFAULT_MAPPING)
    - Fuzzy matching (field name similarity)
    - Returns ready-to-use replacements

get_mapping_report() -> Dict
    Report showing:
    - Total vs mapped placeholders
    - Which fields were unmapped
    - What values used for each
```

**Mapping Rules:**
```python
DEFAULT_MAPPING = {
    "DATE_LOSS": "date_of_loss",
    "INSURED_NAME": "insured_name",
    "INSURED_H_STREET": "address_street",
    # ... more mappings
}
```

**Mapping Strategy:**
1. Direct mapping using DEFAULT_MAPPING
2. Fuzzy matching on lowercase field names
3. Return None for unmapped fields (preserved as-is)

---

## Data Flow

### Complete Processing Pipeline

```
INPUT PHASE
│
├─ Upload Template (.docx)
│  └─ Load & detect placeholders
│
├─ Upload Photo Report(s) (.pdf)
│  └─ Validate file format
│
└─ Configure API Key
   └─ Validate key format

EXTRACTION PHASE
│
├─ PDF Text Extraction
│  └─ pdf_extractor.extract_text_from_pdf()
│  └─ Combine multiple PDFs
│
├─ LLM Analysis
│  └─ llm_handler.extract_insurance_data()
│  └─ Send to Google Gemini API
│  └─ Parse JSON response
│
└─ Narrative Generation
   └─ llm_handler.generate_narrative()
   └─ Create professional text descriptions

MAPPING PHASE
│
├─ Template Analysis
│  └─ Identify all placeholders
│
├─ Data Mapping
│  └─ data_mapper.map_data()
│  └─ Match extracted fields to placeholders
│
└─ Mapping Report
   └─ Report mapped vs unmapped fields

GENERATION PHASE
│
├─ Fill Template
│  └─ template_handler.fill_template()
│  └─ Replace all placeholders
│  └─ Preserve formatting
│
├─ Save Document
│  └─ Save as .docx file
│
└─ Download
   └─ User downloads completed form

OUTPUT
│
└─ Completed_GLR_Report.docx
```

---

## Key Design Decisions

### 1. **Modular Architecture**
Each component has a single responsibility:
- `pdf_extractor.py` - Only text extraction
- `llm_handler.py` - Only LLM communication
- `template_handler.py` - Only document manipulation
- `data_mapper.py` - Only field mapping
- `app.py` - Only UI orchestration

**Benefits:**
- Easy to test individually
- Easy to replace components
- Easy to extend/modify

### 2. **Stateless LLM Calls**
LLM is called with complete context, not expecting memory:
- Always provide full photo report text
- Always provide complete extraction instructions
- No conversation history maintained

**Benefits:**
- Predictable behavior
- No context leakage between requests
- Simpler error recovery

### 3. **Conservative Data Mapping**
Only fills fields with high-confidence matches:
- Direct mapping uses defined dictionary
- Fuzzy matching on field name similarity
- Leaves unknown fields blank (not filled)

**Benefits:**
- Prevents incorrect data in forms
- Forces user review of unmapped fields
- Maintains form integrity

### 4. **Document Preservation**
Deep copy template before modification:
- Original template unchanged
- Safe for batch processing
- Can regenerate documents

**Benefits:**
- No side effects
- Can process template multiple times
- Can compare versions

---

## API Integration Strategy

### Google Gemini API

**Model Used:** `gemini-2.5-flash`

**Prompting Approach:**

```
1. System Role: "You are an insurance claims adjuster"
2. Task: "Extract data from photo report"
3. Expected Output: "Return ONLY valid JSON with these fields..."
4. Input Data: "Here is the photo report text..."
```

**Response Handling:**
- Expect JSON object in response
- Clean markdown wrappers (```json```)
- Parse JSON with error fallback
- Log failures for debugging

**Error Recovery:**
- If JSON parsing fails, use fallback parser
- Extract as much as possible from malformed response
- Log original response for review

---

## Configuration & Deployment

### Environment Variables

```env
GOOGLE_API_KEY=<your-api-key>
DEBUG=False
LOG_LEVEL=INFO
```

### Streamlit Configuration

Optional `~/.streamlit/config.toml`:
- Theme colors
- Client settings
- Logger configuration
- Server settings

### Security Considerations

1. **API Keys:**
   - Never hardcode
   - Passed via environment or UI input
   - Validated before use

2. **File Uploads:**
   - Temporary file handling
   - Cleanup after processing
   - Size limits enforced

3. **Output Documents:**
   - Generated in temp directory
   - User downloads immediately
   - Not persisted on server

---

## Testing Strategy

### Unit Tests (Suggested)

```python
# Test PDF extraction
test_extract_text_simple_pdf()
test_extract_text_complex_pdf()
test_extract_text_corrupted_pdf()

# Test template parsing
test_find_single_placeholder()
test_find_multiple_placeholders()
test_preserve_document_formatting()

# Test data mapping
test_direct_mapping()
test_fuzzy_matching()
test_unmapped_fields()

# Test document generation
test_fill_single_field()
test_fill_multiple_fields()
test_output_file_validity()
```

### Integration Tests (Suggested)

```python
# Test complete workflow
test_example_1_usaa()
test_example_2_wayne_elevate()
test_example_3_guide_one()

# Test edge cases
test_large_photo_report()
test_multiple_pdfs()
test_missing_fields()
test_invalid_template()
```

---

## Performance Considerations

### Bottlenecks
1. **PDF Extraction:** 1-5s per PDF (size dependent)
2. **LLM API Call:** 5-15s (network latency)
3. **Document Generation:** <1s (local)

### Optimization Opportunities
- Parallel PDF extraction (multi-threading)
- Batch multiple extractions per API call
- Cache template parsing results
- Stream large responses

### Scalability Notes
- Current design: Single-threaded, one user at a time
- For production: Add request queuing
- Consider API rate limiting (60 req/min free tier)

---

## Future Enhancements

### Short Term
- [ ] Support for more document types (.pdf forms)
- [ ] Template validation before processing
- [ ] Data preview and editing UI
- [ ] Batch processing multiple templates

### Medium Term
- [ ] User authentication and history
- [ ] Template library/management
- [ ] Advanced field mapping rules
- [ ] OCR for scanned PDFs

### Long Term
- [ ] Support for other LLM providers
- [ ] Document version control
- [ ] Workflow automation
- [ ] Mobile app support

---

## Deployment Notes

### Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Docker Deployment (Future)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

### Cloud Deployment (Future)
- Streamlit Cloud (built-in support)
- AWS Lambda (serverless)
- Google Cloud Run (containerized)

---

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "API key not recognized" | Invalid key format | Verify in Google Cloud Console |
| "PDF text not extracted" | Scanned image | Use OCR service or different PDF |
| "Template not loading" | Invalid .docx format | Resave in MS Word 2010+ |
| "Module not found" | Not in virtual environment | Run `activate` script |
| "API rate limit exceeded" | Free tier limit (60/min) | Wait before retrying |

### Debug Logging

Enable debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View logs:
- Streamlit terminal output
- Application error messages
- Module-level debug statements

---

## Documentation Files

1. **README.md** - User guide & feature overview
2. **SETUP.md** - Installation & configuration
3. **QUICKSTART.py** - Interactive quick start guide
4. **ARCHITECTURE.md** - This file
5. **validate.py** - System validation script

---

**Version:** 1.0  
**Last Updated:** November 2024  
**Author:** AI-Assisted Development
