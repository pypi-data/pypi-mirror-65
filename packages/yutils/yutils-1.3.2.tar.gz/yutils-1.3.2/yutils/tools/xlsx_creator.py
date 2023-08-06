#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import os

from datetime import datetime
from xlsxwriter import Workbook
import string

from yutils.exceptions import InputError

from yutils.tools.check_object_type import check_object_type


class XLSXCreator(object):
    _INPUT_TYPES = {'headers': (list, str),
                    'table': (list, list),
                    'output_path': str}

    CELL_WIDTH_EXTRA = 5
    TABLE_GRID = 'A1:{last_column_letter}{amount_of_rows}'
    TABLE_STYLE = 'TableStyleMedium2'

    SPECIAL_FORMATS = {datetime: '_date_format'}
    DATETIME_NUM_FORMAT = 'dd/mm/yyyy hh:mm:ss.000'

    def __init__(self, headers, table, output_path):
        """
        A class to create an XLSX file from a table.
        It will format the table inside an actual excel's table, according to each field's width.

        :param headers: The fields of the table (headers)
        :type headers: list of str
        :param table: The table
        :type table: matrix - list of lists of the same lengths (cells may be any datatype)
        :param output_path: The path where to save the excel
        :type output_path: str
        """
        self.headers = headers
        self.table = table
        self.output_path = output_path

        self._check_inputs()

        self._filename = os.path.basename(self.output_path)
        self._dirname = os.path.dirname(self.output_path)

        self.workbook = None
        self._formats = {}
        self._last_col_ltr = None

    def _check_inputs(self):
        types_dict = {'type': object}
        types_dict.update(self._INPUT_TYPES)
        check_object_type(self, types_dict)

        for row in self.table:
            if not len(row) == len(self.headers):
                raise InputError("Row #{} is of length {} and not {} (like headers)".format(self.table.index(row) + 1,
                                                                                            len(row),
                                                                                            len(self.headers)))

        if not (os.path.exists(self._dirname) and os.path.isdir(self._dirname)):
            raise InputError("Dir {} doesn't exist".format(self._dirname))

    @property
    def date_format(self):
        if 'date' not in self._formats:
            self._formats['date'] = self.workbook.add_format({'num_format': self.DATETIME_NUM_FORMAT})
        return self._formats['date']

    @property
    def _row_to_length(self):
        """
        input:
        xlsxwriter.Worksheet.set_column('A:A', 16)
        for each column add a record to a dict of the maximum length appeared for the location where it should be.
        :return: dict of {cells_range ('A:A'): width(max_len(column))
        """
        lengths_list = [max([len(str(value)) for value in field_list]) for field_list in zip(*self.table)]
        row_to_length_dict = {}

        for length in lengths_list:
            self._last_col_ltr = get_next_column(self._last_col_ltr)
            row_to_length_dict['{col}:{col}'.format(col=self._last_col_ltr)] = length + self.CELL_WIDTH_EXTRA

        return row_to_length_dict

    @property
    def _header_dicts(self):
        """
        input in here:
        xlsxwriter.Worksheet.add_table({'columns': [('header': name), ...]})
        should define which headers will be in the table in the xlsx file.
        :return: a list of dicts
        """
        header_dicts = []
        for header in self.headers:
            header_dict = {'header': header}

            # Check for special formats (if all column is a certain datatype - e.g. datetime
            header_index = self.headers.index(header)
            col_types = list(set(type(cell) for cell in (row[header_index] for row in self.table) if cell))
            # If there is only one datatype, and it has a special format, add it to header dict
            if len(col_types) == 1 and col_types[0] in self.SPECIAL_FORMATS:
                header_dict['format'] = getattr(self, self.SPECIAL_FORMATS[col_types[0]])

            header_dicts.append(header_dict)
        return header_dicts

    @property
    def _table_span(self):
        return self.TABLE_GRID.format(last_column_letter=self._last_col_ltr,
                                      amount_of_rows=len(self.table) + 1)

    def _write_workbook(self):
        """
        Creates the actual worksheet and table in self.workbook
        """
        ws = self.workbook.add_worksheet()

        # Set column lengths
        for cell, width in self._row_to_length.items():
            ws.set_column(cell, width)

        ws.add_table(self._table_span,
                     {'data': self.table,
                      'columns': self._header_dicts,
                      'style': self.TABLE_STYLE})

    def run(self):
        """
        Creates the XLSX
        """
        cwd = os.getcwd()
        os.chdir(self._dirname)

        with Workbook(self._filename) as self.workbook:
            self._write_workbook()

        os.chdir(cwd)


def table_to_str(table):
    """
    matrix good for the function xlsxwriter.Worksheet.add_table(['data': table))
    :param table: matrix - list of lists of the same lengths (cells may be any datatype)
    :return: fully string matrix
    """
    return [[str(value) for value in row] for row in table]


def get_next_letter(ltr):
    if ltr == 'Z':
        return 'A'
    return string.ascii_uppercase[string.ascii_uppercase.index(ltr) + 1]


def get_next_column(col=None):
    if not col:
        return 'A'

    i = 1
    next_ltr = get_next_letter(col[-1])
    col = col[:-1] + next_ltr

    while next_ltr == 'A':
        if len(col) == i:
            return 'A' + col

        i += 1
        next_ltr = get_next_letter(col[-i])
        col = col[:-i] + next_ltr + col[-i + 1:]

    return col


def create_xlsx(headers, table, output_path):
    """
    Creates an XLSX file from a table.
    It will format the table inside an actual excel's table, according to each field's width.

    :param headers: The fields of the table (headers)
    :type headers: list of str
    :param table: The table
    :type table: matrix - list of lists of the same lengths (cells may be any datatype)
    :param output_path: The path where to save the excel
    :type output_path: str
    """
    xlsx_creator = XLSXCreator(headers, table, output_path)
    xlsx_creator.run()
