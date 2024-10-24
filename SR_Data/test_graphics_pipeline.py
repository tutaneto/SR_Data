import os
import logging
from libraries.gvar import gvar
from libraries.template_config import template_config
from libraries.drawgraph import draw_graph
from libraries.getdata import getdata_init
from libraries.util import init_countries
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Initialize global data structures
df = {}
getdata_init(df)
init_countries()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initialize_environment():
    """Initialize required global variables and environment"""
    # Set offline mode and other required globals
    gvar['ONLINE'] = False
    gvar['DEBUG'] = True
    gvar['decimal'] = 2
    gvar['ERROR_STATE'] = False
    gvar['LAST_ERROR'] = None
    gvar['template_num'] = 1  # Default template number

    # Create required directories
    required_dirs = [
        'graphics',
        'data/out',
        'data/digitado',
        'data/config',
        'data/filter'
    ]
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

def create_test_data():
    """Create sample data for testing graphics generation"""
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    values = np.random.normal(100, 10, size=len(dates))
    df = pd.DataFrame({
        'Data': dates,
        'Valor': values
    })
    return df

def test_graphics_generation():
    """Test the complete graphics generation pipeline"""
    print("\n=== Graphics Pipeline Test ===")

    try:
        # Initialize environment
        initialize_environment()

        # Initialize template
        template_config.set_template('JP_MERC_FIN')
        logger.info("Template initialized: %s", template_config.get_current_template())

        # Verify data initialization
        if not df:
            logger.error("Global data dictionary is empty")
            return False

        logger.info("Checking symbol_list availability...")
        from libraries.drawgraph import symbol_list
        if 'IPCA' not in symbol_list:
            logger.error("Required symbol 'IPCA' not found in symbol_list")
            return False
        logger.info("Symbol 'IPCA' found in symbol_list")

        # Set up graph parameters matching draw_graph interface
        scale = 1.0
        symbol = 'IPCA'
        n_months = 12
        title = symbol_list[symbol]['title'] if symbol in symbol_list else 'IPCA'
        subtit = symbol_list[symbol]['subtit'] if symbol in symbol_list else ''
        dfont = symbol_list[symbol]['dfont'] if symbol in symbol_list else None
        bg_transparent = False
        val_col = None

        # Generate graph
        try:
            fig = draw_graph(
                scale=scale,
                symbol=symbol,
                n_months=n_months,
                title=title,
                subtit=subtit,
                dfont=dfont,
                bg_transparent=bg_transparent,
                val_col=val_col
            )
        except Exception as draw_error:
            logger.error("Error in draw_graph: %s", str(draw_error))
            return False

        if fig is not None:
            output_path = f'graphics/IPCA_test.png'
            fig.write_image(output_path)
            if os.path.exists(output_path):
                logger.info("Graph generated successfully at: %s", output_path)
                return True

        logger.error("Failed to generate graph")
        return False

    except Exception as e:
        logger.error("Error in graphics pipeline: %s", str(e))
        return False

def main():
    success = test_graphics_generation()
    if success:
        print("\nGraphics pipeline test completed successfully")
        return 0
    else:
        print("\nGraphics pipeline test failed")
        return 1

if __name__ == '__main__':
    exit(main())
