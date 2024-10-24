"""
Verify core dependencies are properly installed and functioning.
"""
def verify_dependencies():
    try:
        import pandas
        import numpy
        import matplotlib
        import plotly
        import kaleido
        from PIL import Image
        import requests
        import yfinance

        print("Core dependencies verified successfully:")
        print(f"pandas version: {pandas.__version__}")
        print(f"numpy version: {numpy.__version__}")
        print(f"matplotlib version: {matplotlib.__version__}")
        print(f"plotly version: {plotly.__version__}")
        print(f"PIL version: {Image.__version__}")
        print(f"requests version: {requests.__version__}")
        print(f"yfinance version: {yfinance.__version__}")
        return True
    except ImportError as e:
        print(f"Error importing dependencies: {e}")
        return False

if __name__ == "__main__":
    verify_dependencies()
