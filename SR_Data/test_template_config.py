#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)

from libraries.template_config import template_config
from libraries.gvar import gvar

def test_template_config():
    try:
        # Initialize environment
        gvar['ONLINE'] = True

        # Test template setting
        template_config.set_template('JP_MERC_FIN')
        assert template_config.current_template == 'JP_MERC_FIN', "Template not set correctly"

        # Test template number conversion
        template_num = template_config.get_template_number('JP_MERC_FIN')
        assert template_num == 1, f"Expected template number 1, got {template_num}"

        # Test color retrieval
        color = template_config.get_color('primary')
        assert color is not None, "Failed to retrieve template color"

        print("Template configuration test successful")
        return True
    except Exception as e:
        print(f"Template configuration test failed: {str(e)}")
        return False

if __name__ == '__main__':
    test_template_config()
