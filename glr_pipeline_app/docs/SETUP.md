# GLR Pipeline - Setup & Configuration Guide

## System Requirements

- **OS:** Windows, macOS, or Linux
- **Python:** 3.8 or later
- **RAM:** 2GB minimum (4GB recommended)
- **Disk Space:** 500MB
- **Internet:** Required for API calls

## Installation Steps

### 1. Download & Navigate to Project

```bash
# Navigate to the glr_pipeline_app directory
cd d:\projects\ProductizeTechnology_Assignment\Task3\glr_pipeline_app
```

### 2. Set Up Python Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web framework
- `python-docx` - Word document manipulation
- `pdfplumber` - PDF text extraction
- `google-generativeai` - Google Gemini API
- `python-dotenv` - Environment configuration
- `pillow` - Image processing

### 4. Get Google Gemini API Key

**Step 1: Visit Google AI Studio**
- Go to https://ai.google.dev/

**Step 2: Create/Get API Key**
- Click "Get API Key" in the top-right
- Or go to https://aistudio.google.com/app/apikey
- Sign in with your Google account

**Step 3: Create New API Key**
- If you don't have a project, create one
- Click "Create API Key"
- Select or create a project
- Copy the generated API key

**Step 4: Verify Free Tier**
- Free tier includes 60 requests/minute
- Daily quota limits apply
- Sufficient for testing and moderate use

### 5. Configure Environment (Optional)

Create a `.env` file for local development:

```bash
# Copy template
cp .env.example .env

# Edit .env and add your API key
GOOGLE_API_KEY=your_key_here
```

Note: In Streamlit app, API key is entered via UI (more secure than .env)

### 6. Run the Application

**Option A: Using launcher script (Windows)**
```cmd
run.bat
```

**Option B: Using launcher script (macOS/Linux)**
```bash
chmod +x run.sh
./run.sh
```

**Option C: Direct Streamlit launch**
```bash
streamlit run app.py
```

The application will:
- Install dependencies if needed
- Start the Streamlit server
- Open browser to http://localhost:8501

## Directory Structure

```
glr_pipeline_app/
├── app.py                      # Main Streamlit application
├── pdf_extractor.py           # PDF extraction utilities
├── llm_handler.py             # Google Gemini API handler
├── template_handler.py        # Word document manipulation
├── data_mapper.py             # Data field mapping
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── run.bat                   # Windows launcher
├── run.sh                    # macOS/Linux launcher
├── QUICKSTART.py             # Quick start guide
├── SETUP.md                  # This file
└── README.md                 # Full documentation
```

## Dependency Details

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web application framework |
| python-docx | 0.8.11 | Create/edit Word documents |
| pdfplumber | 0.10.3 | Extract text from PDFs |
| google-generativeai | 0.3.0 | Google Gemini API client |
| python-dotenv | 1.0.0 | Environment configuration |
| pillow | 10.0.0 | Image processing |

## Configuration Options

### Streamlit Config (optional)

Create `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[logger]
level = "info"

[server]
maxUploadSize = 200
enableXsrfProtection = true
```

### API Key Management

**Best Practices:**
1. Never commit API keys to version control
2. Use environment variables or `.env` files
3. Regenerate keys periodically
4. Restrict API usage in Google Cloud Console
5. Monitor API usage on Google AI dashboard

**In Google Cloud Console:**
1. Go to console.cloud.google.com
2. Select your project
3. API & Services > Credentials
4. View API key restrictions:
   - HTTP referrers (restrict to your domain)
   - API restrictions (allow only Generative Language API)

## First Run Checklist

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list | grep streamlit`)
- [ ] Google Gemini API key obtained
- [ ] Able to access http://localhost:8501
- [ ] Template files available (.docx format)
- [ ] Photo reports available (.pdf format)

## Verification Steps

### Test PDF Extraction
```python
from pdf_extractor import extract_text_from_pdf
text = extract_text_from_pdf("example.pdf")
print(text[:200])  # Should print first 200 chars
```

### Test Template Parsing
```python
from template_handler import DocxTemplateHandler
handler = DocxTemplateHandler("template.docx")
print(handler.get_placeholders())  # Should list all placeholders
```

### Test LLM Connection
```python
from llm_handler import GeminiLLMHandler
llm = GeminiLLMHandler("your_api_key")
# Will raise error if key invalid
```

## Troubleshooting

### Python Not Found
```
Error: 'python' is not recognized
```
Solution:
- Add Python to PATH
- Use `python3` instead of `python`
- Reinstall Python with "Add to PATH" option

### Module Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
Solution:
- Activate virtual environment
- Run `pip install -r requirements.txt`
- Check pip is using correct Python: `pip --version`

### Streamlit Port Already in Use
```
Error: Address already in use
```
Solution:
```bash
# Kill existing process or use different port
streamlit run app.py --server.port 8502
```

### API Key Errors
```
Error: Invalid API key
```
Solution:
- Verify key is correctly copied (no leading/trailing spaces)
- Check free tier quota not exceeded
- Regenerate key in Google Cloud Console
- Verify API is enabled in project

### PDF Extraction Issues
```
Text not extracted from PDF
```
Solution:
- Ensure PDF has extractable text (not image scan)
- Try opening PDF with another reader
- Validate PDF file: `pdfplumber.open("file.pdf")`

### Document Generation Fails
```
Error: Cannot save document
```
Solution:
- Check output directory permissions
- Ensure sufficient disk space
- Verify template is valid .docx
- Check placeholders use [UPPERCASE] format

## Performance Optimization

### For Large Documents
```python
# Set higher timeout for large PDFs
import pdfplumber
pdfplumber.open(path).metadata  # Check before processing
```

### For Multiple PDFs
- Process sequentially (default)
- Combine text before sending to LLM
- Use shorter prompts for faster responses

### API Rate Limiting
- Free tier: 60 requests/minute
- Add delays between requests if needed
- Monitor quota in Google AI Studio

## Updating Dependencies

Check for updates:
```bash
pip list --outdated
```

Update all packages:
```bash
pip install --upgrade -r requirements.txt
```

Update specific package:
```bash
pip install --upgrade streamlit
```

## Security Considerations

1. **API Keys:**
   - Never hardcode in source files
   - Never commit to version control
   - Store in environment variables

2. **User Data:**
   - Uploaded files processed locally
   - Only document content sent to API
   - No data persistence by default

3. **Streamlit Security:**
   - CSRF protection enabled
   - Run on localhost by default
   - Use HTTPS when deploying

## Deployment Notes

For production deployment:

1. Use environment variables for API keys
2. Set `logger.level = "warning"`
3. Enable XSRF protection
4. Restrict file upload sizes
5. Use reverse proxy (nginx)
6. Enable HTTPS
7. Monitor API usage and costs

## Support Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **python-docx Docs:** https://python-docx.readthedocs.io/
- **pdfplumber Docs:** https://github.com/jsvine/pdfplumber
- **Google Gemini API:** https://ai.google.dev/docs/
- **Python Docs:** https://docs.python.org/3/

## Getting Help

1. Check README.md for general information
2. Review docstrings in Python files
3. Enable debug logging for detailed info
4. Test with provided examples first
5. Check GitHub issues or documentation

---

**Last Updated:** November 2024
**Version:** 1.0
