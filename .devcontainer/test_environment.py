#!/usr/bin/env python3
"""
🧪 Codespaces Quick Test Script
اختبار سريع للتأكد من أن بيئة Codespaces جاهزة للعمل
"""

import sys
import subprocess
from pathlib import Path


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_command(cmd, name):
    """Check if a command exists and get its version"""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=False, shell=True
        )
        if result.returncode == 0:
            version = result.stdout.strip().split("\n")[0]
            print(f"✅ {name}: {version}")
            return True
        else:
            print(f"❌ {name}: Not found or error")
            return False
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False


def check_python_imports():
    """Check if SA modules can be imported"""
    print_header("🐍 Python Imports")
    
    try:
        # Try importing SA modules
        from sa.generators import ImageGenerator, VideoGenerator, AudioGenerator
        print("✅ ImageGenerator imported successfully")
        print("✅ VideoGenerator imported successfully")
        print("✅ AudioGenerator imported successfully")
        
        from sa.utils import SuggestionEngine
        print("✅ SuggestionEngine imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def check_directories():
    """Check if required directories exist"""
    print_header("📁 Directories")
    
    dirs = ["outputs", "logs", "data", "src", "tests"]
    all_exist = True
    
    for dir_name in dirs:
        path = Path(dir_name)
        if path.exists() and path.is_dir():
            print(f"✅ {dir_name}/ exists")
        else:
            print(f"❌ {dir_name}/ missing")
            all_exist = False
    
    return all_exist


def check_files():
    """Check if required files exist"""
    print_header("📄 Important Files")
    
    files = [".env", "pyproject.toml", "poetry.lock", "README.md"]
    all_exist = True
    
    for file_name in files:
        path = Path(file_name)
        if path.exists() and path.is_file():
            print(f"✅ {file_name} exists")
        else:
            print(f"❌ {file_name} missing")
            all_exist = False
    
    return all_exist


def check_poetry_packages():
    """Check installed poetry packages"""
    print_header("📦 Poetry Packages")
    
    try:
        result = subprocess.run(
            ["poetry", "show"],
            capture_output=True,
            text=True,
            check=True
        )
        packages = result.stdout.strip().split("\n")
        print(f"✅ {len(packages)} packages installed")
        
        # Check for key packages
        key_packages = ["fastapi", "streamlit", "replicate", "openai", "pytest"]
        for pkg in key_packages:
            if any(pkg in line for line in packages):
                print(f"  ✅ {pkg}")
            else:
                print(f"  ⚠️  {pkg} not found")
        
        return True
    except Exception as e:
        print(f"❌ Error checking packages: {e}")
        return False


def main():
    """Run all checks"""
    print("\n" + "🚀" * 30)
    print("  SA Codespaces Environment Test")
    print("  اختبار بيئة SA على Codespaces")
    print("🚀" * 30)
    
    results = []
    
    # Check system commands
    print_header("🔧 System Tools")
    results.append(check_command("python --version", "Python"))
    results.append(check_command("poetry --version", "Poetry"))
    results.append(check_command("git --version", "Git"))
    results.append(check_command("ffmpeg -version | head -1", "FFmpeg"))
    
    # Check directories and files
    results.append(check_directories())
    results.append(check_files())
    
    # Check poetry packages
    results.append(check_poetry_packages())
    
    # Check Python imports
    results.append(check_python_imports())
    
    # Summary
    print_header("📊 Summary")
    passed = sum(results)
    total = len(results)
    
    print(f"\n  Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n  ✅ ✅ ✅ All checks passed! Environment is ready! ✅ ✅ ✅")
        print("  🎉 البيئة جاهزة للاستخدام! 🎉")
        print("\n  Next steps:")
        print("    1. Add your API keys to .env file")
        print("    2. Run: make run-ui")
        print("    3. Start building! 🚀")
        return 0
    else:
        print("\n  ⚠️  Some checks failed. Please review the output above.")
        print("  ⚠️  بعض الاختبارات فشلت. راجع النتائج أعلاه.")
        print("\n  Try running:")
        print("    poetry install --no-interaction")
        return 1


if __name__ == "__main__":
    sys.exit(main())
