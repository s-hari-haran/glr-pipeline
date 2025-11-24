#!/usr/bin/env python3
"""
GitHub Codespaces Setup for GLR Pipeline
Run this in Codespaces terminal after environment is created
"""
import os
import sys
from pathlib import Path

def setup_codespaces():
    """Setup GLR Pipeline for GitHub Codespaces"""
    
    print("\n" + "="*60)
    print("  GLR Pipeline - GitHub Codespaces Setup")
    print("="*60 + "\n")
    
    # Change to app directory
    app_dir = Path("glr_pipeline_app")
    if not app_dir.exists():
        print("❌ glr_pipeline_app directory not found")
        return False
    
    os.chdir(app_dir)
    
    # Check .env file
    print("📋 Checking configuration...")
    if not Path(".env").exists():
        print("⚠️  .env file not found")
        print("   Create .env with your Google API key:")
        print("   GOOGLE_API_KEY=your_api_key_here")
        print("   DEBUG=False")
        print("   LOG_LEVEL=INFO")
        
        # Create template
        with open(".env", "w") as f:
            f.write("GOOGLE_API_KEY=your_api_key_here\n")
            f.write("DEBUG=False\n")
            f.write("LOG_LEVEL=INFO\n")
        print("✓ Created .env template (edit with your API key)\n")
    else:
        print("✓ .env file found\n")
    
    # Verify packages
    print("📦 Verifying packages...")
    try:
        import streamlit
        print("✓ Streamlit OK")
    except:
        print("✗ Streamlit missing")
        return False
    
    try:
        import pdfplumber
        print("✓ pdfplumber OK")
    except:
        print("✗ pdfplumber missing")
        return False
    
    try:
        import docx
        print("✓ python-docx OK")
    except:
        print("✗ python-docx missing")
        return False
    
    try:
        import google.generativeai
        print("✓ google-generativeai OK")
    except:
        print("✗ google-generativeai missing")
        return False
    
    try:
        import dotenv
        print("✓ python-dotenv OK")
    except:
        print("✗ python-dotenv missing")
        return False
    
    try:
        import PIL
        print("✓ Pillow OK\n")
    except:
        print("✗ Pillow missing")
        return False
    
    # Success
    print("="*60)
    print("✅ Setup Complete!")
    print("="*60)
    print("\n🚀 Ready to use!\n")
    print("Options:")
    print("  1. CLI Mode:")
    print("     python cli.py -t template.docx -p report.pdf -o output.docx")
    print("\n  2. Web Mode (Streamlit):")
    print("     streamlit run app.py")
    print("\n  3. Verify System:")
    print("     python verify.py")
    print()
    
    return True

if __name__ == "__main__":
    success = setup_codespaces()
    sys.exit(0 if success else 1)
