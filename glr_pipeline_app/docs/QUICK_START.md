# GLR Pipeline - Setup & Quick Start

## ✅ Current Status

- ✅ Python 3.12 virtual environment created at `.\.venv\`
- ✅ All dependencies installed (streamlit, pdfplumber, python-docx, google-generativeai, python-dotenv)
- ✅ Google Gemini API key configured in `.env`
- ✅ CLI tool ready to use

## 🚀 Quick Start

### Option 1: CLI Mode (Recommended for Work Laptops)

```bash
# Navigate to app folder
cd glr_pipeline_app

# Run with your template and PDF
python cli.py -t template.docx -p report.pdf -o output.docx
```

**Parameters:**
- `-t` or `--template`: Path to .docx template file
- `-p` or `--pdf`: Path to .pdf file (photo report)
- `-o` or `--output`: Output path for filled document

### Example Usage

```bash
python cli.py \
  -t "..\Task 3 - GLR Pipeline\Example 1 - USAA\Input\USAA 800 Claims GLR Template 4-24.docx" \
  -p "..\Task 3 - GLR Pipeline\Example 1 - USAA\Input\photo report.pdf" \
  -o "USAA_filled.docx"
```

## 📁 Project Structure

```
glr_pipeline_app/
├── cli.py                 ← Main CLI tool
├── app.py                 ← Streamlit web app (optional)
├── pdf_extractor.py       ← PDF text extraction
├── llm_handler.py         ← Google Gemini AI integration
├── template_handler.py    ← Word document manipulation
├── data_mapper.py         ← Field mapping logic
├── requirements.txt       ← Python dependencies
├── .env                   ← API configuration (configured)
├── .env.example           ← Environment template
├── README.md              ← Full documentation
└── SETUP.md               ← Detailed setup guide
```

## ⚙️ Configuration

**API Key Setup:**
1. The `.env` file already contains your Google Gemini API key
2. No additional configuration needed
3. To change API key, edit `.env` file

## 🔧 How It Works

1. **Input**: Word template (.docx) + PDF report
2. **Extract**: Text extracted from PDF
3. **Analyze**: Google Gemini AI extracts structured data
4. **Map**: Data automatically mapped to template fields
5. **Generate**: Completed Word document created
6. **Output**: Ready-to-use filled template

## 📋 Features

- ✨ Automatic placeholder detection (`[FIELD_NAME]` format)
- 🤖 AI-powered data extraction
- 🔗 Intelligent field mapping with fuzzy matching
- 📄 Preserves template formatting
- 🚀 Fast processing with Google Gemini

## 🆘 Troubleshooting

**ModuleNotFoundError**
- Make sure virtual environment is activated
- Run: `.\.venv\Scripts\python.exe cli.py -t ... -p ... -o ...`

**API Key Issues**
- Check `.env` file contains valid `GOOGLE_API_KEY`
- Get key from: https://ai.google.dev/

**Permission Denied (Work Laptop)**
- Use full path to Python: `.\.venv\Scripts\python.exe`
- Contact IT if network issues occur

## 📚 More Info

See `README.md` for:
- Full feature documentation
- Supported template placeholders
- Architecture details
- Module documentation
- Examples and use cases

## ✅ Verification

Verify setup is complete:

```bash
cd glr_pipeline_app
.\.venv\Scripts\python.exe -c "import streamlit; import pdfplumber; import docx; import google.generativeai; print('✓ All packages OK')"
```
