# GLR Pipeline - Insurance Template Filler

Automate insurance template filling using photo reports and LLMs via a powerful CLI tool.

## Overview

The GLR (General Loss Report) Pipeline is an intelligent system that:
1. **Extracts** text from insurance photo reports (PDFs)
2. **Analyzes** extracted data using Google Gemini LLM
3. **Maps** extracted information to insurance form fields
4. **Generates** completed insurance templates (.docx files)
5. **Runs** via simple command-line interface

## Features

✨ **Key Capabilities:**
- Upload insurance templates (.docx format) with placeholder fields
- Process multiple photo reports (.pdf format)
- Intelligent data extraction using Google Gemini AI
- Automatic field mapping and template population
- Professional document generation
- Download completed forms

## Requirements

- Python 3.8+
- Google Gemini API key (free tier available)
- 500MB free disk space

## Installation

### 1. Virtual Environment (Already Created)
The virtual environment is at `.\.venv\` with all dependencies installed.

### 2. Get Google Gemini API Key
1. Go to [https://ai.google.dev/](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new API key in your Google Cloud project
4. Copy the API key into `.env` file (replace placeholder)

## Usage

### Running the Application - CLI Mode

Use the command-line interface optimized for all environments:

```bash
python cli.py -t TEMPLATE.docx -p REPORT.pdf -o OUTPUT.docx
```

**Parameters:**
- `-t, --template` : Path to Word template file (.docx)
- `-p, --pdf` : Path to PDF file (photo report, inspection notes)
- `-o, --output` : Output path for filled document (.docx)

### Quick Start Example

```bash
# Test with USAA example
python cli.py \
  -t "..\Task 3 - GLR Pipeline\Example 1 - USAA\Input\USAA 800 Claims GLR Template 4-24.docx" \
  -p "..\Task 3 - GLR Pipeline\Example 1 - USAA\Input\photo report.pdf" \
  -o "USAA_filled.docx"
```

### Step-by-Step Process

**The CLI tool automatically:**
1. Extracts text from the PDF photo report
2. Uses Google Gemini AI to understand claims data
3. Maps extracted data to template fields
4. Fills the Word document
5. Saves the completed document to the output path

**Result:**
- Completed insurance template with all extracted data filled in
- Ready to use or share

## Template Placeholders

Common placeholder fields supported:

| Placeholder | Description | Example |
|-------------|---|---|
| `[DATE_LOSS]` | Date when damage occurred | 2024-11-13 |
| `[INSURED_NAME]` | Property owner name | Richard Daly |
| `[INSURED_H_STREET]` | Street address | 123 Main St |
| `[INSURED_H_CITY]` | City | Houston |
| `[INSURED_H_STATE]` | State | TX |
| `[INSURED_H_ZIP]` | Zip code | 77001 |
| `[DATE_INSPECTED]` | Inspection date | 2024-11-13 |
| `[MORTGAGEE]` | Mortgage company | Bank Name |
| `[TOL_CODE]` | Type of loss | Wind Damage |

## Module Documentation

### `pdf_extractor.py`
Handles PDF text extraction and processing
- `extract_text_from_pdf()` - Extract text from PDF
- `extract_structured_content()` - Extract with metadata

### `llm_handler.py`
Manages Google Gemini API interactions
- `GeminiLLMHandler` - Main LLM interface
- `extract_insurance_data()` - Extract structured data
- `generate_narrative()` - Generate text descriptions

### `template_handler.py`
Handles .docx template parsing and manipulation
- `DocxTemplateHandler` - Template manager
- `get_placeholders()` - Find all field placeholders
- `fill_template()` - Fill template with data
- `fill_and_save()` - Generate output document

### `data_mapper.py`
Maps extracted data to template fields
- `DataMapper` - Maps data to placeholders
- `map_data()` - Perform intelligent mapping
- `get_mapping_report()` - Review mappings

### `app.py`
Main Streamlit web application interface

## File Structure

```
glr_pipeline_app/
├── app.py                 # Main Streamlit application
├── pdf_extractor.py      # PDF text extraction
├── llm_handler.py        # Google Gemini integration
├── template_handler.py   # Word document manipulation
├── data_mapper.py        # Data-to-field mapping
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md            # This file
```

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
GOOGLE_API_KEY=your_api_key_here
DEBUG=False
LOG_LEVEL=INFO
```

### API Key Management

**Security Best Practices:**
- Never hardcode API keys in code
- Use environment variables for sensitive data
- Regenerate keys periodically
- Restrict API key usage in Google Cloud Console

## Supported File Formats

| Format | Purpose | Example |
|--------|---------|---------|
| `.docx` | Insurance template | USAA 800 Claims GLR Template.docx |
| `.pdf` | Photo reports | Photo Report - Damage Assessment.pdf |

## Examples

The workspace includes 3 complete examples:

### Example 1: USAA
- Template: `USAA 800 Claims GLR Template 4-24.docx`
- Photo Report: `photo report.pdf`
- Output: `Completed GLR Word Doc.docx`

### Example 2: Wayne-Elevate
- Template: `Elevate_Wayne Template Report_XM8.docx`
- Photo Report: `Photo Report - 2.pdf`
- Output: `Completed GLR Word Doc-ex2.docx`

### Example 3: Guide One - Eberl
- Template: `Eberl-GuideOne REPORT TEMPLATE_XM8.docx`
- Photo Report: `Photo Report - 3.pdf`
- Output: `Completed GLR Word Doc-ex3.docx`

## Troubleshooting

### API Key Issues
- Ensure API key is correctly entered
- Verify key is active in Google Cloud Console
- Check that free tier limits not exceeded

### PDF Extraction Issues
- Ensure PDF contains extractable text (not scanned images)
- Try a different PDF reader if text extraction fails

### Template Issues
- Verify template uses `[PLACEHOLDER_NAME]` format
- Check that placeholders use only uppercase letters and underscores
- Ensure template is valid `.docx` file

### Document Generation Issues
- Check that all required fields are mapped
- Verify file permissions in output directory
- Ensure sufficient disk space available

## Performance Notes

- Large PDFs (>50MB) may take longer to process
- Multiple PDFs are processed sequentially
- API response time depends on Google Gemini availability
- Document generation is typically very fast

## API Costs

Google Gemini API offers:
- **Free Tier:** 60 requests per minute, daily quota
- **Paid Plans:** Flexible pricing based on usage

Typical costs:
- Data extraction: ~1-2 API calls per document
- All 3 examples: <$0.01 total

## Limitations

1. **Template Structure:** Limited to replacing `[PLACEHOLDER]` fields
2. **Complex Tables:** Placeholders inside table cells may need special handling
3. **Complex Formatting:** Some advanced Word formatting may not be preserved
4. **Data Quality:** Output quality depends on photo report clarity and structure

## Future Enhancements

Potential improvements:
- [ ] Support for nested/complex placeholders
- [ ] Table data extraction and population
- [ ] OCR for scanned documents
- [ ] Batch processing multiple templates
- [ ] Template validation and reporting
- [ ] Support for other LLM providers
- [ ] Document version control
- [ ] User authentication and history

## Support & Issues

For issues or questions:
1. Check the troubleshooting section
2. Review application logs (stderr output)
3. Verify API key and permissions
4. Test with provided examples

## License

This project is part of the ProductizeMe assignment.

## Authors

AI-Assisted Development using Claude Haiku & Google Gemini

---

**Last Updated:** November 2024
**Version:** 1.0
