from libraries.drawgraph import draw_graph
from libraries.template_config import TemplateConfig
import plotly.io as pio
import os

def test_templates():
    # Ensure test output directory exists
    os.makedirs('test_outputs', exist_ok=True)

    # Test different templates
    templates = ['JP_MERC_FIN', 'INVEST_NEWS_BLACK', 'SBT']
    template_config = TemplateConfig()

    for template in templates:
        print(f"Testing template: {template}")
        template_config.set_template(template)
        fig = draw_graph(1, '^BVSP', 12, 'Test Title', 'Test Subtitle', 'Test Source', False)
        output_path = f'test_outputs/test_{template}.png'
        pio.write_image(fig, output_path)
        print(f"Generated: {output_path}")

if __name__ == '__main__':
    test_templates()
