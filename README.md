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
# GLR Pipeline

GLR Pipeline automates extracting structured insurance information from photo reports (PDFs) and filling Word (`.docx`) insurance templates. It combines local heuristics with a Google Generative AI (Gemini) LLM integration to extract fields, generate narratives, and map values into your template while preserving layout and formatting.

Repository layout (high level)
- `glr_pipeline_app/` — Streamlit application and core pipeline modules used by the UI.
- `glr_pipeline/` — helper utilities and package layout (legacy/alternate placement).
- `tools/` — developer utilities (e.g., `tools/headless_generate.py` reproduces the pipeline without the UI).
- `project_docs/` — archived top-level documentation (moved from root during cleanup).

Highlights
- PDF text extraction and preprocessing (`pdf_extractor.py`).
- LLM-based extraction and narrative generation (`llm_handler.py`).
- Template parsing and placeholder replacement while preserving formatting (`template_handler.py`).
- Intelligent field mapping with fuzzy matching and address fallback heuristics (`data_mapper.py`).
- UI manual overrides: when the pipeline cannot find values for placeholders, the Streamlit app shows a small form so users can enter missing values before the final document is generated.

Requirements & environment
- Python 3.10+ recommended.
- Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Add your Google Generative AI API key in a `.env` file at the repository root:

```env
GOOGLE_API_KEY=your_api_key_here
# Optional: override the model (default: gemini-2.5-flash)
GLR_LLM_MODEL=gemini-2.5-flash
```

Running the Streamlit app

```bash
python3 -m streamlit run glr_pipeline_app/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

Open `http://0.0.0.0:8501` (use your Codespaces port preview when in Codespaces) and follow the UI:
1. Upload a `.docx` template (placeholders like `[INSURED_NAME]`).
2. Upload one or more photo report PDFs.
3. Click "Process & Extract Data" to run extraction and narrative generation.
4. Review extracted fields and generate the final document. If values are missing, provide overrides in the UI before finalizing.

Headless generator

Use the headless runner for testing without the UI:

```bash
python3 tools/headless_generate.py
```

Output files
- `Completed_GLR_Report.docx` — final generated document (workspace root).
- `mapping_report.json` — audit report showing which placeholders were mapped and which were left unmapped.

Note: local generated artifacts such as `mapping_report.json`, `streamlit.log`, and temporary `.docx` outputs are ignored in `.gitignore` and should not be committed.

Development notes
- The app prefers a strict placeholder->value mapping produced by the LLM (`generate_placeholder_mapping`) and falls back to local heuristics (`DataMapper`) if the LLM leaves values empty.
- Address and mortgage fields can be hit-or-miss because PDF formats vary — the UI manual override or adding regex heuristics in `data_mapper.py` are reliable fixes.
- To change the LLM model, set `GLR_LLM_MODEL` in your environment.

Contributing
- Make changes under `glr_pipeline_app/`, run the headless generator, and validate the Streamlit UI before opening a PR.

If you'd like, I can also:
- Add stronger address heuristics to `data_mapper.py`.
- Add a UI toggle to choose between LLM-only full-fill vs. LLM mapping + manual overrides.
- Clean generated files from the workspace for a tidy working tree.
