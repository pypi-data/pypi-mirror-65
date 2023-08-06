#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import datetime
import traceback

from yutils.queries.csv_to_db.obj.table_data import TableData
from yutils.queries.csv_to_db.consts.consts import NVARCHAR_HEBREW_ENCODINGS, DATETIME_FORMATS, \
    DB_DATETIME_FORMAT_PYTHON, DB_DATETIME_FORMAT_SQL, TIMESTAMP_FORMATS, DB_TIMESTAMP_FORMAT_PYTHON, \
    DB_TIMESTAMP_FORMAT_SQL
from yutils.queries.csv_to_db.exceptions.csv_to_db_exceptions import NoTableError, BadDateFormatError, \
    BadNVarCharFormatError, MissingFieldError, DataInsertionCancelled, NoInsertQuery


class FieldTypeHandlers(object):
    @staticmethod
    def handle_datetime_field(field_data):
        """
        Handles date fields. Tries to find the date format and prepares it for the insert query.
        """
        if not field_data:
            return "''"

        date_field = ""

        # these (timestamp formats) are for timestamps with 000 as fraction seconds
        for time_format in DATETIME_FORMATS + TIMESTAMP_FORMATS:
            try:
                date_field = datetime.datetime.strptime(field_data, time_format)
                break
            except ValueError:
                continue
        if not date_field:
            raise BadDateFormatError(field_data)

        field_string = date_field.strftime(DB_DATETIME_FORMAT_PYTHON)
        field_to_insert = "TO_DATE('{field_data}', '{date_format}')".format(field_data=field_string,
                                                                            date_format=DB_DATETIME_FORMAT_SQL)
        return field_to_insert

    @staticmethod
    def handle_timestamp_field(field_data):
        """
        Handles date fields. Tries to find the date format and prepares it for the insert query.
        """
        if not field_data:
            return "''"

        date_field = ""

        for time_format in TIMESTAMP_FORMATS:
            try:
                date_field = datetime.datetime.strptime(field_data, time_format)
                break
            except ValueError as e:
                if 'unconverted data remains' in str(e):
                    # When "unconverted data remains" error is raised,
                    # it is probably because resolution has more digits after decimal point than 6.
                    try:
                        # Try lowering to 6 digits after decimal point
                        date_field = datetime.datetime.strptime(field_data[:field_data.rindex('.') + 7], time_format)
                        break
                    except ValueError:
                        continue
                else:
                    continue
        if not date_field:
            raise BadDateFormatError(field_data)

        field_string = date_field.strftime(DB_TIMESTAMP_FORMAT_PYTHON)
        field_to_insert = "TO_TIMESTAMP('{field_data}', '{date_format}')".format(field_data=field_string,
                                                                                 date_format=DB_TIMESTAMP_FORMAT_SQL)
        return field_to_insert

    @staticmethod
    def handle_str_field(field_data):
        field_to_insert = "'{field_data}'".format(field_data=field_data.replace("'", "''"))
        return field_to_insert

    @staticmethod
    def handle_nvarchar_field(field_data):
        for encoding in NVARCHAR_HEBREW_ENCODINGS:
            try:
                field_data = field_data.decode(encoding)
                break
            except UnicodeDecodeError:
                pass

        if not isinstance(field_data, str):
            raise BadNVarCharFormatError(repr(field_data))

        data_to_insert = ''
        for ltr in field_data:
            new_ltr = repr(ltr)[2:-1]
            if len(new_ltr) == 1:
                data_to_insert += new_ltr if new_ltr != "'" else "''"
            elif len(new_ltr) == 6 and new_ltr[:2] == '\\u':
                data_to_insert += '\\' + new_ltr[2:]
            else:
                raise BadNVarCharFormatError(repr(new_ltr))

        field_to_insert = "UNISTR('{field_data}')".format(field_data=data_to_insert)
        return field_to_insert

    @staticmethod
    def handle_number_field(field_data):
        return field_data


