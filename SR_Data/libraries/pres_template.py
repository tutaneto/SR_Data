import json
from .gvar import *
from .template_config import template_config, current_template

config_file_name = 'data/config/config.json'

with open(config_file_name, 'r') as fp:
    config_data = json.load(fp)

# Map template codes to module imports
TEMPLATE_MODULES = {
    'JP_MERC_FIN': '.jp_merc_fin',
    'INVEST_NEWS': '.invest_news',
    'INVEST_NEWS_BLACK': '.invest_news_black',
    'NECTON': '.necton',
    'JP_MERC_FIN_2': '.jp_merc_fin_2',
    'JP_IBOPE': '.jp_ibope',
    'JP_MERC_FIN_3': '.jp_merc_fin_3',
    'JP_MERC_FIN_4': '.jp_merc_fin_4',
    'SBT': '.sbt'
}

# Get template from config or gvar
template_name = config_data.get('template', 'JP_MERC_FIN')
template_name = gvar.get('template', template_name)

# Set the template in template_config
template_config.set_template(template_name)

# Import the appropriate template module
if template_name in TEMPLATE_MODULES:
    module_name = TEMPLATE_MODULES[template_name]
    exec(f"from {module_name} import *")
else:
    # Default to JP_MERC_FIN if template not found
    from .jp_merc_fin import *
