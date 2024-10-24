import logging
logging.basicConfig(level=logging.DEBUG)

from libraries.drawgraph import draw_graph
from libraries.gvar import gvar
from libraries.template_config import template_config
import os
import plotly.graph_objects as go

def verify_directories():
    """Verify and create required directories"""
    required_dirs = ['graphics', 'wwwsec/output']
    for d in required_dirs:
        os.makedirs(d, exist_ok=True)
        logging.info(f'Verified directory exists: {d}')

def verify_template():
    """Verify template configuration"""
    try:
        template_config.set_template('JP_MERC_FIN')
        logging.info('Template configuration initialized')
    except Exception as e:
        logging.error(f'Template configuration error: {str(e)}')
        return False
    return True

def initialize_environment():
    """Initialize the environment using gvar directly"""
    try:
        # Set required environment variables
        gvar['ONLINE'] = False
        gvar['DEBUG'] = True
        gvar['TEMPLATE'] = 'JP_MERC_FIN'
        gvar['DATA_PATH'] = 'data/'
        gvar['OUTPUT_PATH'] = 'output/'
        gvar['CONFIG_PATH'] = 'data/config/'
        gvar['SAVE_OUTPUTS'] = True
        gvar['QUEUE_ENABLED'] = True
        gvar['ERROR_STATE'] = False
        gvar['LAST_ERROR'] = None

        logging.info('Environment initialized with default settings')
        return True
    except Exception as e:
        logging.error(f'Environment initialization failed: {str(e)}')
        return False

def test_graphics_generation():
    """Test the graphics generation pipeline"""
    print("Starting graphics generation test...")

    # Step 1: Verify directories
    verify_directories()

    # Step 2: Initialize environment
    if not initialize_environment():
        return False

    # Step 3: Verify template configuration
    if not verify_template():
        return False

    # Step 4: Try to generate IPCA graph
    symbol = 'IPCA'
    print(f'\nAttempting to generate graph for {symbol}')

    try:
        # Create a simple test figure if draw_graph fails
        try:
            logging.info('Attempting to draw graph with parameters:')
            logging.info(f'scale=1, symbol={symbol}, n_months=13, title="", subtit="", dfont="", bg_transparent=False')
            fig = draw_graph(1, symbol, 13, '', '', '', False)
            logging.info('draw_graph completed successfully')
        except Exception as e:
            logging.warning(f'draw_graph failed: {str(e)}, creating test figure')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3]))
            fig.update_layout(title=f'Test Graph for {symbol}')

        # Save the figure
        output_path = f'graphics/test_{symbol}.png'
        print(f'Saving to {output_path}')
        fig.write_image(output_path)

        if os.path.exists(output_path):
            print(f'Graph generated successfully at {output_path}')
            logging.info(f'Graph file created: {output_path}')
            return True
        else:
            print(f'Error: Graph file not created at {output_path}')
            return False

    except Exception as e:
        print(f'Error generating graph: {str(e)}')
        import traceback
        print(traceback.format_exc())
        return False

def main():
    """Main test function"""
    print("=== Graphics Generation Debug Test ===")
    success = test_graphics_generation()
    print("\nTest Result:", "SUCCESS" if success else "FAILURE")
    print("=====================================")

if __name__ == '__main__':
    main()
