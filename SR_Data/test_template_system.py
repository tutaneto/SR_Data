import logging
import os
from libraries.gvar import gvar
from libraries.template_config import template_config
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def verify_template_files():
    """Verify template configuration files exist and are valid"""
    config_path = os.path.join(gvar['CONFIG_PATH'], 'templates.json')
    if not os.path.exists(config_path):
        logger.error(f"Template configuration file not found at {config_path}")
        return False

    try:
        with open(config_path, 'r') as f:
            templates = json.load(f)
        logger.info(f"Found {len(templates)} template configurations")
        return True
    except Exception as e:
        logger.error(f"Error reading template configuration: {str(e)}")
        return False

def test_template_initialization():
    """Test template configuration initialization"""
    try:
        # Initialize with default template
        template_config.set_template('JP_MERC_FIN')
        current_template = template_config.get_current_template()
        logger.info(f"Current template: {current_template}")

        # Verify template properties
        properties = template_config.get_template_properties()
        logger.info(f"Template properties: {properties}")

        return True
    except Exception as e:
        logger.error(f"Template initialization failed: {str(e)}")
        return False

def main():
    print("=== Template System Test ===")

    # Step 1: Verify template files
    if not verify_template_files():
        return False

    # Step 2: Test template initialization
    if not test_template_initialization():
        return False

    print("\nTemplate system test completed successfully")
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        exit(1)
