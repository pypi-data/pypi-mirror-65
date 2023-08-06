import logging
import time

import pypyodbc
import sys
import re
import os
from pandas import read_sql, concat
from IPython.core import magic_arguments
from IPython.core.magic import magics_class, Magics, line_magic, cell_magic, needs_local_scope
from dawetsql.widgets import SchemaExplorer, LoginWidgets
from . import utils


@magics_class
class OdbcSqlMagics(Magics):

    def __init__(self, *args, **kwargs):
        utils.widget_path.mkdir(exist_ok=True)
        self.conn = None
        self.chunksize = 500
        super(OdbcSqlMagics, self).__init__(*args, **kwargs)

    def connect(self, dsn, username, password, connection_string, verbose=True):
        """
        Open database connection
        :param dsn: DSN name
        :param username: Database username
        :param password: Database password
        :param connection_string: ODBC connectin string
        :param verbose: verbose output
        :return:
        """
        try:
            if connection_string:
                self.conn = pypyodbc.connect(connection_string)
            else:
                connection_string = 'DSN={};'.format(dsn)

                if username and password:
                    connection_string += 'Username={};Password={}'.format(username, password)
                self.conn = pypyodbc.connect(connection_string)
            if self.conn and verbose:
                print("Connected!")
        except Exception as e:
            logging.error(e)
            return

    @line_magic('dawetsql')
    def new_odbc_connect(self, args):
        """
        Open database connection, use `dawetsqlold` for old method.
        :param args:
        :return:
        """
        login_widgets = LoginWidgets(self)
        login_widgets.show()

    @line_magic('dawetsqlold')
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('-u', '--user', type=str, help="Dawet User")
    @magic_arguments.argument('-p', '--password', type=str, help="Dawet Password")
    @magic_arguments.argument('-d', '--dsn', type=str, help="Dawet DSN")
    @magic_arguments.argument('-x', '--connection', type=str, help="ODBC Connection String")
    @magic_arguments.argument('-c', '--chunksize', type=int, default=100, help="ODBC Fetch size")
    def odbc_connect(self, arg):
        """
        Open Database Connection line magic method
        :param arg: magic arguments
        :return:
        """
        if self.conn:
            self.odbc_disconnect()

        args = magic_arguments.parse_argstring(self.odbc_connect, arg)

        self.chunksize = args.chunksize

        return self.connect(args.dsn, args.user, args.password, args.connection)

    @line_magic('dawetsqlclose')
    def odbc_disconnect(self, *args, **kwargs):
        """
        Close Database Connection line magic method
        :return:
        """
        try:
            self.conn.close()
            print("Disconnected")
        except:
            pass
        finally:
            self.conn = None
            return

    @needs_local_scope
    @cell_magic('dawetsql')
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('-l', '--limit', type=int, default=10, help="Set result limit")
    @magic_arguments.argument('-o', '--output', default='_', type=str, help="File or Variable name for results data")
    @magic_arguments.argument('-d', '--decimal-separator', default=',', type=str,
                              help="Decimal separator for float data (for csv output only)")
    @magic_arguments.argument('-s', '--separator', default=',', type=str, help="Columns separator (for csv output only)")
    def odbc_sql(self, arg, cell=None, local_ns=None):
        """
        Run SQL Query. SQL query can user Python Variable, just put `?varname` as placeholder.
        :param arg: optional argument
        :param cell: SQL Query string
        :return:
        """
        args = magic_arguments.parse_argstring(self.odbc_sql, arg)
        varname = args.output.strip()
        
        placeholders = re.findall(r'\?([^\d\W]\w*\Z)', cell, re.DOTALL)
        for placeholder in placeholders:
            value = local_ns[placeholder.strip('?')]
            if type(value) in [int, float]:
                value = str(value)
            else:
                value = "'{}'".format(value)
            cell = cell.replace(placeholder, value)

        ok, valid_name = utils.validate_name(varname)
        query = ' '.join(cell.strip().split())

        if not ok:
            logging.error("Cannot proceed with `{}` as output name".format(varname))
            return

        if not self.conn:
            logging.error(
                "Please open connection first using %dawetsql line magic")
            return

        if valid_name != '_':
            if valid_name.lower().split('.')[-1] in ['csv', 'pkl', 'xlsx'] and os.path.isfile(valid_name):
                valid_name += '_' + str(int(time.time()))

            if valid_name.lower().endswith('.csv'):
                self.to_csv(query=query, filename=valid_name, separator=args.separator.strip(),
                            decimal=args.decimal_separator.strip())
                return
            elif valid_name.lower().endswith('.pkl'):
                self.to_pickle(query, valid_name)
                return
            elif valid_name.lower().endswith('.xlsx'):
                self.to_excel(query, valid_name)
                return
            else:
                self.to_dataframe(query, valid_name, download=True)
                return

        return self.to_dataframe(utils.limit_query(query, args.limit), valid_name)

    def download(self, query):
        if not self.conn:
            logging.error("Connection is closed!")
            return

        utils.log_query(query)
        try:
            data = read_sql(query, self.conn, chunksize=self.chunksize)
            return data
        except Exception as e:
            logging.error(e.__class__.__name__)
            logging.error(e)
            return

    def get_dataframe(self, query, verbose=True):
        """
        Store query result to dataframe
        :param query: SQL Query
        :param verbose: print process to stdout
        :return: pandas dataframe
        """
        print("Fetching result", flush=True) if verbose else None

        result = self.download(query)

        if result is None:
            return

        def generate_df():
            total = 0
            for chunk in result:
                total += len(chunk)
                self.print_process(total) if verbose else None
                yield chunk

        try:
            return concat(generate_df(), ignore_index=True)
        except ValueError:
            return

    def to_csv(self, query, filename, separator=',', decimal=','):
        """
        Export query result to csv
        :param query: SQL Query
        :param filename: csv filename
        :param separator: csv separator
        :param decimal: csv decimal separator
        :return:
        """
        result = self.download(query)

        if result is None:
            return

        total = 0
        header = True

        for chunk in result:
            if header:
                mode = 'w'
            else:
                mode = 'a'
            chunk.to_csv(filename, index=False, mode=mode, header=header, sep=separator, decimal=decimal)
            total += len(chunk)
            self.print_process(total)
            header = False

    def to_excel(self, query, filename):
        """
        Export query result to excel (.xlsx)
        :param query: SQL query to export
        :param filename: File name for results
        :return: None
        """

        raise NotImplementedError("Not Impelented!")

        # result = self.download(query)
        # total = 0
        # current_sheet = 1
        #
        # with ExcelWriter(filename) as writer:
        #     for chunk in result:
        #         if total > 1000000:
        #             current_sheet += 1
        #
        #         chunk.to_excel(writer, sheet_name='Sheet'+str(current_sheet))
        #         total += len(chunk)
        #         self.print_process(total)

    def to_dataframe(self, query, varname, download=False):
        """
        Store dataframe to shell variable
        :param query: SQL query
        :param varname: Dataframe variable name
        :param download: Download or just preview query result
        :return:
        """
        df = self.get_dataframe(query)

        if df is None:
            return

        self.shell.user_ns[varname] = df
        if not download:
            return df

    def to_pickle(self, query, pickle_name):
        """
        Export query result to python pickle
        :param query: SQL Query
        :param pickle_name: pickle file name
        :return:
        """
        df = self.get_dataframe(query)

        if df is None:
            return

        df.to_pickle(pickle_name)

    @line_magic('explorer')
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('-f', '--force', action='store_true', help="Force explorer to re-index schema")
    def explore_schema(self, arg):
        """
        Display schema explorer widgets
        :return:
        """
        args = magic_arguments.parse_argstring(self.explore_schema, arg)

        print('Fetching schema detail..')

        explorer = SchemaExplorer(self)
        explorer.show(force=args.force)

    @staticmethod
    def print_process(total):
        sys.stdout.write("\rTotal {} row(s) downloaded".format(total))
        sys.stdout.flush()

    def __del__(self):
        if self.conn:
            self.conn.close()

        self.conn = None
