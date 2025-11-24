#!/usr/bin/env python3
"""
GLR Pipeline - System Verification Script
Checks that all components are properly installed and configured
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Verify Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_packages():
    """Check all required packages"""
    packages = {
        'streamlit': 'Streamlit',
        'pdfplumber': 'PDF Plumber',
        'docx': 'python-docx',
        'google.generativeai': 'Google Generative AI',
        'dotenv': 'python-dotenv',
        'PIL': 'Pillow'
    }
    
    all_ok = True
    for pkg, display_name in packages.items():
        try:
            __import__(pkg)
            print(f"✓ {display_name} installed")
        except ImportError:
            print(f"✗ {display_name} NOT found")
            all_ok = False
    
    return all_ok

def check_env_file():
    """Check .env configuration"""
    if Path('.env').exists():
        with open('.env', 'r') as f:
            content = f.read()
            if 'GOOGLE_API_KEY' in content:
                print("✓ .env file configured with API key")
                return True
            else:
                print("✗ .env file missing GOOGLE_API_KEY")
                return False
    else:
        print("✗ .env file not found")
        return False

def check_modules():
    """Check custom module files"""
    modules = [
        'pdf_extractor.py',
        'llm_handler.py',
        'template_handler.py',
        'data_mapper.py',
        'cli.py',
        'app.py'
    ]
    
    all_ok = True
    for module in modules:
        if Path(module).exists():
            print(f"✓ {module}")
        else:
            print(f"✗ {module} NOT found")
            all_ok = False
    
    return all_ok

def main():
    print("\n" + "="*50)
    print("  GLR Pipeline - System Verification")
    print("="*50 + "\n")
    
    print("Checking Python Environment:")
    check_python_version()
    print()
    
    print("Checking Installed Packages:")
    pkg_ok = check_packages()
    print()
    
    print("Checking Configuration:")
    env_ok = check_env_file()
    print()
    
    print("Checking Module Files:")
    modules_ok = check_modules()
    print()
    
    if pkg_ok and env_ok and modules_ok:
        print("="*50)
        print("✅ System is ready!")
        print("="*50)
        print("\nUsage:")
        print("  python cli.py -t template.docx -p report.pdf -o output.docx")
        print()
        return 0
    else:
        print("="*50)
        print("❌ Some issues found. See above.")
        print("="*50)
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())
