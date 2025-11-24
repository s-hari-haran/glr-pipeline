# GLR Pipeline - GitHub & Codespaces Setup

## 🚀 Quick Start with GitHub Codespaces

### Step 1: Upload to GitHub

1. **Create a new repository** on GitHub
   - Go to https://github.com/new
   - Name: `glr-pipeline` (or whatever you prefer)
   - Description: "Insurance Template Filler with AI"
   - Public or Private (your choice)
   - Click **Create repository**

2. **Push your code** to GitHub
   ```bash
   cd d:\projects\ProductizeTechnology_Assignment\Task3
   
   # Initialize git (if not already done)
   git init
   git add .
   git commit -m "Initial commit: GLR Pipeline setup"
   
   # Add remote and push
   git remote add origin https://github.com/YOUR_USERNAME/glr-pipeline.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Start Codespaces

1. **Open your GitHub repository**
   - Go to your newly created repo
   
2. **Launch Codespaces**
   - Click the **Code** button (green)
   - Select **Codespaces** tab
   - Click **Create codespace on main**
   - Wait for environment to build (2-3 minutes)

3. **Codespaces will automatically:**
   - Install Python 3.12
   - Install all dependencies from `requirements.txt`
   - Run verification script
   - Open VS Code in browser

### Step 3: Configure API Key

In the Codespaces terminal:

```bash
# Edit .env with your Google API key
nano glr_pipeline_app/.env
```

Add:
```
GOOGLE_API_KEY=your_actual_api_key_here
DEBUG=False
LOG_LEVEL=INFO
```

Save (Ctrl+O, Enter, Ctrl+X)

### Step 4: Run the Application

**Option A: CLI Mode**
```bash
cd glr_pipeline_app
python cli.py -t ../Task\ 3\ -\ GLR\ Pipeline/Example\ 1\ -\ USAA/Input/USAA\ 800\ Claims\ GLR\ Template\ 4-24.docx -p ../Task\ 3\ -\ GLR\ Pipeline/Example\ 1\ -\ USAA/Input/photo\ report.pdf -o output.docx
```

**Option B: Web Mode (Streamlit)**
```bash
cd glr_pipeline_app
streamlit run app.py
```

Codespaces will:
- Detect the port forwarding
- Create a public URL (https://...)
- Show you the link to access the app

### Step 5: Download Results

1. Navigate to the file in Codespaces file explorer
2. Right-click → Download
3. Or use terminal:
   ```bash
   # View available files
   ls glr_pipeline_app/output.docx
   ```

---

## 📁 What Gets Uploaded to GitHub

```
your-repo/
├── glr_pipeline_app/          ← Main application
│   ├── cli.py                 ← CLI tool
│   ├── app.py                 ← Web interface
│   ├── pdf_extractor.py
│   ├── llm_handler.py
│   ├── template_handler.py
│   ├── data_mapper.py
│   ├── requirements.txt
│   ├── .env.example            ← Template (no API key)
│   ├── verify.py
│   ├── CODESPACES_SETUP.py
│   ├── README.md
│   ├── SETUP.md
│   ├── QUICK_START.md
│   └── ARCHITECTURE.md
├── Task 3 - GLR Pipeline/     ← Example data
│   ├── Example 1 - USAA/
│   ├── Example 2 - Wayne-Elevate/
│   └── Example 3 - Guide One - Eberl/
├── .devcontainer/
│   └── devcontainer.json       ← Codespaces config
├── .github/
│   └── workflows/
│       └── test.yml            ← Auto-testing
├── .env.example                 ← Template (copy & edit in Codespaces)
├── requirements.txt
└── README.md
```

---

## ⚙️ Codespaces Environment Details

**Automatically Configured:**
- ✅ Python 3.12
- ✅ All Python packages
- ✅ VS Code extensions (Python, Pylance, Debugger)
- ✅ Port forwarding (8501 for Streamlit)
- ✅ Git configured

**What You Need to Add:**
- ✅ Google Gemini API key in `.env`

---

## 🔑 Getting Your Google API Key

1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create new API key in Google Cloud Console
4. Copy the key
5. Paste into `.env` in Codespaces:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

---

## 🧪 Testing Everything Works

In Codespaces terminal:

```bash
cd glr_pipeline_app

# Run verification
python verify.py

# Or test imports manually
python -c "import streamlit; import pdfplumber; print('✓ OK')"
```

---

## 📤 Download Output Files

After processing templates in Codespaces:

1. **Right-click file in explorer** → Download
2. **Or use terminal**:
   ```bash
   # Copy to a accessible location
   cp output.docx /workspace/glr_pipeline_app/
   ```

---

## 💡 Tips for Codespaces

- **Auto-shutdown**: Codespaces sleeps after 30 mins of inactivity (saves credits)
- **Reconnect**: Just click **Code** → **Codespaces** → your instance
- **Port forwarding**: Streamlit port 8501 is automatically forwarded
- **Free quota**: GitHub gives free Codespaces hours with your account

---

## 🆘 Troubleshooting in Codespaces

**API Key not working:**
```bash
# Check .env is in correct location
cat glr_pipeline_app/.env | grep GOOGLE_API_KEY
```

**Streamlit not loading:**
```bash
# Kill and restart
pkill streamlit
cd glr_pipeline_app && streamlit run app.py
```

**Dependency issues:**
```bash
# Reinstall
pip install --force-reinstall -r glr_pipeline_app/requirements.txt
```

---

## 🎯 Next Steps

1. ✅ Create GitHub repo
2. ✅ Push code
3. ✅ Open Codespaces
4. ✅ Add API key
5. ✅ Run application
6. ✅ Test with examples
7. ✅ Download results
