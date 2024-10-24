import sys
import os

# Add lib directory to Python path
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
sys.path.insert(0, lib_dir)

from libraries.countries import init_countries, idx_country_names

def test_country_initialization():
    try:
        print("Testing country initialization...")
        init_countries()
        print("Country initialization successful!")
        print(f"Number of countries in idx_country_names: {len(idx_country_names)}")
        print("Sample countries:", idx_country_names[:5])
        return True
    except Exception as e:
        print(f"Error during country initialization: {str(e)}")
        return False

if __name__ == '__main__':
    test_country_initialization()
