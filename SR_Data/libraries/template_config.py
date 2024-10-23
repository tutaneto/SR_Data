"""
Centralized template configuration management system.
Replaces scattered template checks with a unified configuration approach.
"""
from typing import Dict, Any, Optional

class TemplateConfig:
    """Manages template-specific configurations and styling."""

    # Base template configurations - will be expanded
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

    @property
    def current_template(self) -> Optional[str]:
        """Get the name of the current template."""
        return self._current_template

# Global instance
template_config = TemplateConfig()