class RowToInsert(object):
    DATATYPE_HANDLERS = {'NUMBER': FieldTypeHandlers.handle_number_field,
                         'DATE': FieldTypeHandlers.handle_datetime_field,
                         'TIMESTAMP': FieldTypeHandlers.handle_timestamp_field,
                         'NVARCHAR2': FieldTypeHandlers.handle_nvarchar_field,
                         'VARCHAR2': FieldTypeHandlers.handle_str_field,
                         'BLOB': FieldTypeHandlers.handle_str_field,
                         'CLOB': FieldTypeHandlers.handle_str_field}

    INSERT_QUERY = """INSERT INTO {table_name} ({fields_names})
VALUES ({fields_data})"""

    def __init__(self, row_data, field_data_types):
        """
        One row from a query to insert to DB

        :param row_data: data of one row
        :type row_data: dict (the keys are the fields and the values are the data of the field)
        :param field_data_types: a dict mapping between field names and their data types
        :type field_data_types: dict
        """
        self.row_data = row_data
        self.field_data_types = field_data_types

        self.fields_data_to_query = None
        self.fields_names_to_query = None
        self.insert_query = None

    def _create_fields_data(self):
        """
        Creates the fields data part of the insert query
        """
        all_fields_data = []
        for field_name, field_data in self.row_data.items():
            if not field_data:
                query_field_data = 'NULL'
            else:
                query_field_data = self.DATATYPE_HANDLERS[self.field_data_types[field_name]](field_data)
            all_fields_data.append(query_field_data)
        self.fields_data_to_query = " , ".join(all_fields_data)

    def create_insert_query(self, table_name):
        """
        Creates the insert query for the row

        :param table_name: the name of the table to insert the row into
        :type table_name: str
        """
        self._create_fields_data()
        self.fields_names_to_query = " , ".join(self.row_data.keys())
        self.insert_query = self.INSERT_QUERY.format(table_name=table_name,
                                                     fields_names=self.fields_names_to_query,
                                                     fields_data=self.fields_data_to_query)


