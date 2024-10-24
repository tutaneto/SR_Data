#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)

from libraries.template_config import template_config
from libraries.gvar import gvar
from libraries.drawgraph import draw_graph, symbol_list, get_save_file_name
from libraries.countries import init_countries
from libraries.util import delete_file, send_by_telegram
from libraries.getdata import getdata_init
from libraries.video import create_video
import os
import numpy as np
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go

def setup_test_environment():
    logging.info("Setting up test environment...")
    # Initialize environment
    gvar['ONLINE'] = True
    gvar['is_SR_Data'] = True
    gvar['template_num'] = 1
    gvar['ERROR'] = ''
    gvar['symbol_old'] = 'IPCA'  # Set a default test symbol
    gvar['file_img_to_video'] = 'graphics/temp_video.png'
    gvar['TELEGRAM_SEND'] = False
    gvar['scale'] = 1.0

    # Clean up any existing test files
    for file_pattern in ['graphics/JP_MERC_FIN_IPCA.png', 'graphics/temp_video.png']:
        if os.path.exists(file_pattern):
            os.remove(file_pattern)
            logging.info(f"Cleaned up existing test file: {file_pattern}")

    # Create necessary directories
    for directory in ['graphics', '../wwwsec/output', 'data/digitado', 'data/filter', 'data/config']:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Created directory: {directory}")

    # Create required files
    if not os.path.exists('data/filter/filters.csv'):
        with open('data/filter/filters.csv', 'w') as f:
            f.write('filters;subtit\n')
        logging.info("Created filters.csv with header")

    # Create queue file if it doesn't exist
    queue_file = '../wwwsec/output/queue.txt'
    if not os.path.exists(queue_file):
        with open(queue_file, 'w') as f:
            f.write('')
        logging.info("Created empty queue.txt")

    # Set default template and prepare template settings
    template_config.set_template('JP_MERC_FIN')
    logging.info("Template set to JP_MERC_FIN")

    # Initialize global variables needed for visualization
    global bg_transparent, save_file_scale, df, fig, file_img_to_video, template_num, scale, symbol_old
    bg_transparent = False
    save_file_scale = 3  # Default scale for JP_MERC_FIN template
    fig = go.FigureWidget()
    file_img_to_video = gvar['file_img_to_video']
    template_num = gvar['template_num']
    scale = gvar['scale']
    symbol_old = gvar['symbol_old']

    # Initialize data structures
    df = {}
    getdata_init(df)
    init_countries()
    logging.info("Data structures initialized")

    # Initialize symbol list
    if 'IPCA' not in symbol_list:
        symbol_list.append('IPCA')
        logging.info("Added IPCA to symbol list")

    return True

def test_button_call():
    try:
        from SR_Data import button_call, prepare_template
        logging.info("Starting button call test...")

        # Setup test environment
        if not setup_test_environment():
            raise RuntimeError("Failed to setup test environment")

        # Prepare template (this sets save_file_scale)
        prepare_template(1)  # 1 = JP_MERC_FIN template
        logging.info("Template prepared")

        # Test direct graph generation
        symbol = 'IPCA'
        n_months = 12
        title = 'Test Graph'
        subtit = 'Test Subtitle'
        dfont = None
        bg_transparent = False
        val_col = None

        fig = draw_graph(gvar['scale'], symbol, n_months, title, subtit, dfont, bg_transparent, val_col)
        assert fig is not None, "Graph generation failed"
        logging.info("Graph generated successfully")

        # Test PNG generation through button_call
        result = button_call('1')  # '1' maps to 'PNG'
        assert result is True, "PNG generation failed"

        # Verify output file exists
        expected_file = f'graphics/{template_config.current_template}_{get_save_file_name()}.png'
        assert os.path.exists(expected_file), f"Output file not found: {expected_file}"
        logging.info(f"Successfully generated: {expected_file}")

        print("Button call test successful")
        return True
    except Exception as e:
        logging.error(f"Error in button_call: {str(e)}", exc_info=True)
        return False

if __name__ == '__main__':
    test_button_call()
