import importlib
from .util import save_error

templates = ['', 'jp_merc_fin', 'invest_news', 'invest_news_black', 'necton', 'jp_merc_fin_2', 'jp_ibope', 'jp_merc_fin_3', 'jp_merc_fin_4', 'sbt']

libraries = [
    'assets',    'coins',     'digitado',  'drawgraph', 'drawpizza',
    'drawtable', 'focus',     'getdata',   'graphcomp', 'graphics',
    'graphtime', 'ingpos',    'ingraph',   'rank',      'screen',
    'symbols',   'tables',    'util',      'video',     'water',     ]

def set_template(tp_num):
    tp_lib  = importlib.import_module(f'libraries.{templates[tp_num]}')
    tp_vars = [var for var in dir(tp_lib) if not var.startswith("__")]
    
    for lib_name in libraries:
        lib = importlib.import_module(f'libraries.{lib_name}')
        for tp_var in tp_vars:
            
            exec(f"lib.{tp_var} = tp_lib.{tp_var}")
            # setattr(lib, tp_var, getattr(tp_lib, tp_var))  # 10x slower than 'exec'
        lib.template_num = tp_num
