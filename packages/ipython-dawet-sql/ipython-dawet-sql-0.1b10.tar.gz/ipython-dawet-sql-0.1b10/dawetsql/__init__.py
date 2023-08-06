from .odbc_sql import OdbcSqlMagics
from .completer import SQLCompleter

__version__ = '0.1b10'
__author__ = 'Agung Pratama'

def load_ipython_extension(ipython):
    completer = SQLCompleter()
    ipython.set_hook('complete_command', completer.complete, re_key='.*')
    ipython.register_magics(OdbcSqlMagics)
