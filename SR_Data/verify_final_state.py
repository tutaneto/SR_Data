import sys
sys.path.insert(0, './lib')

def verify_dependencies():
    """Verify all core dependencies are available and working."""
    try:
        import pytest
        import coverage
        import numpy
        import pandas
        import matplotlib
        import plotly
        from PIL import Image

        print("=== Final Verification Results ===")
        print("All core dependencies verified successfully!")
        print("\nProject Status:")
        print("1. ✓ Testing framework (pytest, coverage)")
        print("2. ✓ Data processing (numpy, pandas)")
        print("3. ✓ Visualization (matplotlib, plotly)")
        print("4. ✓ Image processing (PIL)")
        return True
    except ImportError as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    verify_dependencies()
