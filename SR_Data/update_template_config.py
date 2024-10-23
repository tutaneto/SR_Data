import json

def update_template_config():
    config_file = 'data/config/config.json'

    # Read existing config
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Add template configuration
    config['template_num'] = 1  # Using jp_merc_fin template

    # Write updated config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

if __name__ == '__main__':
    update_template_config()
    print("Template configuration updated successfully.")
