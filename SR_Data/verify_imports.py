"""
Simple script to verify that all required packages can be imported correctly.
"""
def verify_imports():
    try:
        import pytest
        import _pytest
        import pytest_cov
        import coverage
        print("All packages imported successfully")
        return True
    except ImportError as e:
        print(f"Import failed: {str(e)}")
        return False

if __name__ == "__main__":
    verify_imports()
