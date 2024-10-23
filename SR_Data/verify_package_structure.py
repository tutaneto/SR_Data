"""
Script to verify package structure and Python path configuration.
"""
import sys
import os
import importlib.util
from pprint import pprint

def check_package_structure():
    print("Python Path:")
    for path in sys.path:
        print(f"- {path}")

    print("\nChecking for pytest-related packages:")
    packages = ['pytest', '_pytest', 'pytest_cov', 'coverage']
    for package in packages:
        spec = importlib.util.find_spec(package)
        if spec:
            print(f"{package}: Found at {spec.origin}")
        else:
            print(f"{package}: Not found")

    print("\nChecking lib directory structure:")
    lib_dir = os.path.join(os.path.dirname(__file__), 'lib')
    if os.path.exists(lib_dir):
        for root, dirs, files in os.walk(lib_dir):
            if any(name.startswith(('pytest', '_pytest', 'coverage')) for name in dirs + files):
                rel_path = os.path.relpath(root, lib_dir)
                print(f"\nIn {rel_path}:")
                for item in sorted(dirs + files):
                    if item.startswith(('pytest', '_pytest', 'coverage')):
                        print(f"- {item}")

if __name__ == "__main__":
    check_package_structure()
