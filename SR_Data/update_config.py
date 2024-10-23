import json
import shutil
from pathlib import Path

def update_config():
    # Backup existing config
    config_path = Path("data/config/config.json")
    backup_path = Path("data/config/config.json.bak")
    shutil.copy(config_path, backup_path)

    # Read existing config
    with open(config_path) as f:
        existing_config = json.load(f)

    # Create new config structure
    new_config = {
        "apis": {
            "bcb": {
                "base_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.",
                "format": "json",
                "cache_duration": 86400
            },
            "ibge": {
                "base_url": "https://servicodados.ibge.gov.br/api/v3/agregados",
                "pib": existing_config  # Preserve existing PIB configuration
            },
            "fgv": {
                "data_dir": "data/fgv"
            }
        },
        "data_dirs": {
            "bcb": "data/bc",
            "ibge": "data/ibge",
            "fgv": "data/fgv",
            "anbima": "data/anbima",
            "digitado": "data/digitado",
            "filter": "data/filter",
            "mt": "data/mt"
        },
        "cache": {
            "enabled": True,
            "duration": 86400,
            "directory": "data/cache"
        }
    }

    # Write new config
    with open(config_path, "w", encoding='utf-8') as f:
        json.dump(new_config, f, indent=4, ensure_ascii=False)
    print("Configuration updated successfully!")

if __name__ == "__main__":
    update_config()
