# GitHub Codespaces - Visual Setup Guide

## 🚀 Three Simple Paths

### PATH 1: I Want to Use Codespaces
```
1. Push code to GitHub
   ↓
2. Click: Code → Codespaces → Create
   ↓
3. Wait 2-3 minutes for environment
   ↓
4. Terminal appears in browser
   ↓
5. Run: streamlit run app.py
   ↓
6. App opens in browser 🎉
```

### PATH 2: I Want to Understand Everything
```
Read in order:
1. START_HERE.md (this repository)
2. GITHUB_UPLOAD_CHECKLIST.md
3. GITHUB_CODESPACES_GUIDE.md
4. glr_pipeline_app/README.md
```

### PATH 3: I'm Ready Now - Just Tell Me Commands
```bash
# Step 1: Initialize locally
cd d:\projects\ProductizeTechnology_Assignment\Task3
git init
git add .
git commit -m "GLR Pipeline"

# Step 2: Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/glr-pipeline.git
git branch -M main
git push -u origin main

# Step 3: Open GitHub in browser
# https://github.com/YOUR_USERNAME/glr-pipeline

# Step 4: Start Codespaces
# Code → Codespaces → Create

# Step 5: In Codespaces terminal
cd glr_pipeline_app
python CODESPACES_SETUP.py
nano .env  # Add your API key
streamlit run app.py
```

---

## 📊 Architecture Diagram

```
YOUR COMPUTER (Local)
    ↓
    ├─→ git init
    ├─→ git add .
    ├─→ git commit
    └─→ git push origin main
         ↓
    GITHUB (Cloud)
         ↓
    Repository Created
         ├─ Code
         ├─ .devcontainer/ (← This is the magic)
         └─ README.md
         ↓
    CODESPACES (Virtual Environment)
         ↓
    Automatic Setup:
         ├─ Linux Container
         ├─ Python 3.12
         ├─ Dependencies
         ├─ VS Code Browser
         └─ Port Forwarding
         ↓
    YOU CAN NOW:
         ├─ Edit files
         ├─ Run Streamlit
         ├─ Process documents
         └─ Download results
```

---

## 🔄 Workflow After Upload

```
You in Codespaces
    ↓
    ├─ Edit .env (add API key)
    ├─ Run: streamlit run app.py
    └─ Browser: http://localhost:8501
         ↓
    Upload template + PDF
         ↓
    Click "Process"
         ↓
    Download output.docx
         ↓
    Done! 🎉
```

---

## ⏱️ Timeline

| Step | Time | What Happens |
|------|------|--------------|
| Push to GitHub | 1 min | Code uploaded |
| Create Codespace | 2-3 min | Environment building |
| Setup (terminal) | 30 sec | Dependencies check |
| Add API key | 1 min | Edit .env |
| Start Streamlit | 1 min | App starting |
| Load in browser | 30 sec | UI ready |
| **TOTAL** | **~8 minutes** | **Ready to use** ✅ |

---

## 🎛️ Control Center

In Codespaces, you have:

```
┌─────────────────────────────────────┐
│  VS Code (Browser)                  │
├─────────────────────────────────────┤
│                                     │
│  File Explorer          Editor      │
│  ├─ glr_pipeline_app   │ cli.py  │
│  ├─ app.py             │ (Code)  │
│  └─ ...                └─────────┘
│                                     │
├─────────────────────────────────────┤
│  Terminal                           │
│  $ python streamlit run app.py      │
│                                     │
│  Web Preview: localhost:8501        │
│  (Streamlit app appears here)       │
└─────────────────────────────────────┘
```

---

## 🔐 API Key - Where Does It Go?

```
SECURITY FLOW
    ↓
Your API Key
    ↓
You paste into .env (in Codespaces only)
    ↓
.gitignore protects it
    ↓
Never sent to GitHub ✓
    ↓
Only used in Codespaces
    ↓
Safe! 🔒
```

---

## 🆘 Troubleshooting Visual

```
Problem                    Solution
─────────────────────────────────────────
Codespace won't start  →  Wait 2-3 min
                          or restart

Port 8501 not working  →  Kill: pkill streamlit
                          Restart app

API key error          →  Check: cat .env
                          Edit: nano .env

Can't see files        →  Refresh browser
                          or reload

App crashes            →  Check terminal
                          See error message
```

---

## 📈 What You Can Do Now

```
✅ Run on any computer (no installation!)
✅ Share with anyone (just GitHub link)
✅ Test new features (in isolation)
✅ Download results (easy right-click)
✅ Scale up easily (more Codespaces)
✅ Keep API key secret (.gitignore)
✅ Auto-test on push (GitHub Actions)
```

---

## 🎯 Checklist Before You Start

- [ ] GitHub account created
- [ ] Repository created on GitHub
- [ ] Local code initialized with git
- [ ] Code pushed to GitHub
- [ ] .env.example in repo (no real key!)
- [ ] .devcontainer/devcontainer.json exists
- [ ] .gitignore file exists

**If all checked:** → You're ready! 🚀

---

## 📞 Quick Reference

**Repository URL:**
```
https://github.com/YOUR_USERNAME/glr-pipeline
```

**Codespaces Start:**
```
Code → Codespaces → Create codespace on main
```

**App Access:**
```
Browser: http://localhost:8501
```

**Terminal Command:**
```bash
streamlit run glr_pipeline_app/app.py
```

---

## 🎓 Learn More

```
GitHub Codespaces Docs:
  https://docs.github.com/en/codespaces

Streamlit Docs:
  https://docs.streamlit.io

Git & GitHub Guide:
  https://guides.github.com
```

---

## 🎉 You're Ready!

Follow these steps:

1. **Save code locally** (already done)
2. **Push to GitHub** (follow checklist)
3. **Open Codespaces** (click 3 buttons)
4. **Run app** (2 commands in terminal)
5. **Process documents** (use the app)
6. **Download results** (right-click download)

**No more local laptop headaches!** ☺️

---

**Need help?** Check: `GITHUB_CODESPACES_GUIDE.md`
