import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required graphics-related dependencies are available"""
    required_modules = {
        'plotly': 'For creating interactive visualizations',
        'pandas': 'For data manipulation and analysis',
        'numpy': 'For numerical operations',
        'PIL': 'For image processing',
        'matplotlib': 'For static visualizations'
    }

    missing_modules = []

    print("=== Graphics Dependencies Check ===")
    print(f"Python version: {sys.version}")
    print("\nChecking required modules:")

    for module, purpose in required_modules.items():
        try:
            __import__(module)
            print(f"✓ {module:<12} - {purpose}")
        except ImportError as e:
            missing_modules.append(module)
            print(f"✗ {module:<12} - ERROR: {str(e)}")

    if missing_modules:
        print("\nMissing dependencies:", ", ".join(missing_modules))
        return False

    print("\nAll required graphics dependencies are available.")
    return True

if __name__ == '__main__':
    success = check_dependencies()
    if not success:
        sys.exit(1)
