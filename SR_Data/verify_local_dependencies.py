"""
Verify local dependencies for SR_Data
Ensures all required packages are installed locally and accessible
"""
import os
import sys
import importlib
import subprocess
from pathlib import Path

def verify_local_package(package_name):
    """Verify a package is installed locally"""
    try:
        # Add lib directory to Python path
        lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
        sys.path.insert(0, lib_path)

        # Handle package name variations
        package_variations = [
            package_name,
            package_name.replace('-', '_'),
            package_name.split('-')[0]
        ]

        # Try importing the package with different name variations
        for pkg_name in package_variations:
            try:
                importlib.import_module(pkg_name)
                print(f"✓ {package_name} verified")
                return True
            except ImportError:
                continue

        print(f"✗ {package_name} not found locally (tried variations: {', '.join(package_variations)})")
        return False
    except Exception as e:
        print(f"✗ Error verifying {package_name}: {str(e)}")
        return False

def verify_server_dependencies():
    """Verify server management specific dependencies"""
    package_mapping = {
        'pytest': ['pytest', '_pytest'],
        'pytest-cov': ['pytest_cov', 'pytest.cov', 'pytest.plugins.cov', 'pytest_cov.plugin'],
        'coverage': ['coverage']
    }

    all_verified = True
    print("\nVerifying server dependencies:")
    for package, module_names in package_mapping.items():
        verified = False
        error_msg = ""
        for module_name in module_names:
            try:
                __import__(module_name)
                verified = True
                print(f"✓ {package} verified")
                break
            except ImportError as e:
                error_msg = str(e)
                continue
        if not verified:
            print(f"✗ {package} not found locally: {error_msg}")
            all_verified = False

    return all_verified

def verify_project_structure():
    """Verify required project directories exist"""
    required_dirs = [
        'lib',
        'libraries',
        'graphics',
        '../wwwsec/output'
    ]

    all_verified = True
    for directory in required_dirs:
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)
        if not os.path.exists(dir_path):
            print(f"✗ Required directory missing: {directory}")
            all_verified = False
        else:
            print(f"✓ Directory verified: {directory}")

    return all_verified

def verify_queue_file():
    """Verify queue file exists and is writable"""
    queue_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../wwwsec/output/queue.txt')
    try:
        if not os.path.exists(queue_file):
            with open(queue_file, 'w') as f:
                f.write('0 0\n')
        print("✓ Queue file verified")
        return True
    except Exception as e:
        print(f"✗ Queue file verification failed: {str(e)}")
        return False

def main():
    """Main verification process"""
    print("Verifying SR_Data local dependencies...")

    # Verify project structure
    print("\nVerifying project structure:")
    structure_verified = verify_project_structure()

    # Verify server dependencies
    print("\nVerifying server dependencies:")
    deps_verified = verify_server_dependencies()

    # Verify queue file
    print("\nVerifying queue file:")
    queue_verified = verify_queue_file()

    # Final status
    if structure_verified and deps_verified and queue_verified:
        print("\n✓ All verifications passed")
        return 0
    else:
        print("\n✗ Some verifications failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
