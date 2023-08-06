from .utils import widget_path


class SQLCompleter(object):
    TEIID_SQL_KEYWORD = [
        'ALL', 'AND', 'ANY', 'AGG', 'AS', 'ASC', 'ATOMIC', 'BEGIN', 'BETWEEN', 
        'BIGDECIMAL', 'BIGINT', 'BIGINTEGER', 'BLOB', 'BOOLEAN', 'BOTH', 'BREAK', 
        'BY', 'BYTE', 'CALL', 'CASE', 'CAST', 'CHAR', 'CLOB', 'COLUMN', 'COMMIT', 
        'CONSTRAINT', 'CONTINUE', 'CONVERT', 'CREATE', 'CROSS', 'DATE', 'DAY', 
        'DECIMAL', 'DECLARE', 'DEFAULT', 'DELETE', 'DESC', 'DISTINCT', 'DOUBLE', 
        'DROP', 'EACH', 'ELSE', 'END', 'ERROR', 'ESCAPE', 'EXCEPT', 'EXEC', 'EXECUTE', 
        'EXISTS', 'FALSE', 'FETCH', 'FILTER', 'FLOAT', 'FOR', 'FOREIGN', 'FROM', 'FULL', 
        'FUNCTION', 'GEOMETRY', 'GLOBAL', 'GROUP', 'HAVING', 'HOUR', 'IF', 'IMMEDIATE', 
        'IN', 'INNER', 'INOUT', 'INSERT', 'INTEGER', 'INTERSECT', 'INTO', 'IS', 'JOIN', 
        'LANGUAGE', 'LATERAL', 'LEADING', 'LEAVE', 'LEFT', 'LIKE', 'REGEX', 'LIMIT', 
        'LOCAL', 'LONG', 'LOOP', 'MAKEDEP', 'MAKEIND', 'MAKENOTDEP', 'MERGE', 'MINUTE', 
        'MONTH', 'NO', 'NOCACHE', 'NOT', 'NULL', 'OBJECT', 'OF', 'OFFSET', 'ON', 'ONLY', 
        'OPTION', 'OPTIONS', 'OR', 'ORDER', 'OUT', 'OUTER', 'OVER', 'PARAMETER', 'PARTITION', 
        'PRIMARY', 'PROCEDURE', 'REAL', 'REFERENCES', 'RETURN', 'RETURNS', 'RIGHT', 'ROLLUP', 
        'ROW', 'ROWS', 'SECOND', 'SELECT', 'SET', 'SHORT', 'SIMILAR', 'SMALLINT', 'SOME', 
        'SQLEXCEPTION', 'SQLSTATE', 'SQLWARNING', 'STRING', 'TABLE', 'TEMPORARY', 'THEN', 
        'TIME', 'TIMESTAMP', 'TINYINT', 'TO', 'TRAILING', 'TRANSLATE', 'TRIGGER', 'TRUE', 
        'UNION', 'UNIQUE', 'UNKNOWN', 'UPDATE', 'USER', 'USING', 'VALUES', 'VARBINARY', 
        'VARCHAR', 'VIRTUAL', 'WHEN', 'WHERE', 'WHILE', 'WITH', 'WITHOUT', 'XML', 
        'XMLAGG', 'XMLATTRIBUTES', 'XMLCAST', 'XMLCOMMENT', 'XMLCONCAT', 'XMLELEMENT', 
        'XMLEXISTS', 'XMLFOREST', 'XMLNAMESPACES', 'XMLPARSE', 'XMLPI', 'XMLQUERY', 'XMLSERIALIZE', 
        'XMLTABLE', 'XMLTEXT', 'YEAR'
    ]

    TEIID_SQL_FUNCTION = [
        'ACCESSPATTERN', 'ARRAYTABLE', 'INCREMENT', 'AVG', 'CHAIN', 'COLUMNS', 'CONTENT', 'COUNT', 
        'DELIMITER', 'RANK', 'DISABLED', 'DOCUMENT', 'EMPTY', 'ENABLED', 'ENCODING', 'EVERY', 'EXCEPTION', 
        'EXCLUDING', 'EXTRACT', 'FIRST', 'HEADER', 'INCLUDING', 'INDEX', 'INSTEAD', 'AGG', 'JSONOBJECT', 
        'KEY', 'LAST', 'MAX', 'MIN', 'NAME', 'NAMESPACE', 'NEXT', 'NULLS', 'OBJECTTABLE', 'ORDINALITY', 
        'PASSING', 'PATH', 'PRESERVE', 'QUERYSTRING', 'QUOTE', 'RAISE', 'RANK', 'RESULT', 'NUMBER', 
        'SELECTOR', 'SERIAL', 'SKIP', 'DAY', 'SECOND', 'HOUR', 'MINUTE', 'MONTH', 'QUARTER', 'SECOND', 
        'WEEK', 'YEAR', 'POP', 'SAMP', 'SUBSTRING', 'SUM', 'TEXTAGG', 'TEXTTABLE', 'TIMESTAMPADD', 
        'TIMESTAMPDIFF', 'BYTES', 'CHARS', 'TRIM', 'VARIADIC', 'POP', 'SAMP', 'VERSION', 'VIEW', 
        'WELLFORMED', 'WIDTH', 'XMLDECLARATION'
    ]

    DAWET_METADATA_FILE = widget_path.joinpath('dawetmetadata.txt')

    def __init__(self):
        if self.DAWET_METADATA_FILE.is_file():
            self.DAWET_METADATA = self.DAWET_METADATA_FILE.read_text().split()
        else:
            self.DAWET_METADATA = []

    def complete(self, zeromq_interactive_shell, event):
        key = event.line.strip().split()[-1]
        return list(filter(
            lambda x: x.startswith(key), 
            self.TEIID_SQL_KEYWORD+self.TEIID_SQL_FUNCTION+self.DAWET_METADATA
        ))