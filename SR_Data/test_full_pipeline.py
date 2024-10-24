import sys
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Add lib directory to Python path
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
sys.path.insert(0, lib_dir)

# Add current directory to Python path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from libraries.countries import init_countries
from libraries.drawgraph import draw_graph
from libraries.graphics import set_graph, set_graph_axes
from libraries.template_config import template_config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_visualization_pipeline():
    try:
        logger.info("1. Initializing country data...")
        init_countries()

        logger.info("2. Creating sample data...")
        # Create sample data for IPCA
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
        values = [5.5, 5.6, 5.4, 5.2, 5.0, 4.8, 4.7, 4.5, 4.3, 4.2, 4.0, 3.8]
        df = pd.DataFrame({'Data': dates, 'Valor': values})

        # Ensure graphics directory exists
        os.makedirs('graphics', exist_ok=True)

        logger.info("3. Setting up template...")
        template_config.set_template('JP_MERC_FIN')

        logger.info("4. Creating figure and setting properties...")
        fig = go.Figure()

        # Set graph properties using template settings
        width = 1700  # Default width
        height = 800  # Default height
        scale = 1.0   # Default scale
        bg_color = template_config.get_color('background')
        font = 'Arial'  # Default font

        set_graph(fig, width, height, scale, bg_color, font)
        set_graph_axes(fig)

        logger.info("5. Attempting to generate graph...")
        result = draw_graph(
            scale=1.0,
            symbol='IPCA',
            n_months=12,
            title='IPCA - Índice Nacional de Preços ao Consumidor Amplo',
            subtit='Variação percentual em 12 meses',
            dfont='Arial',
            bg_transparent=False
        )

        if result:
            logger.info("Graph generation successful!")
            filepath = f'graphics/{template_config.current_template}_IPCA.png'
            logger.info(f"Graph saved to: {filepath}")
            return True
        else:
            logger.error("Graph generation failed!")
            return False

    except Exception as e:
        logger.error(f"Error during visualization pipeline test: {str(e)}")
        return False

if __name__ == '__main__':
    test_visualization_pipeline()
