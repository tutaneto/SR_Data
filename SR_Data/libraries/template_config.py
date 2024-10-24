"""
Centralized template configuration management system.
Replaces scattered template checks with a unified configuration approach.
"""
from typing import Dict, Any, Optional

class TemplateConfig:
    """Manages template-specific configurations and styling."""

    # Base template configurations - will be expanded
    TEMPLATE_CODES = {
        # Numeric template mappings
        1: 'JP_MERC_FIN',
        3: 'INVEST_NEWS_BLACK',
        # Indicator-specific mappings
        'IPCA': 'JP_MERC_FIN',
        'SELIC': 'JP_MERC_FIN',
        'PIB_IBGE': 'JP_MERC_FIN',
        'FOCUS_IPCA': 'JP_MERC_FIN',
        'FOCUS_SELIC': 'JP_MERC_FIN',
        'FOCUS_PIB': 'JP_MERC_FIN',
        'FOCUS_CAMBIO': 'JP_MERC_FIN',
        'IGPM': 'JP_MERC_FIN',
        'IGPDI': 'JP_MERC_FIN',
        'IGP10': 'JP_MERC_FIN',
        'IVAR': 'JP_MERC_FIN',
        'NUCI': 'JP_MERC_FIN',
        'VOL_SERV': 'JP_MERC_FIN',
        'VENDAS_COM': 'JP_MERC_FIN',
        'PROD_IND': 'JP_MERC_FIN'
    }

    TEMPLATE_COLORS = {
        'JP_MERC_FIN': {
            'primary': '#0BD5F9',
            'secondary': '#FF5A5A',
            'background': '#000066',
            'text': '#FFFFFF',
            'bar_positive': '#0BD5F9',
            'bar_negative': '#FF5A5A',
            'title': '#FFFFFF',
            'subtitle': '#CCCCCC'
        },
        'INVEST_NEWS_BLACK': {
            'primary': '#FFFFFF',
            'secondary': '#CCCCCC',
            'background': '#000000',
            'text': '#FFFFFF',
            'bar_positive': '#00FF00',
            'bar_negative': '#FF0000',
            'title': '#FFFFFF',
            'subtitle': '#CCCCCC'
        },
        'SBT': {
            'primary': '#FFB4DC',
            'secondary': '#B74416',
            'background': '#FFFFFF',
            'text': '#000000',
            'bar_positive': '#FFB4DC',
            'bar_negative': '#B74416',
            'title': '#000000',
            'subtitle': '#666666'
        }
    }

    def __init__(self):
        """Initialize with JP_MERC_FIN as the default template."""
        self._current_template = 'JP_MERC_FIN'  # Set default template
        self._template_data = {'colors': self.TEMPLATE_COLORS['JP_MERC_FIN']}

    def set_template(self, template_name: str) -> None:
        """Set the current template and load its configuration."""
        if template_name not in self.TEMPLATE_COLORS:
            raise ValueError(f"Unknown template: {template_name}")
        self._current_template = template_name
        self._template_data = {'colors': self.TEMPLATE_COLORS[template_name]}

    def get_color(self, color_key: str) -> str:
        """Get a color value for the current template."""
        if not self._current_template:
            raise RuntimeError("No template selected")
        return self._template_data['colors'].get(color_key, '#000000')  # Default to black if color not found

    def get_current_template(self) -> str:
        """Get the current template name."""
        return self._current_template

    def get_template_properties(self) -> Dict[str, Any]:
        """Get all properties for the current template."""
        if not self._current_template:
            raise RuntimeError("No template selected")
        return {
            'name': self._current_template,
            'colors': self._template_data['colors'],
            'template_number': self.get_template_number(self._current_template)
        }

    @property
    def current_template(self) -> Optional[str]:
        """Get the name of the current template."""
        return self._current_template

    def get_template_number(self, template_name: str) -> Optional[int]:
        """Convert template name to its corresponding numeric code."""
        # First check if it's already a number
        if isinstance(template_name, int) and template_name in self.TEMPLATE_CODES:
            return template_name
        # Look up template name in TEMPLATE_CODES
        for num, name in self.TEMPLATE_CODES.items():
            if isinstance(num, int) and name == template_name:
                return num
        return None

# Global instance
template_config = TemplateConfig()
# Module-level exports
current_template = template_config.current_template
get_template_config = template_config.get_color
get_template_number = template_config.get_template_number
