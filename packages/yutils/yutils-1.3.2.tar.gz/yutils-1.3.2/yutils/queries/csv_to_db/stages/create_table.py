#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import datetime
from collections import OrderedDict

from yutils.queries.csv_to_db.exceptions.csv_to_db_exceptions import NotThisDatatypeError, TableCreationCancelled
from yutils.queries.csv_to_db.consts.consts import DATETIME_FORMATS, TIMESTAMP_FORMATS
from yutils.queries.csv_to_db.obj.table_data import TableData


class DatatypeCheckers(object):
    LOB_SIZE_BOUNDARY = 1024

    @staticmethod
    def _get_max_len(column_list):
        return max(len(i) for i in column_list)

    @staticmethod
    def _get_field_utf8_len(field_data):
        """
        Definitely IS NOT exact!
        """
        full_len = 0
        for ltr in field_data:
            try:
                ltr.decode('ascii')
                full_len += 1
            except UnicodeDecodeError:
                full_len += 2
        return full_len

    @classmethod
    def _get_unicode_max_len(cls, column_list):
        return max(cls._get_field_utf8_len(i) for i in column_list)

    @staticmethod
    def check_date(column_list):
        if not any(column_list):
            raise NotThisDatatypeError()

        for field_data in column_list:
            if not field_data:
                continue
            is_date = False
            for time_format in DATETIME_FORMATS:
                try:
                    datetime.datetime.strptime(field_data, time_format)
                    is_date = True
                    break
                except ValueError:
                    continue
            if not is_date:
                raise NotThisDatatypeError()

        return 'DATE'

    @staticmethod
    def check_timestamp(column_list):
        if not any(column_list):
            raise NotThisDatatypeError()

        for field_data in column_list:
            if not field_data:
                continue
            is_date = False
            for time_format in TIMESTAMP_FORMATS:
                try:
                    datetime.datetime.strptime(field_data, time_format)
                    is_date = True
                    break
                except ValueError as e:
                    if 'unconverted data remains' in str(e):
                        # When "unconverted data remains" error is raised,
                        # it is probably because resolution has more digits after decimal point than 6.
                        try:
                            # Try lowering to 6 digits after decimal point
                            datetime.datetime.strptime(field_data[:field_data.rindex('.') + 7], time_format)
                            is_date = True
                            break
                        except ValueError:
                            continue
                    else:
                        continue
            if not is_date:
                raise NotThisDatatypeError()
        second_fractions = list(set(int(field.split('.')[-1]) for field in column_list if '.' in field))
        if second_fractions in ([], [0]):
            return 'DATE'
        return 'TIMESTAMP'

    @staticmethod
    def check_number(column_list):
        if not any(column_list):
            raise NotThisDatatypeError()

        # Check if fields are ints/floats
        for field in column_list:
            if not field:
                continue
            try:
                int(field)
            except ValueError:
                try:
                    float(field)
                except ValueError:
                    raise NotThisDatatypeError()

        max_digits_before_decimal = max(len(str(int(float(field)))) for field in column_list)
        max_digits_after_decimal = max(len(field.split('.')[1]) for field in column_list if '.' in field) \
            if any('.' in field for field in column_list) else 0
        max_digits = max_digits_before_decimal + max_digits_after_decimal
        return 'NUMBER({precision}, {scale})'.format(precision=max_digits,
                                                     scale=max_digits_after_decimal)

    @classmethod
    def check_lob(cls, column_list):
        if not any(column_list):
            raise NotThisDatatypeError()

        if cls._get_max_len(column_list) < cls.LOB_SIZE_BOUNDARY:
            raise NotThisDatatypeError()

        for field in column_list:
            if not field:
                continue
            try:
                field.decode('ascii')
            except UnicodeDecodeError:
                return 'BLOB'

        return 'CLOB'

    @classmethod
    def check_characters(cls, column_list):
        if not any(column_list):
            raise NotThisDatatypeError()

        max_len = cls._get_max_len(column_list)

        for field in column_list:
            try:
                field.decode('ascii')
            except UnicodeDecodeError:
                unicode_max_len = cls._get_unicode_max_len(column_list)
                return 'NVARCHAR2({unicode_max_len})'.format(unicode_max_len=unicode_max_len)

        return 'VARCHAR2({max_len})'.format(max_len=max_len)


