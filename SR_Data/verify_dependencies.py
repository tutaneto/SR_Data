#!/usr/bin/env python3

import sys
import os
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python version {version.major}.{version.minor} is not supported. Please use Python 3.8 or higher.")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is supported.")
    return True

def check_package(package_name, lib_dir):
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            print(f"❌ Package {package_name} not found.")
            return False

        # Check if package is in lib directory
        package_path = Path(spec.origin)
        lib_path = Path(lib_dir).resolve()
        if not str(package_path).startswith(str(lib_path)):
            print(f"⚠️ Package {package_name} is not installed in the local lib directory.")
            return False

        print(f"✅ Package {package_name} found at {spec.origin}")
        return True
    except ImportError as e:
        print(f"❌ Error importing {package_name}: {e}")
        return False

def check_ffmpeg():
    print("\nChecking ffmpeg installation...")
    ffmpeg_path = os.path.join('bin', 'ffmpeg')
    if not os.path.exists(ffmpeg_path):
        print("❌ ffmpeg not found in bin directory")
        return False

    try:
        subprocess.run([ffmpeg_path, '-version'], capture_output=True, check=True)
        print("✅ ffmpeg is properly installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ ffmpeg installation is broken")
        return False

def check_directories():
    print("\nChecking required directories...")
    required_dirs = ['lib', 'bin', 'data/config', 'graphics', 'videos']
    missing_dirs = []

    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
            print(f"❌ Directory {dir_path} not found")
        else:
            print(f"✅ Directory {dir_path} exists")

    return len(missing_dirs) == 0

def main():
    print("=== SR_Data Dependency Verification ===\n")

    # Get the absolute path to the lib directory
    lib_dir = os.path.abspath('lib')

    # Add lib directory to Python path
    sys.path.insert(0, lib_dir)

    success = True
    success &= check_python_version()

    required_packages = [
        'numpy',
        'pandas',
        'matplotlib',
        'plotly',
        'requests',
        'bs4',
        'selenium',
        'yfinance',
        'moviepy',
        'PIL',
        'telegram',
        'telebot',
        'ipywidgets'
    ]

    print("\nChecking required packages...")
    for package in required_packages:
        success &= check_package(package, lib_dir)

    success &= check_ffmpeg()
    success &= check_directories()

    if success:
        print("\n✅ All dependency checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Some dependency checks failed. Please run setup_local_env.sh to fix issues.")
        sys.exit(1)

if __name__ == '__main__':
    main()
