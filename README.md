# GLR Pipeline - Insurance Template Filler

Automate insurance template filling using AI and photo reports. Built for GitHub Codespaces.

## 🚀 Quick Start (Easiest Way)

### Launch in GitHub Codespaces (No local setup needed!)

1. Click **Code** → **Codespaces** → **Create codespace on main**
2. Wait for environment to build (~2 minutes)
3. In terminal: `cd glr_pipeline_app && python CODESPACES_SETUP.py`
4. Add your Google API key to `.env`
5. Run: `streamlit run app.py` or `python cli.py ...`

**That's it!** Your browser will automatically open with the app.

## 📋 What It Does

Takes:
- 📄 Word template with field placeholders (e.g., `[INSURED_NAME]`)
- 📕 PDF photo report from insurance inspection

Produces:
- ✅ Completed Word document with extracted data

## 🛠️ Local Setup (Windows/Mac/Linux)

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/glr-pipeline.git
cd glr-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r glr_pipeline_app/requirements.txt

# Add API key
# Edit glr_pipeline_app/.env with your Google Gemini API key

# Run
cd glr_pipeline_app
python cli.py -t template.docx -p report.pdf -o output.docx
```

## 📚 Documentation

- **[Codespaces Guide](./GITHUB_CODESPACES_GUIDE.md)** ← Start here for GitHub Codespaces
- **[Quick Start](./glr_pipeline_app/QUICK_START.md)** - CLI usage
- **[Setup Guide](./glr_pipeline_app/SETUP.md)** - Detailed setup
- **[Architecture](./glr_pipeline_app/ARCHITECTURE.md)** - Technical details

## 💻 Usage

### CLI Mode (Recommended)
```bash
python cli.py -t template.docx -p report.pdf -o output.docx
```

### Web Mode (Streamlit)
```bash
streamlit run app.py
```

### Verify Setup
```bash
python verify.py
```

## 🔑 Get API Key

1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create/use API key from Google Cloud Console
4. Add to `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

## 📁 Project Structure

```
glr_pipeline_app/
├── cli.py              ← Main CLI tool
├── app.py              ← Streamlit web interface
├── pdf_extractor.py    ← PDF text extraction
├── llm_handler.py      ← Google Gemini integration
├── template_handler.py ← Word document manipulation
├── data_mapper.py      ← Field mapping logic
├── verify.py           ← Verification script
└── requirements.txt    ← Dependencies
```

## ⚙️ Supported Template Fields

- `[INSURED_NAME]` - Property owner name
- `[POLICY_NUMBER]` - Insurance policy number
- `[CLAIM_NUMBER]` - Claim number
- `[DATE_LOSS]` - Date of loss
- `[ADDRESS_*]` - Address components
- `[ROOF_MATERIAL]` - Roof type
- `[DWELLING_TYPE]` - Property type
- And 20+ more...

## 🧪 Test with Examples

Included example files:
- **Example 1**: USAA template + photo report
- **Example 2**: Wayne-Elevate template
- **Example 3**: Guide One - Eberl template

## 🐛 Troubleshooting

**ModuleNotFoundError**
- Ensure venv is activated
- Run: `pip install -r requirements.txt`

**API Key issues**
- Check `.env` file exists
- Verify key format and validity
- Get new key from https://ai.google.dev/

**Streamlit not loading (local)**
- Kill process: `pkill streamlit`
- Restart: `streamlit run app.py`

## 📊 Features

✨ Automatic placeholder detection
🤖 AI-powered data extraction (Google Gemini)
🔗 Intelligent field mapping with fuzzy matching
📄 Preserves document formatting
🚀 Works offline after API calls complete

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**New to Codespaces?** See [Codespaces Guide](./GITHUB_CODESPACES_GUIDE.md)

**Questions?** Check the documentation files in `glr_pipeline_app/`