class ColumnMapper(object):
    _DATATYPE_CHECKER_ORDER = [DatatypeCheckers.check_date,
                               DatatypeCheckers.check_timestamp,
                               DatatypeCheckers.check_number,
                               DatatypeCheckers.check_lob,
                               DatatypeCheckers.check_characters]

    def __init__(self, table_data):
        self.table_data = table_data
        self.column_types = None


    @classmethod
    def _get_best_column_type(cls, column_list):
        datatype = ''
        for datatype_checker in cls._DATATYPE_CHECKER_ORDER:
            try:
                datatype = datatype_checker(column_list)
                break
            except NotThisDatatypeError:
                continue
        if not datatype:
            return 'VARCHAR2(1)'
        return datatype

    def map(self):
        self.column_types = OrderedDict()
        for field in self.table_data.fields:
            column_list = self.table_data.column_dicts[field]
            self.column_types[field] = self._get_best_column_type(column_list)


class CreateQuery(object):
    _CREATE_QUERY_TEMPLATE = """CREATE TABLE {table_name} (
{fields_data}
)"""

    def __init__(self, column_types, table_name):
        self.column_types = column_types
        self.table_name = table_name

        self.create_query = None

    @staticmethod
    def _format_dict(dictionary):
        dict_str = ""
        indent_len = max([len(str(key)) for key in dictionary.keys()]) + 2
        for key, value in dictionary.items():
            dict_str += '    {key}{spaces}{value},\n'.format(key=key,
                                                             spaces=' ' * (indent_len - len(str(key))),
                                                             value=value)
        return dict_str[:-2]  # remove last comma + newline

    def build_create_query(self):
        self.create_query = self._CREATE_QUERY_TEMPLATE.format(table_name=self.table_name,
                                                               fields_data=self._format_dict(self.column_types))


def get_ifyun_for_table(table_name, table_data, table_data_type='path', data_fields=None):
    """
    Gets data from csv or list of lists, and plans a table for it

    :param table_name: the name of the table to create
    :type table_name: str
    :param table_data: the data you want to create the table based on
    :type table_data: str/list
    :param table_data_type: the type of the table_data ('path' / 'data')
    :type table_data_type: str
    :param data_fields: the name of the fields of the data to insert
                        (if None, takes the values of the first line as the fields names)
    :type data_fields: list

    :return: None
    """
    table_data = TableData(table_data, table_data_type, data_fields)

    mapper = ColumnMapper(table_data)
    mapper.map()

    query_maker = CreateQuery(mapper.column_types, table_name)
    query_maker.build_create_query()

    return query_maker.create_query


def create_table(connection_details, table_name, table_data, table_data_type='path', data_fields=None,
                 force=False, print_queries=True):
    """
    Gets the data from csv or list of lists, and creates a new table in the DB for in info to be inserted into.

    :param connection_details: Details for connection to the wanted Oracle DB
    :type connection_details: yutils.conn.sql_connection_details.OracleConnectionDetails
    :param table_name: the name of the table to insert the data into
    :type table_name: str
    :param table_data: the data you want to insert into the table
    :type table_data: str / matrix (list of lists)
    :param table_data_type: the type of the data ('path' / 'data')
    :type table_data_type: str
    :param data_fields: the names of the fields of the data to insert
                        (if None, takes the values of the first line of the CSV as the field names)
    :type data_fields: list of str
    :param force: if to force table creation (won't ask for permission) (default: False)
    :type force: bool
    :param print_queries: if to print queries (default: True)
    :type print_queries: bool

    :return: None
    """
    assert connection_details.TYPE == 'oracle'

    create_query = get_ifyun_for_table(table_name, table_data, table_data_type, data_fields)
    if print_queries:
        print(create_query)

    if not force and input('Create table? (y/n) ') != 'y':
        raise TableCreationCancelled()

    connection_details.query(create_query)  # No commit is necessary for CREATE statements (DDL)

    if print_queries:
        print('\nDone.')