class InsertDataToDB(object):
    _COL_DATATYPES_QUERY = """SELECT LOWER(column_name) AS column_name, datatype
  FROM all_tab_columns
 WHERE table_name = '{table_name}'
   AND owner = '{schema_name}'"""
    _DUPLICATE_ROW_QUERY = """SELECT *
  FROM {table_name}
 WHERE {field_name} = '{field_value}'"""

    def __init__(self, connection_details, table_name, data_to_insert,
                 commit=True, check_duplicates=False, duplicate_field_check=None,
                 print_queries=True):
        """
        Inserts the data into a table in the DB

        :param connection_details: Details for connection to the wanted Oracle DB
        :type connection_details: yutils.conn.sql_connection_details.OracleConnectionDetails
        :param table_name: the name of the table to insert the data into
        :type table_name: str
        :param data_to_insert: the data you want to insert into the table
        :type data_to_insert: yutils.queries.csv_to_db.obj.table_data.TableData object
        :param commit: whether or not to commit (default: True)
        :type commit: bool
        :param check_duplicates: if to ignore rows already inserted into the DB (default: False)
        :type check_duplicates: bool
        :param duplicate_field_check: the column name of the unique field in the table (for uniqueness check) -
                                      (usually is an ID field)
        :type duplicate_field_check: str
        :param print_queries: if to print queries (default: True)
        :type print_queries: bool
        """
        self.connection_details = connection_details
        self.table_name = table_name
        self.data_to_insert = data_to_insert
        self.commit = commit
        self.check_duplicates = check_duplicates
        self.duplicate_field_check = duplicate_field_check
        self.print_queries = print_queries

        self.field_types = None

    def _verbose_print(self, text):
        if self.print_queries:
            print(text)

    def _get_field_types(self):
        datatype_query = self._COL_DATATYPES_QUERY.format(table_name=self.table_name.upper(),
                                                          schema_name=self.connection_details.SCHEMA.upper())

        self._verbose_print(datatype_query)

        res = self.connection_details.query(datatype_query)
        if not res:
            raise NoTableError(self.table_name, self.connection_details.SCHEMA)

        field_types = {row.column_name: self._format_datatype(row.data_type) for row in res}
        self._check_for_missing_field(field_types)
        return field_types

    @staticmethod
    def _format_datatype(datatype):
        if '(' not in datatype:
            return datatype
        return datatype[:datatype.index('(')]

    def _check_for_missing_field(self, field_types):
        for field in self.data_to_insert.row_dicts[0].keys():
            if field not in field_types:
                raise MissingFieldError(field, self.table_name)

    def _check_if_row_exists(self, row):
        check_query = self._DUPLICATE_ROW_QUERY.format(table_name=self.table_name,
                                                       field_name=self.duplicate_field_check,
                                                       field_value=row[self.duplicate_field_check])

        self._verbose_print(check_query)

        res = self.connection_details.query(check_query)

        if res:
            return True
        return False

    def _insert_row_to_db(self, row):
        """
        Inserts one row to the DB
        :param row: data of one row
        :type row: dict (the keys are the fields and the values are the data of the field)
        """
        insert_row = RowToInsert(row, self.field_types)
        insert_row.create_insert_query(self.table_name)

        if not insert_row.insert_query:
            raise NoInsertQuery()

        self._verbose_print(insert_row.insert_query)

        try:
            self.connection_details.query(insert_row.insert_query)
        except:
            print('\n\n~~~~~~~~*******~~~~~~~~')
            print('ERROR INSERTING!!!')
            traceback.print_exc()
            print('~~~~~~~~*******~~~~~~~~\n\n')

    def insert_data(self):
        """
        Inserts all the rows to the DB
        """
        self.field_types = self._get_field_types()

        for row in self.data_to_insert.row_dicts:
            if self.check_duplicates and self._check_if_row_exists(row):
                continue
            self._insert_row_to_db(row)

        if self.commit:
            self.connection_details.commit()
            print('Committed.')


def insert_data_to_table(connection_details, table_name, data_to_insert,
                         data_to_insert_type='path', data_fields=None, commit=True,
                         check_duplicates=False, duplicate_field_check=None, force=False, print_queries=True):
    """
    Gets data from csv or list of lists, and inserts it into the table in the DB.

    :param connection_details: Details for connection to the wanted Oracle DB
    :type connection_details: yutils.conn.sql_connection_details.OracleConnectionDetails
    :param table_name: the name of the table to insert the data into
    :type table_name: str
    :param data_to_insert: the data you want to insert into the table
    :type data_to_insert: str / matrix (list of lists)
    :param data_to_insert_type: the type of the data ('path' / 'data')
    :type data_to_insert_type: str
    :param data_fields: the names of the fields of the data to insert
                        (if None, takes the values of the first line of the CSV as the field names)
    :type data_fields: list of str
    :param commit: whether or not to commit (default: True)
    :type commit: bool
    :param check_duplicates: if to ignore rows already inserted into the DB (default: False)
    :type check_duplicates: bool
    :param duplicate_field_check: the column name of the unique field in the table (for uniqueness check) -
                                  (usually is an ID field)
    :type duplicate_field_check: str
    :param force: if to force data insertion (won't ask for permission) (default: False)
    :type force: bool
    :param print_queries: if to print queries (default: True)
    :type print_queries: bool

    :return: None
    """
    shlifa_data = TableData(data_to_insert, data_to_insert_type, data_fields)

    if not force and input("Insert {rows} rows into table '{table_name}'? (y/n) "
                                       .format(rows=len(shlifa_data.row_dicts),
                                               table_name=table_name)) != 'y':
        raise DataInsertionCancelled()

    insert_to_db = InsertDataToDB(connection_details, table_name, shlifa_data, commit,
                                  check_duplicates, duplicate_field_check, print_queries)
    insert_to_db.insert_data()
